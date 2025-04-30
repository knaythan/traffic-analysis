
# U.S. Traffic Accident Analysis Dashboard

This is the official repository for **"Predictive Analytics for Safer Roads"**, a CS 163 final project by Shervan Shahparnia and Nathan Cohn. We analyze 7.7 million U.S. traffic accident records to identify risk factors, develop predictive models, and present our findings in an interactive web dashboard.

🔗 **Live Website**: [https://cs163-final-project.wl.r.appspot.com/home](https://cs163-final-project.wl.r.appspot.com/home)

---

## 📌 Project Overview

Our goal is to investigate how environmental, temporal, and road network conditions affect the **severity of traffic accidents**. We:
- Perform statistical testing and feature analysis
- Train machine learning models (Random Forests, Neural Networks)
- Visualize spatiotemporal patterns
- Deploy the results in an interactive Dash web application

---

## ⚙️ Setup Instructions

### 🔧 Prerequisites
- Python 3.8+
- Google Cloud SDK (for deployment)
- `pip install -r requirements.txt`

### 🗂️ Install Dependencies
```bash
pip install -r requirements.txt
```

### ▶️ Run Locally
```bash
python webapp.py
```

### ☁️ Deploy to Google App Engine
```bash
gcloud app deploy
```

---

## 🔄 Project Pipeline

```mermaid
graph TD;
    A[Data Collection] --> B[Cleaning & Feature Engineering]
    B --> C[Statistical Testing]
    C --> D[Model Training (ML, NN)]
    D --> E[Evaluation & Visualization]
    E --> F[Web Dashboard Deployment]
```

### Step-by-Step:
1. **Data Collection**: Raw accident data from BigQuery (2016–2023).
2. **Cleaning & Engineering**: Preprocessing includes scaling, TF-IDF, one-hot encoding, and highway feature extraction.
3. **Statistical Testing**: T-tests, chi-squared, correlation to validate feature importance.
4. **Modeling**:
   - Binary classification (Low vs. High Severity) using Random Forest
   - 4-class prediction using a PyTorch Neural Network
5. **Visualization**: Interactive visualizations with Plotly and Folium
6. **Deployment**: Dash app hosted on Google App Engine

---

## 🗃️ Repository Structure

```plaintext
.
├── appengine/
│   ├── components/            # UI components (e.g. navbar)
│   ├── pages/                 # Dash pages: home, methods, findings, objectives
│   ├── styles/                # CSS styling in Python dicts
│   ├── visuals/               # All visualizations and analytics (plots, maps, charts)
│   └── assets/                # Static images or figures (if used)
│
├── model/                     # Machine learning models and evaluation logic
│   └── model.py               # Structured + unstructured feature modeling (PyTorch + sklearn)
│
├── webapp.py                  # Main Dash app entry point
├── requirements.txt           # Python dependencies
├── app.yaml                   # GCP deployment config
└── data/                      # (Optional) Raw and processed datasets (local use)
```

---

## 📁 Key Files

| File/Dir                       | Description |
|-------------------------------|-------------|
| `webapp.py`                   | Launches the Dash web app |
| `appengine/pages/`           | Pages: `home.py`, `methods.py`, `objectives.py`, `findings.py` |
| `appengine/visuals/analysis.py` | All Dash charts, maps, and visual logic |
| `model/model.py`              | ML models: TF-IDF + PyTorch NN, Random Forests, feature engineering |
| `requirements.txt`            | List of Python packages |
| `app.yaml`                    | App Engine configuration for deployment |

---

## 🔍 Key Features

- **ML & NLP**: Combines TF-IDF vectorization with structured feature scaling
- **Visualizations**: Folium maps, confusion matrices, bar charts, correlations
- **Balanced Training**: Downsampling used to address class imbalance
- **Spatiotemporal Risk Mapping**: Interactive severity risk map with zoom filtering
- **Fully Deployed**: Website live on Google Cloud

---

## 👨‍💻 Authors

- **Shervan Shahparnia**  
- **Nathan Cohn**

---

## 🏁 License

This project is for educational use as part of San José State University's CS 163 course.
