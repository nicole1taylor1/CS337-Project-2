from bs4 import BeautifulSoup
import requests
import unicodedata
from ourtypes.ingredient import Ingredient
import foodlists

"""
Common keywords useful for parsing
"""


def read_recipe_from_url(url):
    """Will read a recipe from url using requests
    returns bs4 soup object
    """

    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup

def PluralUnit(word):
    if word[-1] == "s":
        return True, word[:-1], "s"
    return False, word, ""

def get_ingredients_from_soup(soup):
    ingredientsList = []
    ingredients = soup.find("div", {"id":"mntl-structured-ingredients_1-0"})
    for child in ingredients.find_all("li"):
        text = child.text.replace("\n", "").strip()
        text = text.split(" ")
        
        #get QUANTITY
        quantity = unicodedata.numeric(text[0]) #quantity = chars before first space

        #get UNIT
        unit = ""
        posn = 1
        potential_unit = text[1].replace(".","")
        #lowercase unless one char
        if len(potential_unit) > 1:
            potential_unit = potential_unit.lower()
        #handle occurence of fluid/fl before unit name
        if potential_unit == "fluid" or potential_unit == "fl":
            unit += "fluid"
            potential_unit = text[2].lower().replace(".","")
            posn += 1
        #check for units
        for key in foodlists.units.keys():
            plural, potential_unit, end = PluralUnit(potential_unit)
            if potential_unit == key:
                unit += potential_unit + end
            elif potential_unit in foodlists.units[key]:
                unit += key + end
        if unit == "":
            unit=None

        #get INGREDIENT NAME
        #check for plurals
        #just for now
        posn += 1
        name = " ".join(text[posn:])

        ingredient = Ingredient(ingredient_name=str(name), quantity=float(quantity), unit=str(unit))
        ingredientsList.append(ingredient)
    return ingredientsList
        


#run program
soup = read_recipe_from_url("https://www.allrecipes.com/recipe/255365/edible-cookie-dough/")
ingredients = get_ingredients_from_soup(soup)
for i in ingredients:
    print(i)