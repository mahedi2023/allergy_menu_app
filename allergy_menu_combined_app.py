
import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate({
        "type": "service_account",
        "project_id": st.secrets["project_id"],
        "private_key_id": st.secrets["private_key_id"],
        "private_key": st.secrets["private_key"].replace('\n', '\n'),
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

st.set_page_config(page_title="Allergy Scanner", layout="centered")

tab1, tab2, tab3 = st.tabs(["🧪 Allergy Scanner", "📖 Menu Knowledge", "➕ Add New Item"])

# --------------------- TAB 1: ALLERGY SCANNER ---------------------
with tab1:
    st.title("🧪 Allergy Scanner")

    ref = db.reference("menu_items")
    data = ref.get()

    all_dishes = []
    if data:
        for category, entries in data.items():
            for _, item in entries.items():
                item["category"] = category
                all_dishes.append(item)

    all_allergens = sorted(set(a for d in all_dishes for a in d.get("allergens", [])))
    selected_allergens = st.multiselect("Allergens to avoid", all_allergens)

    selected_diets = st.multiselect("Dietary preferences", ["Vegetarian", "Vegan", "Halal", "Pescetarian"])

    include_ingredients = st.text_input("🧂 Must include ingredients (comma-separated):")
    include_terms = [i.strip().lower() for i in include_ingredients.split(",") if i.strip()]

    if selected_allergens or selected_diets or include_terms:
        safe = []
        caution = []

        for dish in all_dishes:
            allergens = dish.get("allergens", [])
            removable = dish.get("removable_allergens", [])
            diet = dish.get("diet", [])
            ingredients = [i.lower() for i in dish.get("ingredients", [])]

            if all(d in diet for d in selected_diets) and all(term in ingredients for term in include_terms):
                if any(a in allergens for a in selected_allergens):
                    if any(a in removable for a in selected_allergens):
                        caution.append(dish)
                else:
                    safe.append(dish)

        from collections import defaultdict
        grouped = defaultdict(list)
        for d in safe:
            grouped[d["category"]].append("✅ " + d["name"])
        for d in caution:
            grouped[d["category"]].append("⚠️ " + d["name"])

        st.subheader("🍽️ Filtered Results by Section")
        for section in ["To Snack", "To Break", "To Start", "To Follow", "To Share", "Dessert"]:
            if section in grouped:
                st.markdown(f"### {section}")
                for item in grouped[section]:
                    st.markdown(f"- {item}")
    else:
        st.info("Please select filters above to begin scanning.")

# --------------------- TAB 2: MENU KNOWLEDGE ---------------------
with tab2:
    st.title("📖 Menu Knowledge")

    menu_tabs = st.tabs(["FOOD", "COCKTAILS", "WINE"])
    categories = ["FOOD", "COCKTAILS", "WINE"]

    for i, category in enumerate(categories):
        with menu_tabs[i]:
            ref = db.reference(f"menu_items/{category}")
            data = ref.get()

            if not data:
                st.info(f"No items in {category}")
            else:
                for item_id, item in data.items():
                    st.markdown(f"### 🍽️ {item.get('name', 'Unnamed')}")
                    st.markdown(f"**Description:** {item.get('description', '')}")
                    if item.get("ingredients"):
                        st.markdown(f"**Ingredients:** {', '.join(item['ingredients'])}")
                    if item.get("allergens"):
                        st.markdown(f"⚠️ Allergens: {', '.join(item['allergens'])}")
                    if item.get("removable_allergens"):
                        st.markdown(f"✂️ Removable Allergens: {', '.join(item['removable_allergens'])}")
                    if item.get("diet"):
                        st.markdown(f"🥗 Diet: {', '.join(item['diet'])}")
                    if item.get("markings"):
                        st.markdown(f"🍴 Markings: {', '.join(item['markings'])}")
                    st.markdown("---")

# --------------------- TAB 3: ADD NEW ITEM ---------------------
with tab3:
    st.title("➕ Add New Menu Item")

    category = st.radio("Category", ["FOOD", "COCKTAILS", "WINE"], horizontal=True)
    name = st.text_input("Dish Name")
    description = st.text_area("Dish Description")

    allergens = st.multiselect("Select Allergens", [
        "Alcohol", "Allium", "Avocado", "Cheese", "Chili", "Chocolate", "Cilantro", "Citrus", "Coconut", "Corn",
        "Dairy", "Egg", "Fish", "Gluten", "Honey", "Legume", "Mollusk", "Mushroom", "Mustard", "Nightshade", "Nut",
        "Pork", "Poultry", "Sechuan Button", "Seed", "Sesame", "Shellfish", "soy"
    ])
    removable = st.multiselect("Removable Allergens", allergens)

    diets = st.multiselect("Dietary Tags", ["Vegetarian", "Vegan", "Halal", "Pescetarian"])

    ingredients = st.text_input("Ingredients (comma-separated)")
    ingredient_list = [i.strip().capitalize() for i in ingredients.split(",") if i.strip()]

    markings = st.multiselect("Markings", ["App Fork", "App Knife", "Entrée Fork", "Entrée Knife", "Soup Spoon", "Dessert Spoon"])

    if st.button("💾 Save Dish"):
        if not name or not description:
            st.error("Please enter both a name and description.")
        else:
            db.reference(f"menu_items/{category}").push({
                "name": name,
                "description": description,
                "allergens": allergens,
                "removable_allergens": removable,
                "diet": diets,
                "ingredients": ingredient_list,
                "markings": markings
            })
            st.success(f"✅ '{name}' added to {category}")
