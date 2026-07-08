
# =========================================================================================
# -----------------------------  PROJECTS.PY FILE -----------------------------------------
# =========================================================================================

import streamlit as st

st.title("General Projects Portfolio")
st.info(" Note: Due to university policy, I cannot publicly share the code for some projects. If you'd like access, please reach out with your GitHub username or the email associated with your GitHub account, and I will grant access. You will then receive an invitation to the repository.")

from PIL import Image

def load_and_resize(img_path):
    img = Image.open(img_path)
    return img.resize((200, 100))


col1, col2 = st.columns(2)

with col1:
    st.image(load_and_resize("images/teton.JPG"), use_container_width=False)
    st.subheader("National Park Crowd Predictor")
    st.write("End to End ML models predicting crowd level at the 63 US National Parks.")
    st.page_link("app/model_app.py", label="Launch Live App", icon="🚀")

with col2:
    st.image(load_and_resize("images/mushroom.png"), use_container_width=False)
    st.subheader("Mushroom Classifier")
    st.write("CNN model using TensorFlow + PCA to classify mushrooms.")
    st.link_button("🌐 View Public GitHub Repo", "https://github.com/samcirceo/MushroomClassifierPUBLIC")

st.write("") 
st.write("") 

col3, col4 = st.columns(2)

with col3:
    st.image(load_and_resize("images/grades.jpeg"), use_container_width=False)
    st.subheader("Final Grade Predictor")
    st.write("ML models predicting student performance using Scikit-learn.")
    st.link_button("🌐 View Public GitHub Repo", "https://github.com/samcirceo/FinalGradePredictorPUBLIC")

with col4:
    st.image(load_and_resize("images/mentalhealth.jpeg"), use_container_width=False) # Replace with your image
    st.subheader("Mental Health Predictor")
    st.write("Regression analysis using R and visualization tools.")
    st.link_button("🌐 View Public Github Repo", "https://github.com/samcirceo/MentalHealthPredictorPUBLIC")