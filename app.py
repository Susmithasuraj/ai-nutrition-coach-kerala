import streamlit as st
import pandas as pd

st.set_page_config(page_title="Kerala Nutrition Coach", page_icon="🥥", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("database/foods.csv")

df = load_data()

st.title("🥥 AI Nutrition Coach for Keralites")
st.write("**Zeroth Phase MVP** - Personalized Kerala meal plans for weight loss, postpartum, thyroid, PCOS")

st.sidebar.header("📊 Your Details")
name = st.sidebar.text_input("Name", "Chechi")
age = st.sidebar.number_input("Age", 18, 80, 23)
weight = st.sidebar.number_input("Weight (kg)", 40.0, 150.0, 61.5)
height = st.sidebar.number_input("Height (cm)", 140, 200, 170)
gender = st.sidebar.selectbox("Gender", ["female", "male"])
goal = st.sidebar.selectbox("Goal", ["weight_loss", "muscle_gain", "postpartum", "thyroid", "maintenance"])
activity = st.sidebar.select_slider("Activity", ["Sedentary", "Light", "Moderate", "Active"], "Light")

if gender == "female":
    bmr = 10*weight + 6.25*height - 5*age - 161
else:
    bmr = 10*weight + 6.25*height - 5*age + 5

activity_map = {"Sedentary": 1.2, "Light": 1.375, "Moderate": 1.55, "Active": 1.725}
tdee = bmr * activity_map[activity]

if goal == "weight_loss":
    target_cal = tdee - 400
elif goal == "muscle_gain":
    target_cal = tdee + 300
elif goal == "postpartum":
    target_cal = tdee + 500
else:
    target_cal = tdee

col1, col2, col3 = st.columns(3)
col1.metric("BMR", f"{int(bmr)} kcal")
col2.metric("TDEE", f"{int(tdee)} kcal")
col3.metric("🎯 Daily Target", f"{int(target_cal)} kcal", f"{goal}")

if goal == "thyroid":
    st.warning("⚠️ **Thyroid Alert**: Raw cabbage, cauliflower, soya avoid cheyyuka. Cooked mathram.")
if goal == "postpartum":
    st.info("🤱 **BF Mode**: Extra 500 kcal added. Iron + Calcium rich foods: Meen Curry, Cheera Thoran, Payar.")

st.divider()
st.subheader(f"🍛 Recommended Kerala Foods for {goal.replace('_', ' ').title()}")
tag_map = {
    "weight_loss": "weight-loss|low-fat",
    "muscle_gain": "muscle-gain|protein",
    "postpartum": "postpartum|bf-friendly|iron",
    "thyroid": "thyroid-friendly",
    "maintenance": ""
}
if tag_map[goal]:
    filtered = df[df['tags'].str.contains(tag_map[goal], na=False, case=False)]
else:
    filtered = df

st.dataframe(filtered[['food_name', 'portion', 'calories', 'protein_g', 'tags']], use_container_width=True, height=400)
st.caption("Built in 1 Day 🚀 | Data: ICMR + Kerala Agri Uni")
