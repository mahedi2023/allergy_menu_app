
import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
from collections import defaultdict

# Firebase setup
if not firebase_admin._apps:
    cred = credentials.Certificate({
        "type": st.secrets["type"],
        "project_id": st.secrets["project_id"],
        "private_key_id": st.secrets["private_key_id"],
        "private_key": st.secrets["private_key"],
        "client_email": st.secrets["client_email"],
        "client_id": st.secrets["client_id"],
        "auth_uri": st.secrets["auth_uri"],
        "token_uri": st.secrets["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["client_x509_cert_url"]
    })
    firebase_admin.initialize_app(cred, {
        "databaseURL": st.secrets["database_url"]
    })

st.set_page_config(page_title="Allergy Menu App", layout="wide")
tab1, tab2, tab3 = st.tabs(["🧪 Allergy Scanner", "📖 Menu Knowledge", "➕ Add New Item"])

with tab1:
    st.title("🧪 Allergy Scanner")
    ref = db.reference("menu_items")
    data = ref.get()

    if isinstance(data, dict):
        for item in data.values():
            if isinstance(item, dict):
                st.markdown(f"### 🍽️ {item.get('name', 'Unnamed')}")
                st.markdown(f"**Description:** {item.get('description', '')}")
                if item.get("ingredients"):
                    st.markdown(f"**Ingredients:** {', '.join(item['ingredients'])}")
                if item.get("allergens"):
                    st.markdown(f"⚠️ Allergens: {', '.join(item['allergens'])}")
                if item.get("removable_allergens"):
                    st.markdown(f"✂️ Removable: {', '.join(item['removable_allergens'])}")
                if item.get("diet"):
                    st.markdown(f"🥗 Diet: {', '.join(item['diet'])}")
                st.markdown("---")
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                st.markdown(f"### 🍽️ {item.get('name', 'Unnamed')}")
                st.markdown(f"**Description:** {item.get('description', '')}")
                if item.get("ingredients"):
                    st.markdown(f"**Ingredients:** {', '.join(item['ingredients'])}")
                if item.get("allergens"):
                    st.markdown(f"⚠️ Allergens: {', '.join(item['allergens'])}")
                if item.get("removable_allergens"):
                    st.markdown(f"✂️ Removable: {', '.join(item['removable_allergens'])}")
                if item.get("diet"):
                    st.markdown(f"🥗 Diet: {', '.join(item['diet'])}")
                st.markdown("---")
    else:
        st.warning("⚠️ Unexpected format. Must be a dictionary or list of menu items.")

            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        st.markdown(f"### 🍽️ {item.get('name', 'Unnamed')}")
                        st.markdown(f"**Description:** {item.get('description', '')}")
                        if item.get("ingredients"):
                            st.markdown(f"**Ingredients:** {', '.join(item['ingredients'])}")
                        if item.get("allergens"):
                            st.markdown(f"⚠️ Allergens: {', '.join(item['allergens'])}")
                        if item.get("removable_allergens"):
                            st.markdown(f"✂️ Removable: {', '.join(item['removable_allergens'])}")
                        if item.get("diet"):
                            st.markdown(f"🥗 Diet: {', '.join(item['diet'])}")
                        st.markdown("---")
            else:
                st.warning("⚠️ Unexpected format. Must be a dictionary or list of menu items.")

            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        st.markdown(f"### 🍽️ {item.get('name', 'Unnamed')}")
                        st.markdown(f"**Description:** {item.get('description', '')}")
                        if item.get("ingredients"):
                            st.markdown(f"**Ingredients:** {', '.join(item['ingredients'])}")
                        if item.get("allergens"):
                            st.markdown(f"⚠️ Allergens: {', '.join(item['allergens'])}")
                        if item.get("removable_allergens"):
                            st.markdown(f"✂️ Removable: {', '.join(item['removable_allergens'])}")
                        if item.get("diet"):
                            st.markdown(f"🥗 Diet: {', '.join(item['diet'])}")
                        st.markdown("---")
            else:
                st.warning(f"⚠️ Unexpected format for {category} menu items.")

            for item in data:
                    
                    
                    st.markdown(f"### 🍽️ {item.get('name', 'Unnamed')}")
                    st.markdown(f"**Description:** {item.get('description', '')}")
                    if item.get("ingredients"):
                        st.markdown(f"**Ingredients:** {', '.join(item['ingredients'])}")
                    if item.get("allergens"):
                        st.markdown(f"⚠️ Allergens: {', '.join(item['allergens'])}")
                    if item.get("removable_allergens"):
                        st.markdown(f"✂️ Removable: {', '.join(item['removable_allergens'])}")
                    if item.get("diet"):
                        st.markdown(f"🥗 Diet: {', '.join(item['diet'])}")
                    st.markdown("---")

with tab3:
    st.title("➕ Add New Item")
    category = st.radio("Select Category", ["FOOD", "COCKTAILS", "WINE"], horizontal=True)

    if category == "FOOD":
        name = st.text_input("Name")
        description = st.text_area("Description")
        allergens = st.multiselect("Allergens", [])
        removable = st.multiselect("Removable Allergens", allergens)
        diet = st.multiselect("Diet", ["Vegetarian", "Vegan", "Halal", "Pescetarian"])
        ingredients = st.text_area("Ingredients (comma-separated)")
        if st.button("Save FOOD"):
            db.reference("menu_items/FOOD").push({
                "name": name,
                "description": description,
                "allergens": allergens,
                "removable_allergens": removable,
                "diet": diet,
                "ingredients": [i.strip() for i in ingredients.split(",") if i]
            })
            st.success("✅ Food item saved.")
