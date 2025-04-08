import streamlit as st

# Full menu data extracted from all PDFs
dishes = [
    {"name": "10-Minute Chocolate Chip Cookies", "allergens": ["Dairy", "Egg", "Gluten", "Sugar"]},
    {"name": "Lemon Tart", "allergens": ["Citrus", "Dairy", "Egg", "Gluten", "Sugar"]},
    {"name": "Samoas Marquise", "allergens": ["Alcohol", "Dairy", "Egg"]},
    {"name": "Banana Pudding", "allergens": ["Canola Oil", "Dairy", "Egg", "HF Corn Syrup", "Palm Oil", "Soybean Oil", "Sugar"]},
    {"name": "The Egg", "allergens": ["Citrus", "Dairy", "Egg", "Gluten", "Sugar"]},
    {"name": "Montauk Swordfish & Squash Curry", "allergens": ["Allium", "Coconut", "Fish", "Mushroom", "Shellfish"]},
    {"name": "F.V. Ivy Rose Halibut en Croute", "allergens": ["Allium", "Dairy", "Egg", "Fish", "Gluten", "Nuts"]},
    {"name": "Duroc Pork Chop", "allergens": ["Allium", "Dairy", "Mustard/Seeds", "Pork"]},
    {"name": "Prime NY Strip", "allergens": ["Alcohol", "Allium", "Dairy", "Egg", "Gluten", "Mustard", "Nightshade", "Poultry", "Sugar", "Vinegar"]},
    {"name": "Pastrami Prime Hanger", "allergens": ["Alcohol", "Allium", "Dairy", "Mustard", "Nightshade"]},
    {"name": "Chicken Under a Brick", "allergens": ["Allium", "Citrus", "Dairy", "Nightshade"]},
    {"name": "Creekstone Farms Tomahawk", "allergens": ["Allium", "Dairy"]},
    {"name": "Carrot Glazed Carrot", "allergens": ["Citrus", "Corn", "Dairy", "Honey", "Poultry"]},
    {"name": "Sunchoked Spinach", "allergens": ["Allium", "Dairy"]},
    {"name": "Gougere", "allergens": ["Allium", "Dairy", "Gluten", "Seeds", "Sesame"]},
    {"name": "Parker House Roll", "allergens": ["Allium", "Dairy", "Gluten"]},
    {"name": "Jami's Sourdough", "allergens": ["Dairy", "Gluten"]},
    {"name": "Shishitos", "allergens": ["Citrus", "Gluten", "Nightshade"]},
    {"name": "Laotian Sushi", "allergens": ["Allium", "Citrus", "Nightshade", "Seafood", "Seeds"]},
    {"name": "Smoking Hot Oysters", "allergens": ["Allium", "Citrus", "Nightshade", "Shellfish", "Pork"]},
    {"name": "Notkitori", "allergens": ["Allium"]},
    {"name": "Tribeca Hot Chicken Wings", "allergens": ["Allium", "Dairy", "Mustard", "Nightshade", "Seeds"]},
    {"name": "Duck in a Jar", "allergens": ["Alcohol", "Allium", "Dairy", "Gluten"]},
    {"name": "Hiramasa for One", "allergens": ["Citrus", "Fish", "Gluten", "Honey", "Tree Nuts"]},
    {"name": "Barbecue Oysters", "allergens": ["Allium", "Dairy", "Gluten", "Nightshade", "Shellfish", "Pork"]},
    {"name": "Greenmarket Roots", "allergens": ["Allium", "Dairy", "Gluten"]},
    {"name": "Montauk Tuna Etuvee", "allergens": ["Alcohol", "Allium", "Citrus", "Dairy", "Gluten", "Mollusk", "Mushroom", "Nightshade", "Pork", "Seafood"]},
    {"name": "Foie Gras", "allergens": ["Alcohol", "Citrus", "Dairy", "Gluten"]},
    {"name": "Beet Agnolotti del Plin", "allergens": ["Allium", "Dairy", "Egg", "Honey", "Gluten", "Nightshade", "Nuts", "Vinegar"]},
    {"name": "Little Shells", "allergens": ["Alcohol", "Allium", "Dairy", "Citrus", "Gluten", "Nightshade", "Pork", "Seeds", "Shellfish"]},
    {"name": "Duck Ragu", "allergens": ["Alcohol", "Allium", "Dairy", "Gluten", "Honey", "Mushroom", "Nightshade", "Stone Fruit"]},
    {"name": "Chili Lobster", "allergens": ["Allium", "Dairy", "Gluten", "Nightshade", "Shellfish"]}
]

st.title("🍽️ Allergy-Friendly Menu Scanner")
st.markdown("Select allergens to **exclude** from your search:")

# Build a set of all allergens
all_allergens = sorted({a for item in dishes for a in item["allergens"]})
selected_allergens = st.multiselect("Allergens to avoid:", all_allergens)

# Filter the dishes based on selected allergens
safe_dishes = [dish for dish in dishes if not any(allergen in dish["allergens"] for allergen in selected_allergens)]

# Show results
if selected_allergens:
    st.subheader("✅ Safe Dishes")
    if safe_dishes:
        for dish in safe_dishes:
            st.markdown(f"**{dish['name']}**")
    else:
        st.warning("No safe dishes found based on your selections.")
else:
    st.info("Please select allergens to filter menu options.")
