import re
import spacy
from foodlists import utensils, actions

nlp = spacy.load("en_core_web_lg")

from ourtypes.step import Step, Steps

def find_steps(soup, ingredient_objects):
    #find the steps of the recipe
    steps = soup.find("div", {"id":"recipe__steps-content_1-0"})
    steps_collection = Steps()

    def find_time(text):
        #find the time mentioned for in the step
        time = []
        time_pat = r'\b(\w+)\b\s+(\d+\s+to\s+\d+|\d+)\s*(hours?|hrs?|minutes?|mins?|seconds?|secs?)\s*(and\s+\d+)?\s*(hours?|hrs?|minutes?|mins?|seconds?|secs?)?'
        time_match = re.findall(time_pat, text)
        if time_match:
            for t in time_match:
                time.append(' '.join(filter(None, t)))
        return time

    def find_temp(text):
        #find the temperature for that step
        temp = []
        temp_match = re.findall(r'(\d+ degrees (C|F|celsius|fahrenheit))', text, re.IGNORECASE)
        if temp_match:
            for t in temp_match:
                temp.append(t[0])
        return temp

    def find_methods(doc):
        methods = []
        for sent in doc.sents:
            for token in sent:
                #check if token is a verb
                if token.pos_ == 'VERB':
                    methods.append(token.lemma_) 
                    # if token.i == sent.start:
                    #     methods.append(token.lemma_)
                
                    # #check if itcomes after punctuation or 'and'
                    # else:
                    #     prev_token = token.nbor(-1)
                    #     if prev_token.is_punct or (prev_token.text.lower() == 'and'):
                    #         methods.append(token.lemma_)
        #check if any of the methods are actually cooking actions
        final_methods = []
        for method in methods:
            for word in method.split():
                if word.lower() in actions:
                    final_methods.append(method)
                    break
        return set(final_methods)
    def find_method_asc(tools, step_ingr, time, temp):
        method_associations = {}

        for method in methods:
            method_associations[method] = {'ingredients': [], 'tools': [], 'time': [], 'temp': []}
            for sent in doc.sents:
                lemma = sent.lemma_.split(',')
                broken_sent = sent.text.split(',')
                for i, s in enumerate(lemma):
                    if method in s:
                        associated_tools = []
                        for tool in tools:
                            if any(t in sent.text for t in tool.split()):
                                associated_tools.append(tool)
                        associated_ingredients = []
                        for ingred in step_ingr:
                            words = ingred.split()
                            for word in words:
                                if word in sent.text:
                                    associated_ingredients.append(ingred)
                                    break
                        text = broken_sent[i]
                        for t in sorted(time, key=len, reverse=True):
                            if t in text:
                                method_associations[method]['time'].extend([t])
                                break
                        for t in temp:
                            if t in text:
                                method_associations[method]['temp'].extend([t])
            method_associations[method]['tools'].extend(associated_tools)
            method_associations[method]['ingredients'].extend(associated_ingredients)
        return method_associations

    def find_ingr(ingredient_objects):
        #identify ingredients present in this step
        step_ingredients = []
        for ingred in ingredient_objects:
            words = ingred.split()
            for word in words:
                if word in step_text:
                    step_ingredients.append(ingred)
                    break
        return step_ingredients

    def find_tools(doc):
        tools = []
        #extract compound nouns for full tool names
        for chunk in doc.noun_chunks:
            tokens = chunk.text.split()
            if len(tokens) > 1 and tokens[0].lower() in ['a', 'an', 'the']:
                #check if the last word is a noun
                if nlp(chunk.text)[-1].pos_ == 'NOUN':
                    tools.append(chunk.text)
            elif chunk.root.dep_ in ['dobj', 'pobj']:  #direct object or object of preposition
                #check if the current chunk is a compound noun
                if any(child.dep_ == 'compound' for child in chunk.root.children):
                    tools.append(chunk.text)
                elif chunk.root.pos_ == 'NOUN':
                    tools.append(chunk.text)
        #remove tools are not tools, do not end in a noun and do not start with "a" or "an":
        tools = [tool for tool in tools if nlp(tool)[-1].pos_ == 'NOUN' and tool.split()[0] in ["a", "an", "the"]]
        final_tools = []
        for tool in tools:
            for words in tool.split():
                if words in utensils:
                    final_tools.append(tool)
                    break
        return final_tools

    def find_tool_asc(tools, step_ingr, methods):
        tool_associations = {}  
        for tool in tools:
            tool_associations[tool] = {'methods': [], 'ingredients': []}
            for sent in doc.sents:
                if tool in sent.text:
                    associated_methods = [method for method in methods if method in sent.lemma_]
                    associated_ingredients = []
                    for ingred in step_ingr:
                        words = ingred.split()
                        for word in words:
                            if word in sent.text:
                                associated_ingredients.append(ingred)
                                break
                    tool_associations[tool]['methods'].extend(associated_methods)
                    tool_associations[tool]['ingredients'].extend(associated_ingredients)
        return tool_associations
        

    for child in steps.find_all("p"):
        step_text = child.text.replace("\n", "").strip()
        doc = nlp(step_text)
        time = find_time(step_text)
        temp = find_temp(step_text)
        methods = find_methods(doc)
        step_ingr = find_ingr(ingredient_objects)
        tools = find_tools(doc)
        tool_asc = find_tool_asc(tools, step_ingr, methods)
        method_asc = find_method_asc(tools, step_ingr, time, temp)

        #create Step object
        step_obj = Step(ingredients=step_ingr, tools=tool_asc, methods=method_asc, description=step_text, time=time, temp=temp)

        #add Step object to Steps collection
        steps_collection.add_step(step_obj)
    return steps_collection

