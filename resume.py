

# =========================================================================================
# ---------------------------------  RESUME.PY FILE ----------------------------------------
# =========================================================================================

import streamlit as st
from PIL import Image

st.title("Professional Resume")


st.markdown("---")
st.subheader("Education")
st.write("**M.S. Data Science** — Eastern University (2024 - 2026)")
st.write("**B.S. Textile Engineering** — North Carolina State University (2014 - 2018)")

st.markdown("---")
st.subheader("Work Experience")
st.markdown("""
##### **Carbon2Cobalt** (2021 – 2024)

**Technical Product Developer** *(2023 – 2024)*
* Conducted data-driven seasonal return rate analysis to identify key drivers of returns and presented findings to stakeholders.
* Conducted analysis on customer demand and sizing, supporting expansion into extended size ranges.

**Jr. Technical Product Developer** *(2022 – 2023)*
* Maintained detailed product datasets ensuring data accuracy and consistency across teams and systems.
* Collaborated with cross-functional teams and external partners to ensure alignment on product requirements.

**Product Development Coordinator** *(2021 – 2022)*
* Partnered with manufacturing partners to resolve quality problems using data-informed problem solving.
""")

st.markdown("""
##### **Guilford Performance Textiles by Lear** (2018 – 2020)

**Research and Development Engineer** *(2019 – 2020)*
* Analyzed testing and production data to improve manufacturing processes and product quality.
* Optimized production efficiency through data-driven design improvements, generating $515K in annual savings.

**Process Engineer** *(2018 – 2019)*
* Conducted root cause analysis on production data, reducing scrap and saving $150K annually
* Built data-driven reports to monitor quality metrics and support continuous improvement
""")

st.markdown("""
##### **Technimark LLC** (2017)
**Quality Engineering Intern** *(2019 – 2020)*
* Completed my Six Sigma Green Belt certification focusing on reducing scrap leading to 60% cost reduction
""")

def load_and_resize(img_path):
    img = Image.open(img_path)
    return img.resize((500, 700))

st.subheader("Photos")

col1, col2 = st.columns(2)


with col1:
    st.image(load_and_resize("images/sb.jpg"), use_container_width=False,
    caption="The view from Carbon2Cobalt office in downtown Santa Barbara")

with col2:
    st.image(load_and_resize("images/fabric.png"), use_container_width=False,
    caption="Greige fabric going into a jet to be dyed at Guilford manufacturing mill")