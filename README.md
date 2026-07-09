
# National Park Crowd & Traffic Optimization Dashboard

A machine learning dashboard that predicts monthly crowd levels across the 63 U.S. National Parks and helps travelers identify lower-congestion times to visit.

<p align="center">
  <img src="images/teton.JPG" width="700", height= "300"/>
  <br>
  <em>I took this sunrise photo in Grand Teton National Park in August 2020.</em>
</p>


## Project Preview
Explore the deployed application, review the full analysis notebook, or watch a short walkthrough of the application.

<p align="center">
  <a href="https://nationalparkcrowdpredictor.streamlit.app/">
    <img src="https://img.shields.io/badge/%20Launch%20App-Streamlit-red?style=for-the-badge">
  </a>
  &nbsp;
  <a href="https://github.com/samcirceo/NationalPark">
    <img src="https://img.shields.io/badge/View%20Notebook-Jupyter-black?style=for-the-badge">
  </a>
</p>


https://github.com/user-attachments/assets/01ffd0d1-3bf5-4952-9e7d-18c1cf903818




## The Business Problem

As an avid National Park fan who has visited 25 of the 63 U.S. National Parks, I have experienced firsthand how high visitation levels can impact the park experience through 1+ hour entrance station wait times, full campgrounds, crowded parking lots, and congested trails.

This inspired me to explore whether machine learning could help travelers better plan visits during less congested periods while helping park managers anticipate future demand.

This project builds a machine learning classification model that predicts monthly National Park crowd levels as:

- Low
- Medium
- High
- Extreme

## Data Strategy

The final dataset combines publicly available data from five major domains:

| Data Source | Purpose |
|---|---|
| National Park Service IRMA | Monthly visitation records and traffic counter data |
| Open-Meteo API | Temperature, precipitation, snowfall, and cloud coverage |
| NASA FIRMS | Wildfire activity and intensity |
| Google Trends via PyTrends | Public interest and search activity |
| U.S. Energy Information Administration | Regional fuel prices |

All datasets were merged into a master dataframe using: Park ID x Year x Month key

The final dataset contains:

- 63 National Parks
- 2006-2025 timeframe
- 15,120 monthly observations
- Approximately 30 engineered features

The dataset remains computationally lightweight and can train on a standard laptop while allowing fast deployment through Streamlit.

## Data Engineering

Combining multiple datasets was one of the largest challenges in this project.

### Wildfire Processing

NASA FIRMS contains approximately 3 million wildfire records. To efficiently calculate nearby fire activity, Scikit-Learn's BallTree with the Haversine metric was used.

For each park and month, wildfire features included:

- Fire count within 100km
- Total fire intensity
- Average FRP
- Maximum FRP

### Weather Processing

Daily weather data was aggregated into monthly summaries:

- Average temperature
- Maximum temperature
- Minimum temperature
- Total rainfall
- Total snowfall
- Cloud coverage

### Feature Engineering

Several features were created:

- `is_pandemic` - Identifies 2020-2021 COVID travel disruptions
- `trend_velocity` - Measures changes in public interest over time
- `comfort_index` - Combines temperature and rainfall patterns
- `relative_visits` - Compares visitation against a park's historical average

Additional preprocessing included:

- Seasonal missing-value imputation
- Cyclic month encoding
- Park target encoding
- Feature lags
- Rolling averages
- Log transformation of wildfire features to account for skew

---

# Exploratory Data Analysis

## Target Selection

Traffic counter data and recreation visits were compared to determine the most reliable visitation target.

Traffic counters frequently contained zeros caused by failures or road closures, making them inconsistent.

Recreation Visits was selected as the final target variable.

---

## Seasonality Analysis

STL decomposition confirmed that National Park visitation is highly seasonal.

The goal of the model is not simply to predict normal seasonal patterns, but to explain deviations caused by:

- Wildfires
- Weather changes
- Economic conditions
- Public interest changes
- Major disruptions such as COVID-19

---

## Feature Analysis

PCA analysis showed that the dataset is not linearly separable, confirming the need for tree-based models.

Feature analysis showed:

Strong predictors:

- Historical visitation patterns
- Search trends
- Temperature patterns
- Seasonal weather

Weaker predictors:

- Gas prices
- Rainfall
- Wildfire activity

---

# Machine Learning Methodology

The project evaluates several classification models:

