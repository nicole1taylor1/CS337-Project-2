import ourtypes.step
import ourtypes.ingredient

class Recipe:

    def __init__(self, name, info=None):
        #Recipe name
        self.name = name
        self.nutritional_info = info
        if info:
            if "Prep Time" in info:
                self.preptime = info["Prep Time"]
            if "Total Time" in info:
                self.totaltime = info["Total Time"]
            if "Servings" in info:
                self.servings = info["Servings"]
            if "Calories" in info:
                self.cals = info["Calories"]
            if "Fat" in info:
                self.fat = info["Fat"]
            if "Carbs" in info:
                self.carbs = info["Carbs"]
            if "Protein" in info:
                self.protein = info["Protein"]

    def add_nutritional_info(self, cals):
        self.cals = cals

    def add_ingredients(self, ingredients):
        self.ingredients = ingredients
    
    def add_steps(self, steps):
        self.steps = steps

    def print_nutritional_facts(self):
        s = ""
        if self.cals is not None:
            s += f"•  Calories: {self.cals}  \n\n"
        else:
            s += f"•  Calories: unavailable  \n\n"
        if self.fat is not None:
            s += f"•  Fat: {self.fat}  \n\n"
        else:
            s += f"•  Fat: unavailable  \n\n"
        if self.carbs is not None:
            s += f"•  Carbs: {self.carbs}  \n\n"
        else:
            s += f"•  Carbs: unavailable  \n\n"
        if self.protein is not None:
            s += f"•  Protein: {self.protein}  \n\n"
        else:
            s += f"•  Protein: unavailable  \n\n"
        
        return s

    def get_fact(self, key):
        if key in self.nutritional_info:
            return self.nutritional_info[key]
        else:
            return None

    def change_serving_size(self, amount):
        #update ingredients list
        for i in self.ingredients:
            i.change_serving_size(amount)
        #update servings
        original_servings = self.servings
        new_servings = float(original_servings) * amount
        self.servings = new_servings
        self.nutritional_info["Servings"] = new_servings
        return f"The recipe {self.name} has been adjusted by {amount} so that instead of making {original_servings} it will produce **{new_servings} servings**. \n\n"
    
        

