import json
import pyrebase
import streamlit as st

# Load Firebase config (copy from your secrets.toml manually if not in Streamlit context)
firebase_config = {
    "apiKey": "AIzaSyBLIbfVIw47ymQbt1w1VH_czYG0M9LRGWw",
    "authDomain": "six-90963.firebaseapp.com",
    "databaseURL": "https://six-90963-default-rtdb.firebaseio.com",
    "projectId": "six-90963",
    "storageBucket": "six-90963.firebasestorage.app",
    "messagingSenderId": "284795024486",
    "appId": "1:284795024486:web:6a0a33425adfb9235869a7"
}

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

# Load your local dishes file
with open("processed_menu_dishes.json", "r") as f:
    dishes = json.load(f)

# Group dishes by category (FOOD, COCKTAILS, WINE)
firebase_data = {"FOOD": {}, "COCKTAILS": {}, "WINE": {}}

for dish in dishes:
    cat = dish.get("category", "").upper()
    if cat in firebase_data:
        firebase_data[cat][dish["name"]] = dish
    else:
        firebase_data["FOOD"][dish["name"]] = dish  # fallback to FOOD

# Upload to Firebase
for section, items in firebase_data.items():
    for name, dish in items.items():
        db.child("menu_items").child(section).push(dish)

print("✅ Upload complete! Your dishes are now in Firebase.")
