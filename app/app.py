
# =========================================================================================
# ---------------------------------  APP.PY FILE -----------------------------------------
# =========================================================================================

import streamlit as st
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import numpy as np
import joblib
import pydeck as pdk

# =========================================================================================
# Paste custom transformers

class ParkSeasonalImputer(BaseEstimator, TransformerMixin):
    def __init__(self, columns):
        self.columns = columns
        self.park_col = 'UnitCode'
        self.month_col = 'Month'
    def fit(self, X, y=None):
        X = X.copy()
        self.global_means = X[self.columns].mean()            #for fallback impuatation
        self.lookup = {}                                      #create dictionary
        for col in self.columns:                              #compute park/month avg 
            self.lookup[col] = (X.groupby([self.park_col, self.month_col])[col]
                                .mean())
        return self
    def transform(self, X):
        for col in self.columns:
            X = X.merge(self.lookup[col].rename(col + "_imp"),
                    left_on=[self.park_col, self.month_col], right_index=True, how="left")
            X[col] = X[col].fillna(X[col + "_imp"])
            X = X.drop(columns=[col + "_imp"])
                # fallback global mean
            X[col] = X[col].fillna(self.global_means[col])
        return X
    def get_feature_names_out(self, input_features= None):
        return input_features

class UnitCodeTargetEncoder(BaseEstimator, TransformerMixin):
    def __init__(self,
                 unit_col='UnitCode',
                 visit_col='RecreationVisits',
                 output_col='UnitCodeTE'):
        self.unit_col = unit_col
        self.visit_col = visit_col
        self.output_col = output_col
    def fit(self, X, y=None):
        self.feature_names_in_ = X.columns
        self.global_median_ = X[self.visit_col].median()
        self.mapping_ = (X.groupby(self.unit_col)[self.visit_col].median())
        return self
    def transform(self, X):
        X = X.copy()
        X[self.output_col] = (X[self.unit_col].map(self.mapping_).fillna(self.global_median_) )
        return X
    def get_feature_names_out(self, input_features= None):
        if input_features is None:
            input_features=self.feature_names_in_
        features = list(input_features)
        if self.output_col not in features:
            features.append(self.output_col)
        return np.array(features)

class CyclicalMonthEncoder(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        X_out = pd.DataFrame(X).copy()
        X_out['Month_sin'] = np.sin(2 * np.pi * (X_out['Month'] - 1) / 12)
        X_out['Month_cos'] = np.cos(2 * np.pi * (X_out['Month'] - 1) / 12)
        return X_out.drop(columns='Month')
    def get_feature_names_out(self, input_features=None):
        return np.array(['Month_sin','Month_cos'])
    
class DropColumnsTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, columns):
        self.columns = columns
    def fit(self, X, y=None):
        # remember original columns
        self.feature_names_in_ = list(X.columns)
        return self
    def transform(self, X):
        X = X.copy()
        return X.drop(columns=self.columns, errors='ignore')
    def get_feature_names_out(self, input_features=None):
        if input_features is None:
            input_features = self.feature_names_in_
        output_features = [col for col in input_features if col not in self.columns ]
        return np.array(output_features)


# =========================================================================================
# Set global page configurations
st.set_page_config(page_title="Professional Portfolio & Predictor", layout="wide")

# 1. Define the pages pointing to your view files
bio_page = st.Page("bio.py", title="Homepage", icon="👤", default=True)
resume_page = st.Page("resume.py", title="Resume", icon="📄")
projects_page = st.Page("projects.py", title="Data Projects", icon="📂")
model_page = st.Page("model_app.py", title="National Park Crowd Predictor", icon="🌲")

# 2. Build the navigation routing system
nav = st.navigation({"Navigation": [bio_page, resume_page, projects_page,model_page] })

# 3. Execute the selected page routing
nav.run()