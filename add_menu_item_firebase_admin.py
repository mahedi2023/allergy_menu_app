
import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import os
import json

# Load credentials from streamlit secrets (provided via .streamlit/secrets.toml)
if not firebase_admin._apps:
    cred = credentials.Certificate({
        "type": "service_account",
        "project_id": st.secrets["project_id"],
        "private_key_id": st.secrets["private_key_id"],
        "private_key": st.secrets["private_key"].replace('\\n', '\n'),
        "client_email": st.secrets["client_email"],
        "client_id": st.secrets["client_id"],
        "auth_uri": st.secrets["auth_uri"],
        "token_uri": st.secrets["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["client_x509_cert_url"]
    })
    firebase_admin.initialize_app(cred, {
        'databaseURL': st.secrets["database_url"]
    })

st.set_page_config(layout="centered")
st.markdown("<h2 style='text-align:center; color:white;'>➕ Add New Menu Item</h2>", unsafe_allow_html=True)

category = st.radio("Select Category", ["FOOD", "COCKTAILS", "WINE"], horizontal=True)

name = st.text_input("Dish Name")
description = st.text_area("Dish Description")
uploaded_image = st.file_uploader("Upload Image (optional)", type=["png", "jpg", "jpeg"])

allergen_options = [
    "Alcohol", "Allium", "Avocado", "Cheese", "Chili", "Chocolate", "Cilantro", "Citrus", "Coconut", "Corn",
    "Dairy", "Egg", "Fish", "Gluten", "Honey", "Legume", "Mollusk", "Mushroom", "Mustard", "Nightshade", "Nut",
    "Pork", "Poultry", "Sechuan Button", "Seed", "Sesame", "Shellfish", "soy"
]
selected_allergens = st.multiselect("Select Allergens", allergen_options)
removable_allergens = st.multiselect("Select Removable Allergens (optional)", selected_allergens)

dietary_options = ["Vegetarian", "Vegan", "Halal", "Pescetarian"]
selected_diet = st.multiselect("Select Dietary Tags", dietary_options)

ingredient_input = st.text_input("List Ingredients (comma-separated)")
ingredient_list = [i.strip().capitalize() for i in ingredient_input.split(",") if i.strip()]

marking_options = ["App Fork", "App Knife", "Entrée Fork", "Entrée Knife", "Soup Spoon", "Dessert Spoon"]
selected_markings = st.multiselect("Select Markings", marking_options)

if st.button("💾 Save to Menu"):
    if not name or not description:
        st.error("Please fill in required fields: Name and Description.")
    else:
        new_item = {
            "name": name,
            "description": description,
            "allergens": selected_allergens,
            "removable_allergens": removable_allergens,
            "diet": selected_diet,
            "ingredients": ingredient_list,
            "markings": selected_markings
        }

        ref = db.reference(f"menu_items/{category}")
        ref.push(new_item)
        st.success(f"✅ '{name}' added successfully under {category}!")
