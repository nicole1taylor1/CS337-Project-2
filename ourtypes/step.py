"""
How it should print out:
Step #1
Ingredients: ingredients objects
tools: list of str
methods: list of methods
description = description of step
time, temp 
"""

class Step:
    """
    Step Class
    ingredients -> list of Ingredient objects used in this step.
    tools -> list of str, tools required for this step
    methods -> list of str, cooking methods used in this step 
    description -> str, a description of the step.
    time -> time required for this step (optional)
    temp -> temperature set for this step (optional)
    """
    def __init__(self, ingredients, tools, methods, description=None, time=None, temp=None):
        self.ingredients = ingredients
        self.tools = tools
        self.methods = methods
        self.description = description
        self.time = time
        self.temp = temp

    def __repr__(self):
            return f"Step(Ingredients: {self.ingredients}, Tools: {self.tools}, Methods: {self.methods}, Time: {self.time}, Temp: {self.temp}, Description: '{self.description}')"
    
    def print_desc(self, stepnum):
        ingredients = f"**Ingredients** required for **Step #{stepnum + 1}:**  \n\n" + "  \n\n".join([str(ingedient) for ingedient in self.ingredients])
        return self.description + "  \n\n" + ingredients
    
    """def __str__(self):
        ingredients = "**Ingredients required for this step:**  \n" + "\n".join([str(ingedient) for ingedient in self.ingredients])
        tools = f"**Tools required for this step:  \n" + "\n".join([("•  " + str(tool) for tool in tools)])
        methods = f"**Methods required for this step:  \n" + "\n".join([("•  " + str(tool) for tool in tools)])"""

    

class Steps:
    """
    Steps Class
    steps -> list of Step objects

    methods
        add_step(step) -> Adds a Step object to the list.
        get_step(index) ->  Retrieves a Step at an index.
        remove_step(index) -> Removes a Step at an index.
        __len__ -> Returns the number of steps.
        __getitem__ -> Allows indexing.
        __repr__ -> Returns a string of all steps.
    """

    def __init__(self):
        self.steps = []

    def add_step(self, step):
        self.steps.append(step)

    def get_step(self, index):
        if index <= len(self.steps):
            return self.steps[index]
        else:
            return None

    def remove_step(self, index):
        del self.steps[index]

    def __len__(self):
        return len(self.steps)

    def __getitem__(self, index):
        return self.steps[index]

    def __repr__(self):
        return "\n".join([f"Step {i + 1}: {step}" for i, step in enumerate(self.steps)])

