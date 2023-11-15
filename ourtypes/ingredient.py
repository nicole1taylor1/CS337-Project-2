
class Ingredient:
    """Ingredient Class
    ingredient name -> str
    quantity -> int/float 
    unit -> str (cup, teaspoon, pinch, etc.)
    descriptor -> str (optional, e.g. fresh, extra-virgin)
    preparation -> str (optional, e.g. chopped)
    """

    def __checktype__(self, var, typ):
        assert isinstance(var, typ), f"Field hould be type: {typ}, is {var}"
        if type == str:
            assert not var.isspace(), "Field cannot be whitespace"

    def __init__(self, ingredient_name, quantity, unit, descriptor=None, preparation=None):
        
        #set fields
        self.ingredient_name = ingredient_name
        self.quantity = quantity
        self.unit = unit
        self.description = descriptor 
        self.preparation = preparation
    
    def __str__(self):
        #probs need to adjust plurals
        if self.quantity != 1 and self.unit[-1] != "s":
            return f"{self.quantity} {self.unit}s of {self.ingredient_name}\n"
        else:
            return f"{self.quantity} {self.unit} of {self.ingredient_name}\n"

    


        


