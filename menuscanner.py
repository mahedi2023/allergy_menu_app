
import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# Use secrets instead of hardcoding
if not firebase_admin._apps:
    cred = credentials.Certificate({
        "type": st.secrets["firebase"]["type"],
        "project_id": st.secrets["firebase"]["project_id"],
        "private_key_id": st.secrets["firebase"]["private_key_id"],
        "private_key": st.secrets["firebase"]["private_key"].replace('\\n', '\n'),
        "client_email": st.secrets["firebase"]["client_email"],
        "client_id": st.secrets["firebase"]["client_id"],
        "auth_uri": st.secrets["firebase"]["auth_uri"],
        "token_uri": st.secrets["firebase"]["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["firebase"]["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"]
    })
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://six-90963-default-rtdb.firebaseio.com/'
    })

st.set_page_config(page_title="Allergy Menu Manager", layout="centered")
st.title("📋 Allergy Menu Manager")

tabs = st.tabs(["🥘 Allergy Scanner", "📖 Menu Knowledge", "➕ Add New Item"])

with tabs[0]:
    st.subheader("🥘 Allergy Scanner")
    st.info("This tab will let you filter dishes by allergen, diet, or required ingredients (to be restored next).")

with tabs[1]:
    st.subheader("📖 Menu Knowledge")
    st.info("This will eventually show menu data pulled from Firebase in categories like FOOD, COCKTAILS, and WINE.")

with tabs[2]:
    st.header("➕ Add New Item")
    category = st.selectbox("Select category", ["FOOD", "COCKTAILS", "WINE"])

    if category == "FOOD":
        name = st.text_input("Dish Name")
        description = st.text_area("Description")
        allergens = st.multiselect("Allergens", ["Gluten", "Dairy", "Egg", "Nut", "Soy", "Shellfish", "Allium", "Nightshade", "Seed", "Pork", "Citrus", "Legume", "Mushroom", "Alcohol"])
        removable_allergens = st.multiselect("Removable Allergens", allergens)
        diet = st.multiselect("Dietary Tags", ["Vegetarian", "Pescetarian", "Halal", "Vegan"])
        ingredients = st.text_area("Ingredients (comma-separated)")
        markings = st.multiselect("Markings", ["App Fork", "App Knife", "Entrée Fork", "Entrée Knife", "Dessert Spoon", "Wine Glass", "Rocks Glass", "Highball", "Champagne Flute"])

        if st.button("💾 Save FOOD Item"):
            db.reference("menu_items/FOOD").push({
                "name": name,
                "description": description,
                "allergens": allergens,
                "removable_allergens": removable_allergens,
                "diet": diet,
                "ingredients": [i.strip().capitalize() for i in ingredients.split(",") if i],
                "markings": markings
            })
            st.success("✅ Food item saved successfully.")

    elif category == "COCKTAILS":
        name = st.text_input("Cocktail Name")
        description = st.text_area("Specifications / Recipe")
        glassware = st.text_input("Glassware")
        rocks = st.radio("Rocks", ["Yes", "No"], horizontal=True)
        garnish = st.text_input("Garnish")
        flavor = st.multiselect("Flavor", ["Sweet", "Bitter", "Sour", "Spicy", "Smoky"])
        aroma = st.multiselect("Aroma", ["Fragrant", "Tropical", "Spiced", "Woody", "Citrusy"])
        texture = st.multiselect("Texture / Mouthfeel", ["Smooth", "Fizzy", "Crisp", "Icy", "Frothy"])
        strength = st.multiselect("Strength / Body", ["Boozy", "Light-bodied", "Balanced", "Potent", "Delicate"])
        mood = st.multiselect("Mood / Style", ["Classic", "Modern", "Tiki", "Elegant", "Playful"])

        if st.button("💾 Save COCKTAIL"):
            db.reference("menu_items/COCKTAILS").push({
                "name": name,
                "description": description,
                "glassware": glassware,
                "rocks": rocks,
                "garnish": garnish,
                "flavor": flavor,
                "aroma": aroma,
                "texture": texture,
                "strength": strength,
                "mood": mood
            })
            st.success("✅ Cocktail saved successfully.")

    elif category == "WINE":
        producer = st.text_input("Producer Name")
        cuvee = st.text_input("Cuvée Name")
        grape = st.text_input("Grape Variety")
        vintage = st.text_input("Vintage")
        region = st.text_input("Region / Appellation")
        description = st.text_area("Wine Description")
        body = st.multiselect("Body", ["Light", "Medium", "Full", "Round", "Rich"])
        acidity = st.multiselect("Acidity", ["Soft", "Balanced", "Bright", "Crisp", "Zesty"])
        tannin = st.multiselect("Tannin", ["Low", "Silky", "Smooth", "Firm", "Grippy"])
        nose = st.multiselect("On the Nose", ["Fruity", "Floral", "Herbal", "Spicy", "Earthy"])
        palate = st.multiselect("On the Palate", ["Dry", "Juicy", "Velvety", "Lush", "Savory"])
        finish = st.multiselect("Finish", ["Clean", "Smooth", "Lingering", "Long", "Bold"])

        if st.button("💾 Save WINE"):
            db.reference("menu_items/WINE").push({
                "producer": producer,
                "cuvee": cuvee,
                "grape": grape,
                "vintage": vintage,
                "region": region,
                "description": description,
                "body": body,
                "acidity": acidity,
                "tannin": tannin,
                "nose": nose,
                "palate": palate,
                "finish": finish
            })
            st.success("✅ Wine saved successfully.")
