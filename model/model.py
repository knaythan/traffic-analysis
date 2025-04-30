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



# Shervan Added Code

import re

# Define expanded regex pattern to capture I-5, I 5, US-101, US 101, Hwy, etc.
highway_pattern = r'\b(I[-\s]?\d+|US[-\s]?\d+|Hwy|HWY|highway)\b'

# Create a new 'highway' column in df_original
df_original['highway'] = df_original['Description'].str.contains(highway_pattern, flags=re.IGNORECASE, na=False)

# Create a filtered DataFrame containing only highway-related accidents
df_highway_only = df_original[df_original['highway'] == True]

# Save the filtered data to CSV (optional)
df_highway_only.to_csv("Filtered_Highway_Accidents.csv", index=False)

# Preview the result
print(f"✅ Rows with highway mentions: {df_highway_only.shape[0]}")
print(df_highway_only[['ID', 'Description', 'highway']].head())

import re

# Use non-capturing groups to avoid warning
highway_pattern = r'\b(?:I[-\s]?\d+|US[-\s]?\d+|Hwy|HWY|highway)\b'

# Add 'highway' column with True/False values based on Description content
df_original['highway'] = df_original['Description'].str.contains(highway_pattern, flags=re.IGNORECASE, na=False)

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# === Step 1: Load your dataset ===
df = pd.read_csv("US_Accidents_With_Highway_Flag.csv")

# === Step 2: Define features and target ===
features = [
    "Temperature(F)", "Humidity(%)", "Wind_Speed(mph)",
    "Pressure(in)", "Precipitation(in)", "Visibility(mi)", "highway"
]

# Drop rows with missing values in selected columns
df = df[["Severity"] + features].dropna()
df["highway"] = df["highway"].astype(int)

# Binary classification target: 0 = Low (1–2), 1 = High (3–4)
df["Severity_Binary"] = df["Severity"].apply(lambda x: 0 if x <= 2 else 1)

X = df[features]
y = df["Severity_Binary"]

# === Step 3: Scale numeric features ===
scaler = StandardScaler()
X_scaled = X.copy()
X_scaled[features[:-1]] = scaler.fit_transform(X_scaled[features[:-1]])

# === Step 4: Train-test split ===
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, stratify=y, random_state=42
)

# === Step 5: Train Random Forest with class balancing ===
rf_model = RandomForestClassifier(
    n_estimators=100, class_weight='balanced', random_state=42
)
rf_model.fit(X_train, y_train)

# === Step 6: Predict and evaluate ===
y_pred = rf_model.predict(X_test)

# Print classification report
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred, target_names=["Low Severity", "High Severity"]))

# Show confusion matrix
ConfusionMatrixDisplay.from_estimator(rf_model, X_test, y_test, cmap="Blues")
plt.title("Random Forest - Confusion Matrix")
plt.show()

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.utils import resample
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# === Load dataset ===
df = pd.read_csv("US_Accidents_With_Highway_Flag.csv")

# === Define features and target ===
features = [
    "Temperature(F)", "Humidity(%)", "Wind_Speed(mph)",
    "Pressure(in)", "Precipitation(in)", "Visibility(mi)", "highway"
]

df = df[["Severity"] + features].dropna()
df["highway"] = df["highway"].astype(int)
df["Severity_Binary"] = df["Severity"].apply(lambda x: 0 if x <= 2 else 1)

# === Split first, then balance ===
X = df[features]
y = df["Severity_Binary"]

X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)

# === Combine and balance training data (undersampling) ===
train_df = pd.concat([X_train, y_train], axis=1)
majority = train_df[train_df["Severity_Binary"] == 0]
minority = train_df[train_df["Severity_Binary"] == 1]
majority_downsampled = resample(majority, replace=False, n_samples=len(minority), random_state=42)
train_balanced = pd.concat([majority_downsampled, minority])

