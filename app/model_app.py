
# =========================================================================================
# -----------------------------  MODEL_APP.PY FILE -----------------------------------------
# =========================================================================================




import streamlit as st
import pandas as pd
import numpy as np
import joblib
import pydeck as pdk

# =====================================================================================================
# Load model, lookup csv, labels and store in cache
# =====================================================================================================

@st.cache_resource
def load_assets():
    modelPipeline = joblib.load("finalModelJun26.joblib")
    labels = joblib.load("crowd_tier_bins.joblib") 
    lookup_df = pd.read_csv("park_lookup_data.csv")
    return modelPipeline, labels, lookup_df
modelPipeline, labels, lookup_df = load_assets()

st.title("National Park Crowd Predictor")



# =====================================================================================================
# Select Park & Month from user 
# =====================================================================================================
#user input as dropdown box
month_lbls = { 1:"Jan", 2:"Feb", 3:"Mar", 4:"Apr", 5:"May", 6:"Jun", 7:"Jul", 8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec"}
park_dict = lookup_df.drop_duplicates('UnitCode').set_index('UnitCode')['park_name'].to_dict()
park_list = sorted(list(park_dict.keys()))
selected_park = st.selectbox("Select a National Park:", park_list, format_func=lambda x: park_dict[x])
selected_month = st.selectbox("Choose Target Month:", list(month_lbls.keys()), format_func=lambda x: month_lbls[x])

#filters lookup csv to just the selected month - output is 63 rows (each park)
map_df = lookup_df[lookup_df['Month'] == selected_month].copy()

#formatting
rgb_colors = {0: [46, 204, 113, 200],  # Green (Low) + alpha opacity
              1: [241, 196, 15, 200],  # Yellow (Medium)
              2: [230, 126, 34, 200],  # Orange (High)
              3: [231, 76, 60, 200] }  # Red (Extreme)
tier_names = {0: "Low", 1: "Medium", 2: "High", 3: "Extreme"}



# =====================================================================================================
# Create function to create input features from user's selection
# =====================================================================================================

def run_pipeline(park_id, target_month, row_data):
    inputs = pd.DataFrame([{'UnitCode': park_id,
            'Month': target_month,
            'fire_count_lag_1': row_data['fire_count_lag_1'],
            'Baseline_Prediction': row_data['Baseline_Prediction'],
            'relative_visits_lag_12': row_data['relative_visits_lag_12'],
            'relative_visits_lag_1': row_data['relative_visits_lag_1'],
            'trend_score_lag_1': row_data['trend_score_lag_1'],
            'temp_mean_roll_mean_3': row_data['temp_mean_roll_mean_3'],
            'rain_roll_mean_3': row_data['rain_roll_mean_3'],
            'snow_roll_mean_3': row_data['snow_roll_mean_3'],
            'trend_velocity': row_data['trend_velocity'],
            'comfort_index': row_data['comfort_index'],
            'RecreationVisits': 0,'is_pandemic': 0, }]) 

    prediction = modelPipeline.predict(inputs)[0]
    probabilities = modelPipeline.predict_proba(inputs)[0]
    confidence_pct = round(max(probabilities)*100)
    return prediction, confidence_pct


#create predictions for each park of chosen month
pred_list, color_list, confidencelist = [], [], []
for idx, row in map_df.iterrows():
    prediction, confidence = run_pipeline(row['UnitCode'], selected_month, row)
    pred_list.append(prediction)
    color_list.append(rgb_colors.get(prediction)) #, "#95a5a6")) #if invalid entry, backup is grey color
    confidencelist.append(confidence)

#adds prediction and color to map df    
map_df['Predicted_Tier'] = pred_list
map_df['color'] = color_list
map_df['marker_size'] = map_df['UnitCode'].apply(lambda x: 95000 if x == selected_park else 35000)
map_df['Tier_Name'] = map_df['Predicted_Tier'].map(tier_names)
map_df['Confidence_Pct'] = confidencelist

# =====================================================================================================
#Load Dynamic Map
# =====================================================================================================
#plot dynamic map of each park in the predicted color
st.subheader(f"Dynamic National Park Map — {month_lbls[selected_month]} 2026")
layer = pdk.Layer("ScatterplotLayer",map_df,get_position=["longitude", "latitude"],  get_color="color", get_radius="marker_size", pickable=True, opacity=0.9)

#change starting viewpoint of map (centered on the chosen park)
selectedparkrow = map_df[map_df['UnitCode']== selected_park].iloc[0]
view_state = pdk.ViewState(latitude=selectedparkrow["latitude"],longitude=selectedparkrow["longitude"],zoom=4, pitch=0)

# add tooltip of other parks crowd level
st.pydeck_chart(pdk.Deck(layers=[layer],initial_view_state=view_state,map_style="", tooltip={"html": "<b>Park:</b> {park_name}<br/><b>Status Tier:</b> {Tier_Name}"}))

#Legend
st.write("Each dot depicts each parks crowd levels:")
st.write("🟢 Low &nbsp;&nbsp;&nbsp;&nbsp; 🟡 Medium &nbsp;&nbsp;&nbsp;&nbsp; 🟠 High &nbsp;&nbsp;&nbsp;&nbsp; 🔴 Extreme")


# =====================================================================================================
#Sidebar Deeper Diagnostics


with st.sidebar:
    #define specific park & month row of DF
    park_record = map_df[map_df['UnitCode'] == selected_park].iloc[0]
    park_tier = park_record['Predicted_Tier']
    tier_names = {0: "Low", 1: "Medium", 2: "High", 3: "Extreme"}
    current_tier = tier_names.get(park_tier, "Unknown")
    confidencenum = park_record['Confidence_Pct']

    #add colors for each tier
    if current_tier in ["Low"]:
        tier_color = "#00cc66"  # Green
    elif current_tier in ["High", "Extreme"]:
        tier_color = "#ff4b4b"  # Red
    else:
        tier_color = "#e67e22" #Yellow

    # Print prediction
    st.subheader('Predicted Crowd Level:')
    st.markdown(f"""<div <div style="font-size: 28px; font-weight: bold; color: {tier_color}; font-family: sans-serif;">
        {current_tier} Crowds </div>""", unsafe_allow_html=True)
    st.metric(label="Prediction Confidence", value=f"{confidencenum}%")

    #Print Historical Weather trends for that month/park
    st.subheader(f"""Historical Weather for {month_lbls[selected_month]} """)
    st.write(f"Average Rainfall (past 3 months): **{park_record['rain_roll_mean_3']:.1f} in**")
    st.write(f"Average Snowfall (past 3 months): **{park_record['snow_roll_mean_3']:.1f} in**")
    st.write(f"Estimated Max Temp: **{park_record['temp_max']:.0f}°F**")
    st.write(f"Estimated Min Temp: **{park_record['temp_min']:.0f}°F**")
    st.write(f"Estimated # Nearby Fires: **{park_record['firecountavg']:.0f}**")
    st.markdown("---")

    #if park is high or extreme give better months to travel
    st.subheader("Travel Optimization Engine")
    if park_tier >= 2: 
        st.error(f"⚠️ {selected_park} is projected to experience heavy congestion in {month_lbls[selected_month]}.")
        st.write("##### Better Times to Travel:")

        alternatives = []
        park_annual_profile = lookup_df[lookup_df['UnitCode'] == selected_park]
        for m in range(1, 13):
            m_row = park_annual_profile[park_annual_profile['Month'] == m].iloc[0]
            m_pred,m_conf = run_pipeline(selected_park, m, m_row)
            if m_pred < 2 :
                alternatives.append((m, m_pred))
                
        if alternatives:
            for alt_month, alt_pred in alternatives:
                if alt_pred == 0:  # Low Crowds
                    st.success(f"👉 **{month_lbls[alt_month]}**: {tier_names[alt_pred]} Crowds")
                elif alt_pred == 1:  # Medium Crowds
                    st.warning(f"👉 **{month_lbls[alt_month]}**: {tier_names[alt_pred]} Crowds")
    
    #if park is low or medium
    else:
        st.success(f"✅ {month_lbls[selected_month]} is a wonderful choice for {selected_park}.")




