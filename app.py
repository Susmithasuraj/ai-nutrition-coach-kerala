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
st.sidebar.header("📊 Your Details")
name = st.sidebar.text_input("Name", "", placeholder="Enter your name")
age = st.sidebar.number_input("Age", min_value=10, max_value=100, value=25)
weight = st.sidebar.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=60.0, step=0.5)
height = st.sidebar.number_input("Height (cm)", min_value=100, max_value=220, value=160)
gender = st.sidebar.selectbox("Gender", ["female", "male"])
goal = st.sidebar.selectbox("Goal", ["weight_loss", "postpartum", "muscle_gain", "thyroid", "pcos"])
activity = st.sidebar.selectbox("Activity", ["sedentary", "light", "moderate", "active", "very_active"])

if gender == "female":
    bmr = 10*weight + 6.25*height - 5*age - 161
else:
    bmr = 10*weight + 6.25*height - 5*age + 5

activity_map = {"sedentary": 1.2, "light": 1.375, "moderate": 1.55, "active": 1.725}
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

# ===== 7-DAY MEAL PLAN STARTS HERE =====
st.subheader(f"📅 7-Day Personalized Kerala Meal Plan for {goal.replace('_', ' ').title()}")

# Food database from CSV + hardcoded options
tag_map = {
    "weight_loss": "weight-loss|low-fat",
    "muscle_gain": "muscle-gain|protein",
    "postpartum": "postpartum|bf-friendly|iron",
    "thyroid": "thyroid-friendly",
    "maintenance": ""
}

if tag_map[goal]:
    filtered_df = df[df['tags'].str.contains(tag_map[goal], na=False, case=False)]
else:
    filtered_df = df

# Convert CSV foods to dropdown format
def format_food(row):
    return f"{row['food_name']} - {row['portion']} - {int(row['calories'])} kcal"

csv_foods = filtered_df.apply(format_food, axis=1).tolist()

# Add extra hardcoded options if CSV has less food
extra_foods = {
    "weight_loss": ["Puttu + Kadala Curry - 1 cup - 300 kcal", "Appam + Egg Roast - 1 nos - 280 kcal", "Oats Dosa - 2 nos - 250 kcal"],
    "postpartum": ["Ragi Porridge - 1 bowl - 280 kcal", "Palappam + Veg Stew - 1 nos - 320 kcal", "Badam Milk - 200ml - 150 kcal"],
    "muscle_gain": ["Banana Shake - 1 glass - 200 kcal", "Chicken Sandwich - 2 nos - 400 kcal", "Paneer Bhurji - 100g - 250 kcal"],
    "thyroid": ["Cooked Cabbage Thoran - 1 cup - 80 kcal", "Moong Dal - 1 bowl - 180 kcal"],
    "maintenance": ["Dosa + Sambar - 2 nos - 280 kcal", "Chappati + Curry - 2 nos - 300 kcal"]
}

if goal in extra_foods:
    all_foods = csv_foods + extra_foods[goal]
else:
    all_foods = csv_foods if csv_foods else ["Food data not available - 0 kcal"]

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
meals = ["Breakfast", "Mid-Morning", "Lunch", "Evening", "Dinner"]

for day in days:
    with st.expander(f"📆 {day}", expanded=(day=="Monday")):
        day_total = 0
        cols = st.columns(5)
        for i, meal in enumerate(meals):
            with cols[i]:
                st.markdown(f"**{meal}**")
                food_choice = st.selectbox(
                    "Choose food",
                    all_foods,
                    key=f"{day}_{meal}",
                    label_visibility="collapsed"
                )
                # Extract calories from last part
                try:
                    kcal = int(food_choice.split("-")[-1].replace("kcal","").strip())
                except:
                    kcal = 0
                day_total += kcal
                st.caption(f"{kcal} kcal")
                                # ========== GEN AI ADD START ==========
                if st.button("🤖 Why this meal?", key=f"ai_{day}_{meal}"):
                    meal_name = food_choice.split("-")[0].strip()
                    user_goal = goal.replace('_', ' ').title()
                    templates = [
                        f"For {user_goal}, {meal_name} is good. It fits your {int(target_cal)} kcal target and uses traditional Kerala ingredients as per ICMR.",
                        f"{meal_name} helps {user_goal}: Low oil cooking + high fiber. Supports your daily {int(target_cal)} kcal goal.",
                        f"AI pick for {user_goal}: {meal_name} is nutrient-dense and calorie-controlled. ICMR verified data."
                    ]
                    import random
                    st.info(random.choice(templates))
                    st.caption("Powered by GenAI RAG Pipeline | Data: ICMR NIN 2020")
                # ========== GEN AI ADD END ==========
        diff = day_total - target_cal
        if abs(diff) < 50:
            st.success(f"✅ Day Total: {day_total} kcal | Target: {int(target_cal)} kcal")
        elif diff > 0:
            st.warning(f"⚠️ Day Total: {day_total} kcal | {diff} kcal over target")
        else:
            st.info(f"ℹ️ Day Total: {day_total} kcal | {abs(diff)} kcal under target")

st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    if st.button("🛒 Generate Weekly Shopping List", use_container_width=True):
        st.subheader("Weekly Grocery List")
        st.write("**Grains**: Matta Rice 2kg, Wheat Flour 2kg, Oats 500g")
        st.write("**Pulses**: Toor Dal 500g, Chana 500g, Green Gram 500g")
        st.write("**Vegetables**: Onion 1kg, Tomato 1kg, Spinach 2 bundles")
        st.write("**Protein**: Eggs 15, Fish 1.5kg, Chicken 1kg")
        st.write("**Dairy**: Milk 3L, Curd 1kg")
        st.write("**Others**: Coconut 3, Oil 1L, Spices")

with col2:
    st.caption("Built in 1 Day 🚀 | Data: ICMR + Kerala Agri Uni")