# Steps class: This class is a collection of Step objects.

# Step class: This class is a single step in a recipe. It has these attributes:

#               ingredients: This is a list of ingredients used in this step.
#                     (Example: ['flour', 'brown sugar', 'butter', 'vanilla extract', 'salt', 'milk', 'milk chocolate chips', 
#                                 'chocolate chips'] )

#               tools: This is a list of tools used in this step, along with the associations.
#                     (Example: {'an oven':                     // 1 of the tools mentioned in the step 
#                                 {'methods': ['toast'],        // What methods this tool is used in
#                                 'ingredients': ['flour']}}    // What this tool is used on.)

#               methods: This is a list of cooking methods used in this step, along with the associations.
#                     (Example: {'toast':                                       // 1 of the methods mentioned in the step
#                                 {'ingredients': ['flour'],                    // ingredients associated with this method
#                                 'tools': ['a microwave', 'a baking sheet',
#                                            'an oven'],                        // tools associated with this method
#                                 'time': ['for 5 to 6 minutes'],               // time associated with this method (for the oven)
#                                 'temp': ['350 degrees F']}}                   // temp associated with this method (for the oven))

#               description: This is the text description of the step.
#                     (Example: See below)

#               time: This is a list of times mentioned in this step. (Used to create associations)
#                     (Example: [for 10 minutes, every 20 sec], if the step mentions "use tool for 10 minutes" and asks 
#                                 "to stir every 20 sec")

#               temp: This is the list of temperatures mentioned in this step. (Used to create associations)
#                     (Example: [190 Degrees celsius, 375 degrees F] if the step mentions "Preheat oven to 190 degrees C 
#                                 or 375 degrees F")

# Ingredients, Methods and Tools will probably be the most useful attr. to use in the front-end

# Example Steps Class:

# Step 1: Step(Ingredients: ['flour'], 
#             Tools: {'a microwave-safe dish': 
#                         {'methods': ['cook', 'stir'], 
#                         'ingredients': ['flour']}}, 
#             Methods: {'cook': 
#                         {'ingredients': ['flour'], 
#                         'tools': ['a microwave-safe dish'], 
#                         'time': ['for 1 minute and 15 seconds'], 
#                         'temp': []}, 
#                     'stir': 
#                         {'ingredients': ['flour'], 
#                         'tools': ['a microwave-safe dish'], 
#                         'time': ['every 15 seconds'], 
#                         'temp': []}}, 
#             Time: ['for 1 minute and 15 seconds', 'every 15 seconds'], 
#             Temp: [], 
#             Description: 'To heat-treat your flour so it is safe to use: Place flour in a microwave-safe dish and cook 
#             for 1 minute and 15 seconds, stirring it every 15 seconds. Set aside.')

# Step 2: Step(Ingredients: ['flour', 'brown sugar', 'butter', 'vanilla extract', 'salt', 'milk', 'milk chocolate chips', 
#                             'chocolate chips'], 
#             Tools: {'an electric mixer': 
#                         {'methods': ['Beat', 'mix'], 
#                         'ingredients': ['brown sugar', 'butter']}, 
#                     'a large bowl': 
#                         {'methods': ['Beat', 'mix'], 
#                         'ingredients': ['brown sugar', 'butter']}}, 
#             Methods: {'stir': 
#                         {'ingredients': ['milk', 'milk chocolate chips', 'chocolate chips'], 
#                         'tools': ['an electric mixer', 'a large bowl'], 
#                         'time': [], 
#                         'temp': []}, 
#                     'combine': 
#                         {'ingredients': ['milk', 'milk chocolate chips', 'chocolate chips'], 
#                         'tools': ['an electric mixer', 'a large bowl'], 
#                         'time': [], 
#                         'temp': []}, 
#                     'Beat': 
#                         {'ingredients': ['vanilla extract', 'salt'], 
#                         'tools': ['an electric mixer', 'a large bowl'], 
#                         'time': [], 
#                         'temp': []}, 
#                     'add': 
#                         {'ingredients': ['flour'], 
#                         'tools': ['a large bowl'], 
#                         'time': [], 
#                         'temp': []}, 
#                     'mix': 
#                         {'ingredients': ['flour'], 
#                         'tools': ['a large bowl'], 
#                         'time': [], 
#                         'temp': []}}, 
#             Time: [], 
#             Temp: [], 
#             Description: 'Beat sugar and butter with an electric mixer in a large bowl until creamy. Beat in vanilla extract 
#                 and salt. Add heat-treated flour; mix until a crumbly dough forms. Stir in milk until dough is just combined; 
#                 fold in milk chocolate chips and mini chocolate chips.')

# Step 3: Step(Ingredients: ['flour'], 
#             Tools: {'a microwave': 
#                         {'methods': ['toast'], 
#                         'ingredients': ['flour']}, 
#                     'a baking sheet': 
#                         {'methods': ['toast'], 
#                         'ingredients': ['flour']}, 
#                     'an oven': 
#                         {'methods': ['toast'], 
#                         'ingredients': ['flour']}}, 
#             Methods: {'toast': 
#                         {'ingredients': ['flour'], 
#                         'tools': ['a microwave', 'a baking sheet', 'an oven'], 
#                         'time': ['for 5 to 6 minutes'], 
#                         'temp': ['350 degrees F']}}, 
#             Time: ['for 5 to 6 minutes'], 
#             Temp: ['350 degrees F'], 
#             Description: 'There is a potential risk of foodborne illness from the consumption of raw flour. Follow Step 1 to 
#                             heat-treat your flour so it is safe to use. If you do not have a microwave, spread flour out on a 
#                             baking sheet and toast in an oven at 350 degrees F for 5 to 6 minutes.')