
import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
from collections import defaultdict, OrderedDict

# Initialize Firebase
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

# -------------------- TAB 1: ALLERGY SCANNER --------------------
with tab1:
    st.markdown("<h2 style='text-align:center;'>🍽️ Allergy Scanner</h2>", unsafe_allow_html=True)
    st.markdown(
        "<div style='background:#f9f9f9; padding:10px; text-align:center; font-size:18px; "
        "border-radius:10px; color:#333;'>💡 KNOWLEDGE IS MONEY</div>", unsafe_allow_html=True
    )

    ref = db.reference("menu_items")
    data = ref.get()
    all_dishes = []
    if data:
        for category, entries in data.items():
            for _, item in entries.items():
                item["category"] = category
                all_dishes.append(item)

    all_allergens = sorted({a for d in all_dishes for a in d.get("allergens", [])})
    selected_allergens = [a.lower() for a in st.multiselect("❌ Allergens to avoid:", all_allergens)]

    diet_tags = ["Vegetarian", "Vegan", "Halal", "Pescetarian"]
    selected_diet = [d.lower() for d in st.multiselect("🥗 Dietary preferences:", diet_tags)]

    safe_dishes = []
    modifiable_dishes = []
    rejected_dishes = []

    for dish in all_dishes:
        name = dish.get("name", "Unnamed")
        allergens = [a.lower() for a in dish.get("allergens", [])]
        removable = [a.lower() for a in dish.get("removable_allergens", [])]
        diet = [d.lower() for d in dish.get("diet", [])]
        category = dish.get("category", "Uncategorized")

        allergens_block = [a for a in selected_allergens if a in allergens and a not in removable]
        removable_ok = [a for a in selected_allergens if a in removable]
        diet_ok = all(d in diet for d in selected_diet)

        if not allergens_block and diet_ok:
            if removable_ok:
                modifiable_dishes.append((dish, removable_ok))
            else:
                safe_dishes.append(dish)
        else:
            rejected_dishes.append((dish, allergens_block, diet_ok))

    if selected_allergens or selected_diet:
        st.subheader("✅ Matching Dishes")
        if safe_dishes or modifiable_dishes:
            for d in safe_dishes:
                st.markdown(f"✅ **{d['name']}** - *{d.get('category', '')}*")
            for d, mods in modifiable_dishes:
                st.markdown(f"⚠️ **{d['name']}** (Can be made {', '.join([m + '-free' for m in mods])})")
        else:
            st.warning("No matching dishes found.")

        if st.checkbox("🧠 Show rejected dishes"):
            for d, blocked, ok in rejected_dishes:
                st.markdown(f"❌ **{d['name']}** — Blocked by: {blocked}, Diet OK: {ok}")
    else:
        st.info("Use filters to start scanning for safe dishes.")

# -------------------- TAB 2: MENU KNOWLEDGE --------------------
with tab2:
    st.title("📖 Menu Knowledge")
    menu_tabs = st.tabs(["FOOD", "COCKTAILS", "WINE"])
    categories = ["FOOD", "COCKTAILS", "WINE"]
    for i, category in enumerate(categories):
        with menu_tabs[i]:
            ref = db.reference(f"menu_items/{category}")
            data = ref.get()
            if not data:
                st.info(f"No items found in {category}")
            else:
                for item in data.values():
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

# -------------------- TAB 3: ADD NEW ITEM --------------------
with tab3:
    st.title("➕ Add New Item")
    category = st.radio("Select Category", ["FOOD", "COCKTAILS", "WINE"], horizontal=True)

    if category == "FOOD":
        name = st.text_input("Name")
        description = st.text_area("Description")
        allergens = st.multiselect("Allergens", all_allergens)
        removable = st.multiselect("Removable Allergens", allergens)
        diet = st.multiselect("Diet", diet_tags)
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

    elif category == "COCKTAILS":
        name = st.text_input("Cocktail Name")
        description = st.text_area("Description / Recipe")
        glassware = st.text_input("Glassware")
        garnish = st.text_input("Garnish")
        flavor = st.text_input("Flavor Notes (comma-separated)")
        if st.button("Save COCKTAIL"):
            db.reference("menu_items/COCKTAILS").push({
                "name": name,
                "description": description,
                "glassware": glassware,
                "garnish": garnish,
                "flavor": [f.strip() for f in flavor.split(",") if f]
            })
            st.success("✅ Cocktail saved.")

    elif category == "WINE":
        name = st.text_input("Wine Name")
        producer = st.text_input("Producer")
        grape = st.text_input("Grape Variety")
        region = st.text_input("Region")
        vintage = st.text_input("Vintage")
        notes = st.text_area("Notes")
        if st.button("Save WINE"):
            db.reference("menu_items/WINE").push({
                "name": name,
                "producer": producer,
                "grape": grape,
                "region": region,
                "vintage": vintage,
                "notes": notes
            })
            st.success("✅ Wine saved.")
