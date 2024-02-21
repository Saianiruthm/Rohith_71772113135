import pandas as pd
import random

# Load the CSV file
df = pd.read_csv("recipes.csv", usecols=['Unnamed: 0', 'recipe_name', 'ingredients', 'cuisine_path'])

# Rename the columns for clarity
df.columns = ['ID', 'Recipe Name', 'Ingredients', 'Cuisine Path']

# Split values into separate columns using "|" as the separator
split_df = df['Cuisine Path'].apply(lambda x: pd.Series(x.split('/')))

# Rename columns if needed
split_df.columns = [f'Cuisine Path_{i}' for i in range(split_df.shape[1])]

# Concatenate the split DataFrame with the original DataFrame
df = pd.concat([df, split_df], axis=1)
# Drop the original column
df.drop('Cuisine Path', axis=1, inplace=True)

# Display the DataFrame
#print(df.head())


# Sample menu
menu = [
"Mulligatawny Soup","Sauteed Apples","Homemade Apple Cider","Canned Apple Pie Filling","Easy Apple Pie","Apple Crumb Pie","Caramel Apples","German Apple Cake","Awesome Sausage","Apple and Cranberry Stuffing","Apple Hand Pies","Amazing Apple Butter","Easy Apple Cinnamon Muffins","Debbie's Amazing Apple Bread","Mom's Apple Fritters","Easy Apple Crisp with Pie Filling","Apple Strudel Muffins","Delicious Cinnamon Baked Apples"
]

# Function to identify cuisine and diet
def identify_cuisine_diet(menu, food_df):
    cuisine_dict = {}
    for item in menu:
        row = food_df.loc[food_df['Recipe Name'] == item]
        if not row.empty:
            cuisine = row['Cuisine Path_1'].values[0]
            ingredients = row['Ingredients'].values[0]
            is_vegetarian = all(ingredient.lower() != 'chicken' and ingredient.lower() != 'beef' for ingredient in ingredients.split(', '))
            if cuisine not in cuisine_dict:
                cuisine_dict[cuisine] = {"vegetarian": [], "non-vegetarian": []}
            if is_vegetarian:
                cuisine_dict[cuisine]["vegetarian"].append(item)
            else:
                cuisine_dict[cuisine]["non-vegetarian"].append(item)
    return cuisine_dict

def generate_kitchen_description_auto_main_cuisine_random(cuisine_dict):
    main_cuisine = max(cuisine_dict, key=lambda x: sum(len(v) for v in cuisine_dict[x].values()))
    main_cuisine_items = cuisine_dict[main_cuisine]
    
    # Define multiple templates
    templates = [
            f"This {main_cuisine} kitchen offers a variety of dishes including ",
            f"Discover the essence of {main_cuisine} cuisine with dishes like ",
            f"Taste the authenticity of {main_cuisine} cuisine through dishes like ",
            f"Explore the flavors of {main_cuisine} cuisine with dishes such as ",
            f"Enjoy a selection of {main_cuisine} delicacies including ",
            f"Indulge in the flavors of {main_cuisine} cuisine with dishes like ",
            f"Experience the traditional flavors of {main_cuisine} cuisine with dishes like ",
            f"Savor the taste of {main_cuisine} cuisine with dishes like ",
            f"Delight in the culinary heritage of {main_cuisine} cuisine with dishes like ",
            f"Immerse yourself in the flavors of {main_cuisine} cuisine with dishes like ",
            f"Satisfy your cravings with {main_cuisine} cuisine and dishes like ",
            f"Enjoy the authentic taste of {main_cuisine} cuisine with dishes like ",
            f"Get a taste of {main_cuisine} cuisine with dishes like ",
            f"Embark on a culinary journey with {main_cuisine} cuisine and dishes like ",
            f"Sample the delights of {main_cuisine} cuisine with dishes like ",
            f"Indulge in the rich flavors of {main_cuisine} cuisine with dishes like ",
            f"Experience the culinary traditions of {main_cuisine} cuisine with dishes like ",
            f"Enjoy the deliciousness of {main_cuisine} cuisine with dishes like ",
            f"Discover the rich flavors of {main_cuisine} cuisine with dishes like ",
            f"Savor the culinary creations of {main_cuisine} cuisine with dishes like ",
            f"Relish the authentic taste of {main_cuisine} cuisine with dishes like ",
            f"Experience the exquisite taste of {main_cuisine} cuisine with dishes like ",
            f"Treat yourself to the delights of {main_cuisine} cuisine with dishes like ",
            f"Indulge your palate with {main_cuisine} cuisine and dishes like ",
            f"Discover the mouthwatering flavors of {main_cuisine} cuisine with dishes like ",
            f"Savor the delectable taste of {main_cuisine} cuisine with dishes like "
        ]
    
    # Randomly choose a template
    description_template = random.choice(templates)
    
    # Generate description using the selected template
    dish_types = []
    for type, items_list in main_cuisine_items.items():
        if type != 'cuisine':
            dish_types.extend(items_list)
    if dish_types:
        description = description_template + ", ".join(dish_types[:2]) if len(dish_types) > 1 else dish_types[0]
        if len(dish_types) > 2:
            description += f", and {len(dish_types) - 2} more."
    else:
        description = description_template + "no specific dishes."
    return description

