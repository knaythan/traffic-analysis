
# U.S. Traffic Accident Analysis Dashboard

This is the official repository for **"Predictive Analytics for Safer Roads"**, a CS 163 final project by Shervan Shahparnia and Nathan Cohn. We analyze 7.7 million U.S. traffic accident records to identify risk factors, develop predictive models, and present our findings in an interactive web dashboard.

**Live Website**: [https://cs163-final-project.wl.r.appspot.com/home](https://cs163-final-project.wl.r.appspot.com/home)

---

## Project Overview

Our goal is to investigate how environmental, temporal, and road network conditions affect the **severity of traffic accidents**. We:
- Perform statistical testing and feature analysis
- Train machine learning models (Random Forests, Neural Networks)
- Visualize spatiotemporal patterns
- Deploy the results in an interactive Dash web application

---

## Data Source & Citation

Our data was collected from the following source:

[U.S. Accidents Dataset (Kaggle)](https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents)

This dataset was originally compiled and published by Sobhan Moosavi and collaborators. Please cite the following if using the dataset:

> Moosavi, Sobhan, Mohammad Hossein Samavatian, Srinivasan Parthasarathy, and Rajiv Ramnath. “A Countrywide Traffic Accident Dataset.”, 2019.

> Moosavi, Sobhan, Mohammad Hossein Samavatian, Srinivasan Parthasarathy, Radu Teodorescu, and Rajiv Ramnath. "Accident Risk Prediction based on Heterogeneous Sparse Data: New Dataset and Insights." In proceedings of the 27th ACM SIGSPATIAL International Conference on Advances in Geographic Information Systems, ACM, 2019.


## Setup Instructions

### Prerequisites
- Python 3.8+
- Google Cloud SDK (for deployment)
- Git installed

### Install Dependencies

Clone the repo and install required packages:

```bash
git clone https://github.com/your-username/traffic-analysis.git
cd traffic-analysis
python -m venv env
source env/bin/activate  # On Windows: .\env\Scripts\activate
pip install -r requirements.txt
```

### Run Locally

```bash
cd appengine/
python webapp.py
```

### Testing the Setup

To ensure the web application and model code run correctly:

1. Run `webapp.py` and confirm Dash loads on [http://127.0.0.1:8050](http://127.0.0.1:8050).
2. Open `model.py` and run it to test the model pipeline and view printed metrics.
3. Ensure your environment has access to BigQuery if fetching live data.

### Deploy to Google App Engine

```bash
gcloud app deploy
```

Make sure your Google Cloud project is set up and authenticated locally using:

```bash
gcloud auth login
gcloud config set project [YOUR_PROJECT_ID]
```

---

## Project Pipeline

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

## Pipeline Component Breakdown

Each stage of our pipeline is modular and purpose-built to support clear experimentation, fast iteration, and seamless deployment.

### 1. Data Collection
- **Source**: [U.S. Accidents Dataset on Kaggle](https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents)
- **Scope**: February 2016 – March 2023, 7.7M+ records
- **Automation**: Queried and filtered with BigQuery to ensure relevant, high-quality data for modeling

### 2. Data Cleaning & Feature Engineering
- **Structured Features**: Weather (temperature, humidity, visibility, wind, pressure), road network flags, rush hour indicators
- **Unstructured Features**: Accident descriptions processed using TF-IDF
- **Feature Engineering**:
  - Highway regex tagging (e.g., "I-80", "US-101")
  - One-hot encoding, normalization, and missing value handling

### 3. Statistical Testing
- **Tests Used**: Chi-squared tests, t-tests, Pearson correlations
- **Purpose**: Validate the significance of key features before modeling
- **Visuals**: Feature correlation heatmaps and severity-wise comparisons

### 4. Model Training & Evaluation
- **Baseline Model**: Random Forest Classifier for explainability and benchmarking
- **Advanced Model**: PyTorch Neural Network for multi-class classification
- **Data Configurations**: Both balanced and non-balanced versions tested
- **Evaluation**: Accuracy, confusion matrices, and feature importance plots

### 5. Visualization & Analysis
- **Libraries**: Plotly, Seaborn, Folium, Dash
- **Visualizations**:
  - Severity distribution charts
  - Temporal trends by hour and month
  - Heatmaps of national accident density
  - Feature importance comparisons
- **Widgets**: Precision-adjustable Folium maps for risk mapping

### 6. Web Dashboard Deployment
- **Frontend**: Modular layout using Dash components (`pages/`, `navbar.py`)
- **Backend**: Python with Dash callbacks and plotting logic (`visuals/`)
- **Hosting**: Google App Engine (`app.yaml` handles configuration)
- **Structure**: Four main pages — Home, Objectives, Methods, Findings — plus reusable assets and styles

---

## Repository Structure
```plaintext
traffic-analysis/
├── appengine/
│   ├── components/
│   │   └── navbar.py              # Reusable navigation bar across all pages
│   ├── assets/
│   │   └── Figure_1.png           # Non-Balanced Train/Test Confusion Matrix
│   │   ├── Figure_2.png           # Balanced Train/Test Confusion Matrix
│   │   └── Figure_4.png           # Feature Importance Random Forest
│   ├── pages/
│   │   ├── home.py                # Homepage content
│   │   ├── methods.py             # Methodology and data analysis workflow
│   │   ├── findings.py            # Main research findings and visualizations
│   │   └── objectives.py          # Project goals and broader impact
│   ├── styles/
│   │   └── styles.py              # Styling (colors, spacing, layout dicts)
│   ├── visuals/
│   │   └── analysis.py            # Plotly/Folium visualization functions
│   ├── webapp.py                  # Main Dash entry point
│   ├── requirements.txt          # Project dependencies
│   └── app.yaml                  # Google App Engine deployment config
│
├── model/
│   └── model.py                   # PyTorch + sklearn ML pipeline, feature extraction
│
└── data/                          # (Optional) Sample processed datasets
```

---

## Key Files

| File/Dir                       | Description |
|-------------------------------|-------------|
| `appengine/webapp.py`                   | Launches the Dash web app |
| `appengine/pages/`           | Pages: `home.py`, `methods.py`, `objectives.py`, `findings.py` |
| `appengine/visuals/analysis.py` | All Dash charts, maps, and visual logic |
| `model/model.py`              | ML models: TF-IDF + PyTorch NN, Random Forests, feature engineering |
| `requirements.txt`            | List of Python packages |
| `app.yaml`                    | App Engine configuration for deployment |
| `us_accidents.csv`            | Dataset from Kaggle renamed to "us_accidents.csv" | 

---

## Key Features

- **Hybrid Modeling Approach**: Combines structured features (weather, time, road) and unstructured text (accident descriptions) for prediction.
- **TF-IDF + PyTorch NN**: Uses TF-IDF for textual feature extraction and a custom PyTorch neural network for multiclass classification.
- **Random Forest Baseline**: Interpretable, traditional model used to rank feature importance and compare performance.
- **Statistical Validation**: Chi-squared tests, t-tests, and correlation heatmaps validate feature relevance before modeling.
- **Interactive Visualizations**: Includes bar charts, scatter plots, confusion matrices, and Folium-based geographic heatmaps.
- **Spatiotemporal Risk Mapping**: Enables exploration of severity by location and time with dynamic granularity controls.
- **Modular Dash Layout**: Each section of the site (Home, Objectives, Methods, Findings) is rendered via individual Dash pages.
- **Cloud Deployment**: Fully deployed to Google Cloud Platform using App Engine, with configuration managed by `app.yaml`.

---

## Authors

- **Shervan Shahparnia**  
- **Nathan Cohn**

---

## License

This project is for educational use as part of San José State University's CS 163 course.