# === Balance the test set similarly ===
test_df = pd.concat([X_test, y_test], axis=1)
majority_test = test_df[test_df["Severity_Binary"] == 0]
minority_test = test_df[test_df["Severity_Binary"] == 1]
majority_test_down = resample(majority_test, replace=False, n_samples=len(minority_test), random_state=42)
test_balanced = pd.concat([majority_test_down, minority_test])

# === Scale and split X/y ===
scaler = StandardScaler()
X_train_bal = scaler.fit_transform(train_balanced[features])
y_train_bal = train_balanced["Severity_Binary"]
X_test_bal = scaler.transform(test_balanced[features])
y_test_bal = test_balanced["Severity_Binary"]

# === Train Random Forest ===
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train_bal, y_train_bal)

# === Evaluate ===
y_pred = rf.predict(X_test_bal)

print("Classification Report (Balanced Train & Test):\n")
print(classification_report(y_test_bal, y_pred, target_names=["Low", "High"]))

ConfusionMatrixDisplay.from_estimator(rf, X_test_bal, y_test_bal, cmap="Blues")
plt.title("Random Forest - Balanced Train/Test")
plt.show()

# === Feature Importance Bar Plot ===
importances = rf.feature_importances_
feature_names = features

feat_df = pd.DataFrame({"Feature": feature_names, "Importance": importances})
feat_df = feat_df.sort_values(by="Importance", ascending=True)

feat_df.plot(kind="barh", x="Feature", y="Importance", legend=False, color="skyblue")
plt.title("Feature Importance (Random Forest)")
plt.xlabel("Importance Score")
plt.tight_layout()
plt.show()

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# === Feature importance data (assuming you've already trained your model) ===
importances = rf.feature_importances_
feature_names = features

feat_df = pd.DataFrame({"Feature": feature_names, "Importance": importances})
feat_df = feat_df.sort_values(by="Importance", ascending=True)

# === Generate color palette based on number of features ===
colors = sns.color_palette("coolwarm", len(feat_df))

# === Plot feature importance with custom colors ===
plt.figure(figsize=(8, 5))
plt.barh(feat_df["Feature"], feat_df["Importance"], color=colors)
plt.title("Feature Importance (Random Forest)")
plt.xlabel("Importance Score")
plt.tight_layout()
plt.show()

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.utils import resample
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# === Load dataset ===
df = pd.read_csv("US_Accidents_With_Highway_Flag.csv")

# === Define features and target ===
features = [
    "Temperature(F)", "Humidity(%)", "Wind_Speed(mph)",
    "Pressure(in)", "Precipitation(in)", "Visibility(mi)", "highway"
]

df = df[["Severity"] + features].dropna()
df["highway"] = df["highway"].astype(int)
df["Severity_Binary"] = df["Severity"].apply(lambda x: 0 if x <= 2 else 1)

# === Split first, then balance ===
X = df[features]
y = df["Severity_Binary"]

X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)

# === Combine and balance training data (undersampling) ===
train_df = pd.concat([X_train, y_train], axis=1)

# Separate classes
majority = train_df[train_df["Severity_Binary"] == 0]
minority = train_df[train_df["Severity_Binary"] == 1]

# Undersample majority class to match minority
majority_downsampled = resample(majority, replace=False, n_samples=len(minority), random_state=42)
train_balanced = pd.concat([majority_downsampled, minority])

# === Balance the test set the same way ===
test_df = pd.concat([X_test, y_test], axis=1)
majority_test = test_df[test_df["Severity_Binary"] == 0]
minority_test = test_df[test_df["Severity_Binary"] == 1]
majority_test_down = resample(majority_test, replace=False, n_samples=len(minority_test), random_state=42)
test_balanced = pd.concat([majority_test_down, minority_test])

# === Scale and split X/y ===
scaler = StandardScaler()

X_train_bal = scaler.fit_transform(train_balanced[features])
y_train_bal = train_balanced["Severity_Binary"]

X_test_bal = scaler.transform(test_balanced[features])
y_test_bal = test_balanced["Severity_Binary"]

