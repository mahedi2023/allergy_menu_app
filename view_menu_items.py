
import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase from secrets
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

st.set_page_config(layout="centered", page_title="📖 Menu Viewer")
st.title("📖 Menu Knowledge")

# Tab navigation
tabs = st.tabs(["FOOD", "COCKTAILS", "WINE"])

categories = ["FOOD", "COCKTAILS", "WINE"]

for i, category in enumerate(categories):
    with tabs[i]:
        ref = db.reference(f"menu_items/{category}")
        data = ref.get()

        if not data:
            st.info(f"No items added yet in {category}.")
        else:
            for item_id, item in data.items():
                st.markdown(f"### 🥣 {item.get('name', 'Unnamed Dish')}")
                st.markdown(f"**Description:** {item.get('description', '')}")

                if item.get("ingredients"):
                    st.markdown(f"**Ingredients:** {', '.join(item['ingredients'])}")

                if item.get("allergens"):
                    st.markdown(f"⚠️ **Allergens:** {', '.join(item['allergens'])}")

                if item.get("removable_allergens"):
                    st.markdown(f"✂️ **Removable Allergens:** {', '.join(item['removable_allergens'])}")

                if item.get("diet"):
                    st.markdown(f"🥗 **Diet Tags:** {', '.join(item['diet'])}")

                if item.get("markings"):
                    st.markdown(f"🍴 **Markings:** {', '.join(item['markings'])}")

                st.markdown("---")
