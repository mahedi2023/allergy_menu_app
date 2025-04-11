
import streamlit as st
import json
from collections import defaultdict, OrderedDict

# Load dish data
with open("processed_menu_dishes.json", "r") as f:
    dishes = json.load(f)

# Custom title for mobile
st.markdown("<h2 style='text-align:center; color:white; margin-top: 0;'>🍽️ Allergy Scanner</h2>", unsafe_allow_html=True)
st.markdown(
    """
    <div style='background-color: #f9f9f9; padding: 10px 15px; border-radius: 10px; 
         text-align: center; font-size: 20px; font-weight: bold; color: #333; 
         border: 1px solid #eee; margin-bottom: 15px;'>
        💡 KNOWLEDGE IS MONEY
    </div>
    """,
    unsafe_allow_html=True
)

category_order = OrderedDict([
    ("To Snack", "🧂 To Snack"),
    ("To Break", "🍳 To Break"),
    ("To Start", "🥗 To Start"),
    ("To Follow", "🍽️ To Follow"),
    ("To Share", "👫 To Share"),
    ("Dessert", "🍰 Dessert")
])

# Expanders for filters
with st.expander("🔻 Filter by Allergens"):
    all_allergens = sorted({a for dish in dishes for a in dish.get("allergens", [])})
    selected_allergens = st.multiselect("Select allergens to avoid:", all_allergens)

with st.expander("🔻 Filter by Dietary Preferences"):
    diet_tags = ["Vegetarian", "Pescetarian", "Halal", "Vegan"]
    selected_diet = st.multiselect("Select dietary preferences to follow:", diet_tags)

with st.expander("🧂 Filter by Required Ingredients"):
    all_ingredients = sorted({i for dish in dishes for i in dish.get("ingredients", [])})
    include_ingredients = st.multiselect("Must include ingredients:", all_ingredients)

# Filtering logic
safe_dishes = []
modifiable_dishes = []

for dish in dishes:
    allergens = dish.get("allergens", [])
    removable = dish.get("removable_allergens", [])
    diet = dish.get("diet", [])
    ingredients = dish.get("ingredients", [])

    allergens_block = [
        a for a in selected_allergens
        if any(a.lower() in x.lower() for x in allergens) and
           not any(a.lower() in r.lower() for r in removable)
    ]
    removable_ok = [
        a for a in selected_allergens
        if any(a.lower() in r.lower() for r in removable)
    ]
    diet_ok = all(d in diet for d in selected_diet)
    includes_ok = all(
        any(ing in i.lower() for i in ingredients) for ing in include_ingredients
    )

    if not allergens_block and diet_ok and includes_ok:
        if removable_ok:
            modifiable_dishes.append((dish, removable_ok))
        else:
            safe_dishes.append(dish)

# Group dishes
grouped_safe = defaultdict(list)
grouped_modifiable = defaultdict(list)
for dish in safe_dishes:
    cat = dish.get("category", "Uncategorized")
    grouped_safe[cat].append(f"✅ {dish['name']}")
for dish, mods in modifiable_dishes:
    cat = dish.get("category", "Uncategorized")
    grouped_modifiable[cat].append(f"⚠️ {dish['name']} *(Can be made {', '.join(m + '-free' for m in mods)})*")

# Output
if selected_allergens or selected_diet or include_ingredients:
    if include_ingredients and not selected_allergens and not selected_diet:
        st.subheader("🍽️ Dishes containing selected ingredients")
    else:
        st.subheader("✅ Safe Dishes by Menu Section")

    any_displayed = False
    for key, label in category_order.items():
        safe = grouped_safe.get(key, [])
        modifiable = grouped_modifiable.get(key, [])
        if safe or modifiable:
            st.markdown(f"### {label}")
            for name in safe:
                st.markdown(f"- {name}")
            for name in modifiable:
                st.markdown(f"- {name}")
            any_displayed = True
    if not any_displayed:
        st.warning("No matching dishes found based on your filters.")
else:
    st.info("Please select allergens, dietary preferences, or ingredients to filter menu options.")
