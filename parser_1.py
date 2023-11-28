from bs4 import BeautifulSoup
import requests
import unicodedata
from ourtypes.ingredient import Ingredient
import foodlists
import re

def check_url(url):
    """Checks validity of recipe given by user
    recipe should look like
    https://www.allrecipes.com/recipe/{recipe ID}/{recipe name}/
    """
    urlList = url.split("//")
    if urlList[0] != "https:":
        return 1, "Please type the url as: https://www.allrecipes.com/recipe/{recipe ID}/{recipe name}/"
    address = urlList[1].split("/")
    if urlList[0] != "www.allrecipes.com":
        return 1, "Hmmm... It doesn't seem like this is from AllRecipes\n \
            Please try typing it again or if you need inspo check here https://www.allrecipes.com/ \n"
    if (urlList[1] != "recipe"):
        return 1, "This doesn't appear to be a valid recipe from AllRecipes\n \
            The url should follow the format: https://www.allrecipes.com/recipe/{recipe ID}/{recipe name}/"
    if not urlList[2].isnumeric():
        return 1, "The recipe ID should consist only of digits.\n \
            The url should follow the format: https://www.allrecipes.com/recipe/{recipe ID}/{recipe name}/"
    #valid url!
    return 0, urlList[3]


    
    

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

def check_preparation_and_description(text):
    descriptors = []
    preps = []
    for word in text:
        if word in foodlists.preparations:
            preps.append(word)
        elif word in foodlists.descriptions:
            descriptors.append(word)
    return descriptors, preps

def parse_ingredient_name(text):
    tags = []
    unit_qualifier, name = "", text
    
    if ',' in text:
        unit_qualifier = text[text.find(','):]
        name = text[:text.find(',')]

    #check ingredients for helpful tagging
    for k in foodlists.allIngredients.keys():
        vals = foodlists.allIngredients[k]
        for val in vals:
            if val in text:
                tags.append(k)
                break

    if unit_qualifier != "" and unit_qualifier in foodlists.unit_qualifiers:
        return unit_qualifier, tags, name
    else:
        return None, tags, name
    
def get_ingredients_from_soup(soup):
    ingredientsList = []
    ingredients = soup.find("div", {"id":"mntl-structured-ingredients_1-0"})
    for child in ingredients.find_all("li"):
        text = child.text.replace("\n", "").strip()
        text = text.split(" ")
        
        #get QUANTITY
        quantity_unicode = text[0]
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
        name = text[posn:]
        map(lambda x: x.lower(), name)

        #get DESCRIPTION
        descriptors, preparation = check_preparation_and_description(name)
        for ele in descriptors:
            name.remove(ele)           

        #get PREPARATION
        for ele in preparation:
            name.remove(ele)

        name = " ".join(name)
        unit_qualifier, tags, name = parse_ingredient_name(name)

        ingredient = Ingredient(ingredient_name=str(name), quantity=float(quantity), quantity_unicode=quantity_unicode, 
                                unit=unit, descriptor=descriptors, preparation=preparation,
                                unit_qualifier=unit_qualifier, tags=tags)
        ingredientsList.append(ingredient)
    return ingredientsList


#run program
soup = read_recipe_from_url("https://www.allrecipes.com/recipe/255365/edible-cookie-dough/")
ingredients = get_ingredients_from_soup(soup)
for i in ingredients:
    print(i)
    print(i.tags)
    print("\n\n")