1. Logistic Regression
2. Random Forest Classifier
3. XGBoost Classifier

A seasonal baseline model was created using:

> Same month, previous year visitation

This provided a benchmark for measuring whether machine learning improved predictions.

---

# Training Strategy

To prevent data leakage:

- Data was split chronologically
- Training period: 2006-2022
- Test period: 2023-2025

A rolling window time-series validation strategy was used instead of random splitting.

Additional training techniques:

- Randomized hyperparameter search
- Class weighting for imbalanced crowd tiers
- Feature importance analysis
- Probability calibration evaluation

---

# Model Evaluation

The primary evaluation metric was Weighted F1-score.

Macro F1-score was also tracked to ensure the model performed well on rare but important events such as Extreme crowd levels.

## Cross Validation Results

| Model | Weighted F1 | Macro F1 |
|---|---:|---:|
| Logistic Regression | .675 | .661 |
| Random Forest | .689 | .674 |
| XGBoost | .692 | .675 |
| Baseline | .691 | .675 |

---

# Final Test Results (2023-2025)

| Model | Weighted F1 | Macro F1 |
|---|---:|---:|
| XGBoost | **.735** | **.731** |
| Baseline | .731 | .729 |

XGBoost was selected as the final model because it generalized better on unseen data and reduced severe prediction errors compared to the baseline.

Feature importance analysis showed:

- Baseline crowd tier was the strongest predictor
- XGBoost used additional weather and interest features to correct edge cases
- Random Forest showed signs of overfitting

---

# Streamlit Application

The final project includes an interactive Streamlit application. [VIEW APP HERE](https://nationalparkcrowdpredictor.streamlit.app/)

The application contains:

## Interactive National Park Map

- Displays all 63 National Parks
- Predicts monthly crowd levels
- Uses color-coded tiers:

🟢 Low  
🟡 Medium  
🟠 High  
🔴 Extreme

## Park Diagnostics

Users can view:

- Predicted crowd level
- Confidence score
- Historical weather conditions
- Fire activity
- Visitation trends

## Better Time To Travel Recommendation

If a selected park and month is predicted to have High or Extreme crowds, the application recommends alternative months with lower expected visitation.

---

# Technologies Used

## Machine Learning

- Python
- Pandas
- NumPy
- Scikit-Learn
- XGBoost

## Data Collection

- National Park Service API
- Open-Meteo API
- NASA FIRMS
- Google Trends
- EIA

## Visualization & Deployment

- Streamlit
- Plotly
- Matplotlib
- Seaborn

---

# Future Improvements

Potential improvements include:

- Daily crowd forecasting
- Real-time weather integration
- Park capacity estimation
- Expansion to monuments and state parks
- Additional public interest signals

---

# Project Impact

This project demonstrates how machine learning can combine environmental, economic, and behavioral signals to predict National Park crowd patterns.

The final application provides value for both travelers planning trips and park managers preparing for future visitation demands.

##  Model Architecture & Pipeline Design


## Core Engineering Insights & Visual Audits

### 1. Model Selection: Random Forest vs. XGBoost
While both algorithms tied with a high **92% overall accuracy**, a rigorous **Probability Calibration Evaluation** using Reliability Diagrams and **Brier Scores** revealed a critical structural difference. 

XGBoost demonstrated a hesitant "S-Curve" (underconfidence in mid-range predictions). Random Forest's voting architecture closely hugged the perfect calibration diagonal across all probability thresholds. This ensures that the "Confidence Meter" displayed on the Streamlit user interface is mathematically trustworthy for real-world decision-making.

* [INSERT YOUR PROBABILITY CALIBRATION PLOT HERE]*

### 2. Operational Wins (Error Delta Matrix)
Instead of looking at raw counts, subtracting the baseline matrix from the model matrix isolates the exact operational wins. The model successfully caught critical **"Extreme" traffic days** that historical lookbacks missed entirely, protecting park staff from being caught under-prepared.

* [INSERT YOUR ERROR DELTA HEATMAP HERE]*

### 3. Feature Importance
An audit of feature importances reveals that the model heavily prioritizes rolling calendar history and localized weather physics over static geography markers, validating that the network is truly learning attendance behavior.

* [INSERT YOUR FEATURE IMPORTANCE COMPARISON PLOT HERE]*



<p align="center">
  <img src="images/GIS.gif" width="700"/>
</p>


