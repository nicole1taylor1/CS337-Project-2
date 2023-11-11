
class Ingredient:
    """Ingredient Class
    ingredient name -> str
    quantity -> int/float 
    measurement -> str (cup, teaspoon, pinch, etc.)
    descriptor -> str (optional, e.g. fresh, extra-virgin)
    preparation -> str (optional, e.g. chopped)
    """

    def __checktype__(self, var, typ):
        assert isinstance(var, typ), f"Field hould be type: {typ}, is {var}"
        if type == str:
            assert not var.isspace(), "Field cannot be whitespace"

    def __init__(self, ingredient_name, quantity, measuement, descriptor=None, preparation=None):
        #check the inputs are of the correct type
        for var, typ in zip([ingredient_name, quantity, measuement,descriptor, preparation],
                            [str, (int, float), str, (None, str), (None, str)]):
            self.__checktype__(var, typ)
        
        #set fields
        self.ingredient_name = ingredient_name
        self.quantity = quantity
        self.measurement = measuement
        self.description = descriptor 
        self.preparation = preparation

    


        


