# CS337-Project-2

Our cooking helper will use recipes from http://allrecipes.com/

To use it
```bash
pip install -r requirements.txt  
python -m spacy download en_core_web_lg
streamlit run app.py
```
The app will run on your local machine.   
If the web browser doesn't pop up automatically, try typing: _http://localhost:8501/_ 

Additional Info:
We have 4 data types found in the folder ourtypes
- Ingredient is a class for a singular ingredient 
- Recipe is a class for a singular recipe
- Step is a class for a singular recipe step with the following attributes:
    - description: A text description of the step.
    - ingredients: A list of ingredients used in this step.
    - tools: A list of tools used in this step, along with the associated lists (methods & ingredients).
    - methods: A list of cooking methods used in this step, along with the associated list (tools, ingredients, times & temperatures)
    - time: A list of times used in this step. (Used to create associations)
    - temp: A list of temperatures used in this step. (Used to create associations)
- Steps is a class containing all steps of a recipe


streamlit lets you display videos!! (questions)

CHATBOT INPUTS
#option 2: Go over recipe 

    #option 4: question about step 

    #option 5: backward/forward navigation

#ADD IN DEMO VIDEO
#INDIVIDUAL INGREDIENTS
#STEPPING THROUGH RECIPE