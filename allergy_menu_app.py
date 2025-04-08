import streamlit as st
from collections import defaultdict

# Full menu data with categories and dietary preferences
dishes = [
    {"name": "10-Minute Chocolate Chip Cookies", "category": "Dessert", "allergens": ["Dairy", "Egg", "Gluten", "Chocolate", "Corn"], "diet": ["Vegetarian"]},
    {"name": "Lemon Tart", "category": "Dessert", "allergens": ["Citrus", "Dairy", "Egg", "Gluten"], "diet": ["Vegetarian"]},
    {"name": "Chocolate Trifle", "category": "Dessert", "allergens": ["Gluten", "Dairy", "Egg", "Chocolate", "Chiles", "pork"], "diet": ["Vegetarian"]},
    {"name": "Banana Pudding", "category": "Dessert", "allergens": ["Canola Oil", "Dairy", "Egg", "HF Corn Syrup", "Palm Oil", "Soybean Oil", "Sugar"], "diet": ["Vegetarian"]},
    {"name": "The Egg", "category": "Dessert", "allergens": ["Citrus", "Dairy", "Egg", "Gluten", "Sugar", "Coconut"], "diet": ["Vegetarian"]},
    {"name": "Golden Snapper", "category": "To Follow", "allergens": ["Allium", "Dairy", "Nightshade", "Legume", "Pork"], "diet": ["Pescetarian", "Halal"]},
    {"name": "F.V. Ivy Rose Halibut en Croute", "category": "To Follow", "allergens": ["Allium", "Dairy", "Egg", "Fish", "Gluten", "Nuts"], "diet": ["Pescetarian"]},
    {"name": "Duroc Pork Chop", "category": "To Follow", "allergens": ["Allium", "Dairy", "Seeds", "Pork", "Legume", "Nightshade", "Citrus"], "diet": []},
    {"name": "Filet Mignon", "category": "To Follow", "allergens": ["Alcohol", "Allium", "Dairy", "Mushroom", "Pork", "Nightshade", "Poultry", "Vinegar"], "diet": ["Halal"]},
    {"name": "Pastrami Prime Hanger", "category": "To Follow", "allergens": ["Alcohol", "Allium", "Dairy", "Mustard", "Nightshade"], "diet": ["Halal"]},
    {"name": "Chicken Under a Brick", "category": "To Share", "allergens": ["Allium", "Citrus", "Dairy", "Nightshade"], "diet": ["Halal"]},
    {"name": "Creekstone Farms Tomahawk", "category": "To Share", "allergens": ["Allium", "Dairy"], "diet": ["Halal"]},
    {"name": "Carrot Glazed Carrot", "category": "To Share", "allergens": ["Citrus", "Corn", "Dairy", "Honey", "Poultry"], "diet": ["Vegetarian"]},
    {"name": "Sunchoked Spinach", "category": "To Share", "allergens": ["Allium", "Dairy"], "diet": ["Vegetarian"]},
    {"name": "Gougere", "category": "To Snack", "allergens": ["Allium", "Dairy", "Gluten", "Seeds", "Sesame"], "diet": ["Vegetarian"]},
    {"name": "Parker House Roll", "category": "To Snack", "allergens": ["Allium", "Dairy", "Gluten"], "diet": ["Vegetarian"]},
    {"name": "Jami's Sourdough", "category": "To Snack", "allergens": ["Dairy", "Gluten"], "diet": ["Vegetarian"]},
    {"name": "Shishitos", "category": "To Snack", "allergens": ["Citrus", "Gluten", "Nightshade"], "diet": ["Vegan"]},
    {"name": "Laotian Sushi", "category": "To Snack", "allergens": ["Allium", "Citrus", "Nightshade", "Seafood", "Seeds"], "diet": ["Pescetarian"]},
    {"name": "Smoking Hot Oysters", "category": "To Snack", "allergens": ["Allium", "Citrus", "Nightshade", "Shellfish", "Pork"], "diet": []},
    {"name": "Notkitori", "category": "To Snack", "allergens": ["Allium"], "diet": ["Vegan"]},
    {"name": "Tribeca Hot Chicken Wings", "category": "To Snack", "allergens": ["Allium", "Dairy", "Mustard", "Nightshade", "Seeds"], "diet": ["Halal"]},
    {"name": "Duck in a Jar", "category": "To Snack", "allergens": ["Alcohol", "Allium", "Dairy", "Gluten"], "diet": []},
    {"name": "Hiramasa for One", "category": "To Start", "allergens": ["Citrus", "Fish", "Gluten", "Honey", "Tree Nuts"], "diet": ["Pescetarian"]},
    {"name": "Barbecue Oysters", "category": "To Start", "allergens": ["Allium", "Dairy", "Gluten", "Nightshade", "Shellfish", "Pork"], "diet": []},
    {"name": "Greenmarket Roots", "category": "To Start", "allergens": ["Allium", "Dairy", "Gluten"], "diet": ["Vegetarian"]},
    {"name": "Montauk Tuna Etuvee", "category": "To Start", "allergens": ["Alcohol", "Allium", "Citrus", "Dairy", "Gluten", "Mollusk", "Mushroom", "Nightshade", "Pork", "Seafood"], "diet": []},
    {"name": "Foie Gras", "category": "To Start", "allergens": ["Alcohol", "Citrus", "Dairy", "Gluten"], "diet": []},
    {"name": "Beet Agnolotti del Plin", "category": "To Start", "allergens": ["Allium", "Dairy", "Egg", "Honey", "Gluten", "Nightshade", "Nuts", "Vinegar"], "diet": ["Vegetarian"]},
    {"name": "Little Shells", "category": "To Start", "allergens": ["Alcohol", "Allium", "Dairy", "Citrus", "Gluten", "Nightshade", "Pork", "Seeds", "Shellfish"], "diet": []},
    {"name": "Stroganoff", "category": "To Start", "allergens": ["Alcohol", "Allium", "Dairy", "Gluten", "Pink Peppercorn", "Mushroom", "Nightshade"], "diet": []},
    {"name": "Chili Lobster", "category": "To Start", "allergens": ["Allium", "Dairy", "Gluten", "Nightshade", "Shellfish"], "diet": ["Pescetarian"]}
]

st.title("🍽️ Allergy-Friendly Menu Scanner")

st.markdown("Select allergens to **exclude** from your search:")
all_allergens = sorted({a for item in dishes for a in item["allergens"]})
selected_allergens = st.multiselect("Allergens to avoid:", all_allergens)

st.markdown("Select dietary preferences to **include**:")
diet_tags = ["Vegetarian", "Vegan", "Halal", "Kosher", "Pescetarian"]
selected_diet = st.multiselect("Dietary restrictions to follow:", diet_tags)

# Filter the dishes
safe_dishes = [
    dish for dish in dishes
    if not any(allergen in dish["allergens"] for allergen in selected_allergens)
    and all(diet in dish["diet"] for diet in selected_diet)
]

# Group safe dishes by category
grouped_dishes = defaultdict(list)
for dish in safe_dishes:
    grouped_dishes[dish["category"]].append(dish["name"])

# Show results
if selected_allergens or selected_diet:
    st.subheader("✅ Safe Dishes by Menu Section")
    if grouped_dishes:
        for category in sorted(grouped_dishes.keys()):
            st.markdown(f"### 🍴 {category}")
            for name in grouped_dishes[category]:
                st.markdown(f"- {name}")
    else:
        st.warning("No safe dishes found based on your selections.")
else:
    st.info("Please select allergens or dietary preferences to filter menu options.")
