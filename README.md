
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
- Git installed

### 🗂️ Install Dependencies

Clone the repo and install required packages:

```bash
git clone https://github.com/your-username/traffic-analysis.git
cd traffic-analysis
python -m venv env
source env/bin/activate  # On Windows: .\env\Scripts\activate
pip install -r requirements.txt
```

### ▶️ Run Locally

```bash
python webapp.py
```

### 🧪 Testing the Setup

To ensure the web application and model code run correctly:

1. Run `webapp.py` and confirm Dash loads on [http://127.0.0.1:8050](http://127.0.0.1:8050).
2. Open `model.py` and run it to test the model pipeline and view printed metrics.
3. Ensure your environment has access to BigQuery if fetching live data.

### ☁️ Deploy to Google App Engine

```bash
gcloud app deploy
```

Make sure your Google Cloud project is set up and authenticated locally using:

```bash
gcloud auth login
gcloud config set project [YOUR_PROJECT_ID]
```

---

## 🔄 Project Pipeline

```
+-------------------------------+
|       Data Collection         |
+-------------------------------+
              ↓
+-------------------------------+
| Cleaning & Feature Engineering|
+-------------------------------+
              ↓
+-------------------------------+
|     Statistical Testing       |
+-------------------------------+
              ↓
+-------------------------------+
|   Model Training (ML, NN)     |
+-------------------------------+
              ↓
+-------------------------------+
| Evaluation & Visualization    |
+-------------------------------+
              ↓
+-------------------------------+
| Web Dashboard Deployment      |
+-------------------------------+
```

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
