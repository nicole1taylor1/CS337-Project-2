import re
import spacy

nlp = spacy.load("en_core_web_lg")

from ourtypes.step import Step, Steps

def find_steps(soup, ingredient_objects):
    #find the steps of the recipe
    steps = soup.find("div", {"id":"recipe__steps-content_1-0"})
    steps_collection = Steps()

    def find_time(text):
        #find the time mentioned for in the step
        time = []
        time_match = re.findall(r'(\d+\s+to\s+\d+|\d+)\s*(hours?|hrs?|minutes?|mins?|seconds?|secs?)(\s+and\s+\d+\s*(hours?|hrs?|minutes?|mins?|seconds?|secs?))?', text)
        if time_match:
            for t in time_match:
                time.append(' '.join(filter(None, t)))
        return time

    def find_temp(text):
        #find the temperature for that step
        temp = []
        temp_match = re.findall(r'(\d+ degrees (C|F))', text)
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
                    #check if it's the first token in a sentence 
                    if token.i == sent.start:
                        methods.append(token.lemma_)
                
                    #check if itcomes after punctuation or 'and'
                    else:
                        prev_token = token.nbor(-1)
                        if prev_token.is_punct or (prev_token.text.lower() == 'and'):
                            methods.append(token.lemma_)
        return methods
    def find_method_asc(tools, step_ingr, time, temp):
        method_associations = {}

        for method in methods:
            method_associations[method] = {'ingredients': [], 'tools': [], 'time': [], 'temp': []}
            for sent in doc.sents:
                if method in sent.lemma_:
                    associated_tools = [tool for tool in tools if tool in sent.text]
                    associated_ingredients = []
                    for ingred in step_ingr:
                        words = ingred.split()
                        for word in words:
                            if word in sent.text:
                                associated_ingredients.append(ingred)
                                break
            method_associations[method]['tools'].extend(associated_tools)
            method_associations[method]['ingredients'].extend(associated_ingredients)
            if any(t in sent.text for t in time):
                method_associations[method]['time'].extend([t for t in time if t in sent.text])
            if any(t in sent.text for t in temp):
                method_associations[method]['temp'].extend([t for t in temp if t in sent.text])      
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
            if len(tokens) > 1 and tokens[0].lower() in ['a', 'an']:
                #check if the last word is a noun
                if nlp(chunk.text)[-1].pos_ == 'NOUN':
                    tools.append(chunk.text)
            elif chunk.root.dep_ in ['dobj', 'pobj']:  #direct object or object of preposition
                #check if the current chunk is a compound noun
                if any(child.dep_ == 'compound' for child in chunk.root.children):
                    tools.append(chunk.text)
                elif chunk.root.pos_ == 'NOUN':
                    tools.append(chunk.text)
        #remove tools are ingredients, do not end in a noun and do not start with "a" or "an":
        # tools = [tool for tool in tools if all(ingr not in tool for ingr in ingredient_objects)]
        tools = [tool for tool in tools if nlp(tool)[-1].pos_ == 'NOUN' and tool.split()[0] in ["a", "an"]]
        return tools

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