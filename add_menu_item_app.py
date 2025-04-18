
import streamlit as st


# NEW:
import pyrebase4 as pyrebase

from collections import OrderedDict

# Firebase setup
firebase_config = st.secrets["firebase"]
firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

st.set_page_config(layout="centered")
st.markdown("<h2 style='text-align:center; color:white; margin-top: 0;'>➕ Add New Menu Item</h2>", unsafe_allow_html=True)

# Step 1: Select Category
category = st.radio("Select Category", ["FOOD", "COCKTAILS", "WINE"], horizontal=True)

# Step 2: Basic Info
name = st.text_input("Dish Name")
description = st.text_area("Dish Description")
uploaded_image = st.file_uploader("Upload Image (optional)", type=["png", "jpg", "jpeg"])

# Step 3: Allergens
allergen_options = [
    "Alcohol", "Allium", "Avocado", "Cheese", "Chili", "Chocolate", "Cilantro", "Citrus", "Coconut", "Corn",
    "Dairy", "Egg", "Fish", "Gluten", "Honey", "Legume", "Mollusk", "Mushroom", "Mustard", "Nightshade", "Nut",
    "Pork", "Poultry", "Sechuan Button", "Seed", "Sesame", "Shellfish", "soy"
]
selected_allergens = st.multiselect("Select Allergens", allergen_options)

# Step 4: Removable Allergens
removable_allergens = st.multiselect("Select Removable Allergens (optional)", selected_allergens)

# Step 5: Dietary Tags
dietary_options = ["Vegetarian", "Vegan", "Halal", "Pescetarian"]
selected_diet = st.multiselect("Select Dietary Tags", dietary_options)

# Step 6: Ingredients
ingredient_input = st.text_input("List Ingredients (comma-separated)")
ingredient_list = [i.strip().capitalize() for i in ingredient_input.split(",") if i.strip()]

# Step 7: Markings
marking_options = ["App Fork", "App Knife", "Entrée Fork", "Entrée Knife", "Soup Spoon", "Dessert Spoon"]
selected_markings = st.multiselect("Select Markings", marking_options)

# Save
if st.button("💾 Save to Menu"):
    if not name or not description or not category:
        st.error("Please fill in required fields: Category, Name, Description.")
    else:
        new_dish = {
            "name": name,
            "description": description,
            "allergens": selected_allergens,
            "removable_allergens": removable_allergens,
            "diet": selected_diet,
            "ingredients": ingredient_list,
            "markings": selected_markings
        }
        db.child("menu_items").child(category).push(new_dish)
        st.success(f"✅ '{name}' added successfully under {category}!")
