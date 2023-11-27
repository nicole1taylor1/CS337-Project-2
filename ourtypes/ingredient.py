from fractions import Fraction

class Ingredient:
    """Ingredient Class
    ingredient name -> str
    quantity -> int/float 
    unit -> str (cup, teaspoon, pinch, etc.)
    descriptor -> str (optional, e.g. fresh, extra-virgin) or list
    preparation -> str (optional, e.g. chopped) or list

    PRINTS: quanity unit (of) preparation description ingredient name
    """

    def __checktype__(self, var, typ):
        assert isinstance(var, typ), f"Field hould be type: {typ}, is {var}"
        if type == str:
            assert not var.isspace(), "Field cannot be whitespace"

    def __init__(self, ingredient_name, quantity, unit, quantity_unicode, descriptor, preparation, unit_qualifier, tags):
        
        #set fields
        self.ingredient_name = ingredient_name
        self.quantity = quantity
        self.unit = unit
        self.quantity_unicode = quantity_unicode
        self.description = descriptor
        self.preparation = preparation
        self.tags = tags
        if unit_qualifier != None:
            self.unit_qualifier = unit_qualifier
        else:
            self.unit_qualifier = ""

    def get_preparation(self):
        match len(self.preparation):
            case 0:
                return ""
            case 1:
                return f"{self.preparation[0]} "
            case 2:
                return f"{self.preparation[0]} and {self.preparation[1]} "
            case _:
                #preps = ', '.join(self.preparation[:-1])
                return f"{' '.join(self.preparation[:-1])} and {self.preparation[-1]} "

    def format_ingredient_name(self):
        """description ingredient name, preparation
        ex. salted butter, softened
        ex. candied pecans, chopped and toasted
        ex. fresh romaine, cleaned and chopped
        ex. plain, nonfat greek yogurt
        ex. meduim, brown eggs, boiled and peeled
        """
        prep = self.get_preparation()

        match len(self.description):
            case 0:
                return f"{prep}{self.ingredient_name}"
            case 1:
                return f"{prep}{self.description[0]} {self.ingredient_name}"
            case _:
                return f"{prep}{', '.join(self.description)} {self.ingredient_name}"
        

    
    def __str__(self):
        #probs need to adjust plurals
        name = self.format_ingredient_name()
        if self.quantity != 1 and self.unit[-1] != "s":
            return f"{self.quantity_unicode} {self.unit}s of {name}{self.unit_qualifier}\n"
        elif self.unit != None:
            return f"{self.quantity_unicode} {self.unit} of {name}{self.unit_qualifier}\n"
        else:
            return f"{self.quantity_unicode} {name}{self.unit_qualifier}\n"


        


