from bs4 import BeautifulSoup
import requests

def read_recipe_from_url(url):
    """Will read a recipe from url using requests
    returns bs4 soup object
    """

    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup

def get_ingredients_from_soup(soup):
    ingredients = soup.find("div", {"id":"mntl-structured-ingredients_1-0"})
    #get entire list of ingredients 
    for child in ingredients.find_all("li"):
        text = child.text.replace("\n", "").strip()