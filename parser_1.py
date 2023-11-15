from bs4 import BeautifulSoup
import requests
import unicodedata

"""
Common keywords useful for parsing
"""
units = {"teaspoon": ["t", "tsp"],
"tablespoon": ["T", "tbl", "tbs", "tbsp"],
"ounce": ["oz", "ozs", "ounce"], 
"cup":["c", "C"],
"pint": ["p", "P", "pt"], 
"quart": ["q", "Q", "qt"],
"gallon": ["g", "G", "gal"],
"pinch": [""],
"sprinkle": [""],
"dash": [""]}

def read_recipe_from_url(url):
    """Will read a recipe from url using requests
    returns bs4 soup object
    """

    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup

def PluralUnit(word):
    if word[-1] == "s":
        return True, word[:-1]
    return False, word

def get_ingredients_from_soup(soup):
    ingredients = soup.find("div", {"id":"mntl-structured-ingredients_1-0"})
    for child in ingredients.find_all("li"):
        text = child.text.replace("\n", "").strip()
        text = text.split(" ")

        #get QUANTITY
        quantity = unicodedata.numeric(text[0]) #quantity = chars before first space

        #get UNIT
        unit = ""
        potential_unit = text[1].replace(".","")
        #lowercase unless one char
        if len(potential_unit) > 1:
            potential_unit = potential_unit.lower()
        #handle occurence of fluid/fl before unit name
        if potential_unit == "fluid" or potential_unit == "fl":
            unit += "fluid"
            potential_unit = text[2].lower().replace(".","")
        #check for units
        for key in units.keys():
            plural, potential_unit = PluralUnit(potential_unit)
            if potential_unit == key:
                unit += potential_unit
                if plural:
                    unit +="s"
            elif potential_unit in units[key]:
                unit += potential_unit
                if plural:
                    unit +="s"
        if unit == "":
            unit=None

        #get INGREDIENT NAME
        #need to check for plural foods

