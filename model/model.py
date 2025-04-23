import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.utils import resample
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns

# ==================== STEP 1: Load Dataset ====================
df = pd.read_csv("../data/us_accidents.csv")

# ==================== STEP 2: Basic Cleanup ====================
drop_cols = ['ID', 'Start_Time', 'End_Time', 'Weather_Timestamp', 'City', 'County',
             'Street', 'Zipcode', 'Airport_Code', 'Country', 'State']
df = df.drop(columns=[col for col in drop_cols if col in df.columns], errors='ignore')
df = df.dropna(subset=['Severity', 'Description'])
df = df.dropna()
df = df[df['Severity'].isin([1, 2, 3, 4])]

# ==================== STEP 3: TF-IDF Vectorization for Description ====================
tfidf = TfidfVectorizer(max_features=500, stop_words='english')
desc_tfidf = tfidf.fit_transform(df['Description'].astype(str)).toarray()

# Drop raw Description (it's now vectorized)
df = df.drop(columns=['Description'])

# ==================== STEP 4: Encode Categorical and Scale Numeric Features ====================
categorical_cols = df.select_dtypes(include='object').columns
df = pd.get_dummies(df, columns=categorical_cols)
df['Severity'] = df['Severity'].astype(int)

y_full = df['Severity'] - 1
X_full = df.drop(columns=['Severity'])

scaler = StandardScaler()
X_scaled_structured = scaler.fit_transform(X_full)

# ==================== STEP 5: Combine Structured + TF-IDF Features ====================
X_combined = np.hstack([X_scaled_structured, desc_tfidf])

# ==================== STEP 6: Split and Balance ====================
X_train_all, X_test, y_train_all, y_test = train_test_split(
    X_combined, y_full, test_size=0.2, stratify=y_full, random_state=42
)

train_df = pd.DataFrame(X_train_all)
train_df['Severity'] = y_train_all.values + 1

min_class_size = train_df['Severity'].value_counts().min()
train_balanced = pd.concat([
    resample(g, replace=False, n_samples=min_class_size, random_state=42)
    for _, g in train_df.groupby('Severity')
])

y_train = train_balanced['Severity'].astype(int) - 1
X_train = train_balanced.drop(columns=['Severity']).values

# ==================== STEP 7: PyTorch Setup ====================
X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train.values, dtype=torch.long)
X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test.values, dtype=torch.long)

train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
train_loader = DataLoader(train_dataset, batch_size=256, shuffle=True)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ==================== STEP 8: Model ====================
class AccidentSeverityNN(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 512),
            nn.BatchNorm1d(512),
            nn.LeakyReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, 256),
            nn.BatchNorm1d(256),
            nn.LeakyReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.LeakyReLU(),
            nn.Linear(128, 4)
        )

    def forward(self, x):
        return self.net(x)

model = AccidentSeverityNN(X_train_tensor.shape[1]).to(device)

# ==================== STEP 9: Training ====================
class_counts = np.bincount(y_train)
class_weights = torch.tensor(1. / class_counts, dtype=torch.float32).to(device)
criterion = nn.CrossEntropyLoss(weight=class_weights)
optimizer = optim.AdamW(model.parameters(), lr=0.001)
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.7)

epochs = 50
best_accuracy = 0
patience = 7
early_stop_counter = 0

for epoch in range(epochs):
    model.train()
    running_loss = 0.0
    for X_batch, y_batch in train_loader:
        X_batch, y_batch = X_batch.to(device), y_batch.to(device)
        optimizer.zero_grad()
        outputs = model(X_batch)
        loss = criterion(outputs, y_batch)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
    scheduler.step()

    # Validation
    model.eval()
    with torch.no_grad():
        val_outputs = model(X_test_tensor.to(device))
        y_val_pred = torch.argmax(val_outputs, dim=1).cpu().numpy()
        acc = accuracy_score(y_test, y_val_pred)

    print(f"Epoch {epoch+1}: Loss={running_loss:.4f}, Val Accuracy={acc:.4f}")

    if acc > best_accuracy:
        best_accuracy = acc
        best_model_state = model.state_dict()
        early_stop_counter = 0
    else:
        early_stop_counter += 1
        if early_stop_counter >= patience:
            print("Early stopping.")
            break

# ==================== STEP 10: Evaluation ====================
model.load_state_dict(best_model_state)
model.eval()
with torch.no_grad():
    y_pred = model(X_test_tensor.to(device))
    y_pred_labels = torch.argmax(y_pred, dim=1).cpu().numpy()
    y_true = y_test_tensor.cpu().numpy()

print("\nClassification Report:\n")
print(classification_report(y_true, y_pred_labels, labels=[0, 1, 2, 3]))
print(f"Accuracy: {accuracy_score(y_true, y_pred_labels):.2f}")

# ==================== STEP 11: Confusion Matrix ====================
cm = confusion_matrix(y_true, y_pred_labels)
labels = [1, 2, 3, 4]

plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Oranges', xticklabels=labels, yticklabels=labels)
plt.title('Confusion Matrix - NN Severity Prediction (with Description)')
plt.xlabel('Predicted Severity')
plt.ylabel('True Severity')
plt.tight_layout()
plt.show()