# === Train Random Forest ===
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train_bal, y_train_bal)

# === Evaluate ===
y_pred = rf.predict(X_test_bal)

print("Classification Report (Balanced Train & Test):\n")
print(classification_report(y_test_bal, y_pred, target_names=["Low", "High"]))

ConfusionMatrixDisplay.from_estimator(rf, X_test_bal, y_test_bal, cmap="Blues")
plt.title("Random Forest - Balanced Train/Test")
plt.show()

import pandas as pd
from scipy.stats import chi2_contingency

# Load the dataset
df = pd.read_csv("US_Accidents_With_Highway_Flag.csv")

# Define categorical/boolean columns (you can expand this list)
categorical_cols = [
    "Amenity", "Bump", "Crossing", "Junction",
    "No_Exit", "Railway", "Roundabout", "Station", "Stop",
    "Traffic_Calming", "Traffic_Signal", "Turning_Loop"
]

# Clean the data
df = df[["Severity"] + categorical_cols].dropna()
df["Severity_Binary"] = df["Severity"].apply(lambda x: 0 if x <= 2 else 1)

# Run chi-square tests
results = []

for col in categorical_cols:
    contingency = pd.crosstab(df[col], df["Severity_Binary"])
    chi2, p, dof, _ = chi2_contingency(contingency)
    results.append({
        "Feature": col,
        "Chi2 Stat": round(chi2, 2),
        "P-Value": round(p, 5)
    })

# Show results
chi2_df = pd.DataFrame(results).sort_values(by="P-Value")
print("\nChi-Square Test Results (Categorical vs Severity):\n")
print(chi2_df.to_string(index=False))

import pandas as pd
from sklearn.utils import resample
from scipy.stats import ttest_ind, f_oneway, pearsonr

# === Load your dataset ===
df = pd.read_csv("US_Accidents_With_Highway_Flag.csv")

# === Define numeric columns ===
numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
numeric_cols = [col for col in numeric_cols if col != "Severity"]

# === Drop missing values for selected numeric columns + Severity ===
df = df[["Severity"] + numeric_cols].dropna()

# === Binary group: Low (1–2) vs High (3–4) ===
df["Severity_Binary"] = df["Severity"].apply(lambda x: 0 if x <= 2 else 1)

# === Create a balanced small subset (undersample majority class) ===
low = df[df["Severity_Binary"] == 0]
high = df[df["Severity_Binary"] == 1]
sample_size = min(len(low), len(high), 10000)  # you can adjust 10000

low_sample = resample(low, replace=False, n_samples=sample_size, random_state=42)
high_sample = resample(high, replace=False, n_samples=sample_size, random_state=42)

df_balanced = pd.concat([low_sample, high_sample])

# === Add Severity Group for readability (for T-test) ===
df_balanced["Severity_Group"] = df_balanced["Severity"].apply(lambda x: "Low" if x <= 2 else "High")

# === Run statistical tests ===
results = []

for col in numeric_cols:
    group_low = df_balanced[df_balanced["Severity_Group"] == "Low"][col]
    group_high = df_balanced[df_balanced["Severity_Group"] == "High"][col]
    t_stat, t_pval = ttest_ind(group_low, group_high, equal_var=False)
    
    groups_anova = [df_balanced[df_balanced["Severity"] == s][col] for s in sorted(df_balanced["Severity"].unique())]
    a_stat, a_pval = f_oneway(*groups_anova)
    
    corr, corr_pval = pearsonr(df_balanced[col], df_balanced["Severity"])

    results.append({
        "Feature": col,
        "T-Test p-value": round(t_pval, 5),
        "ANOVA p-value": round(a_pval, 5),
        "Correlation (r)": round(corr, 3),
        "Correlation p-value": round(corr_pval, 5)
    })

# === Display results ===
results_df = pd.DataFrame(results)
print("\nStatistical Test Results (Balanced Subset):\n")
print(results_df.to_string(index=False))
