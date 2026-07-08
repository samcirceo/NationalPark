
# =========================================================================================
# ---------------------------------  BIO.PY FILE -----------------------------------------
# =========================================================================================


import streamlit as st
from PIL import Image


st.set_page_config(page_title="Samantha Circeo | Portfolio", layout="wide", page_icon="👤")

st.title("Samantha Circeo | Data Science Portfolio")
st.markdown("---")

col1, col2 = st.columns([2, 1], gap="large")

with col1:
    st.markdown("### Professional Overview")
    st.write(
        "Welcome! This portfolio brings together my background in engineering, my academic training in data science, "
        "and my passion for solving real-world problems. ")
    
    st.write(
        "I previously worked as a Research and Development Engineer at a textile manufacturing company and as a "
        "Technical Product Developer in the apparel industry. Through these roles, I developed a strong foundation in "
        "process optimization, product lifecycle development, and cross-functional collaboration.")
    
    st.write(
        "Driven to back my engineering instincts with advanced analytics, I recently graduated with my M.S. in Data Science "
        "from Eastern University. Here, I strengthened my technical skills in SQL, Python, R, machine learning, "
        "and data visualization, learning how to translate complex data into actionable insights.")

with col2:
    st.markdown("### Career Aspirations & Interests")
    st.markdown(
    """
    <div style="background-color: #eff5f9; padding: 16px; border-left: 4px solid #2e7d32; border-radius: 4px; font-family: sans-serif; color: #1e293b;">
        <p style="margin-top: 0; margin-bottom: 12px;"><strong>Where I'm Heading:</strong> I am looking to step into data science roles where data directly informs critical business decisions.</p>
        <p style="margin-bottom: 6px;"><strong>Core Areas of Interest:</strong></p>
        <ul style="margin-top: 0; margin-bottom: 0; padding-left: 20px;">
            <li style="margin-bottom: 4px;">Predictive Modeling & ML Pipelines</li>
            <li style="margin-bottom: 4px;">Operations & Process Automation</li>
            <li>Data Visualization</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

st.markdown("### Personal Introduction")

pic_col1, pic_col2 = st.columns([1, 2], gap="medium")

def resize_headshot(img_path):
    img = Image.open(img_path)
    return img.resize((270, 270))

with pic_col1:
    st.image(resize_headshot("images/headshot.png"), use_container_width=False)

with pic_col2:
    st.write("Outside of my career, I enjoy spending time outdoors recharging in nature through camping, hiking, & surfing. "
        "I especially enjoy exploring the beauty of U.S. National Parks. "
        "So far, I have visited 25 of the 63 U.S. National Parks! My love for these landscapes actually inspired my capstone project—a "
        "machine learning application designed to predict park crowd trends. You can check it out by clicking on the National Park Crowd Predictor "
        "page in the sidebar!")
    st.write(
        "When I am not out on the trails, you can usually find me experimenting with new recipes in the kitchen, tracking down the best local coffee shops and restaurants, and cheering on the Philadelphia Eagles during football season.")

# Bottom layout anchor
st.markdown("---")
st.caption("✨ Built entirely with Python and Streamlit. Explore the sidebar navigation to see my full Resume and active Data Projects.")