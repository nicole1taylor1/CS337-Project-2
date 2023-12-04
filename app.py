import streamlit as st
import random
import time
import parser_1
#from streamlit_chat import message
#from streamlit_extras.colored_header import colored_header
#from streamlit_extras.add_vertical_space import add_vertical_space

#HELPER FUNCTION
def assistant_respond(assistant_response):
    #avatar="👨🏻‍🍳"
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        #handle new lines
        chars = assistant_response.split()
        if "  \n\n" in assistant_response:
            chars = []
            chunks = assistant_response.split("\n\n")
            for chunk in chunks:
                chars += chunk.split()
                chars.append("  \n\n")

        # Simulate stream of response with milliseconds delay
        for chunk in chars:
            full_response += chunk + " "
            time.sleep(0.04)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    #(})
    return {"role": "assistant", "content": full_response}

##########################TITLE################################
###############################################################

col1, col2 = st.columns([0.12,0.88])
with col1:
    #add All Recipes logo
    st.image('allrecipeslogo.jpeg')
with col2:
    st.title("AllRecipes Sous Chef")


##########################SIDEBAR##############################
###############################################################
with st.sidebar:
    st.title("The Sous Chef")
    
    st.markdown('''
    ### About Me :male-cook:  
                
    I'm designed to parse recipes from [AllRecipes](allrecipes.com)  
    
    ### Getting Started  
                
    Once you know which recipe you'd like to try, paste the link in the corresponding field. If the URL is valid, the chat feature will pop up.  
                
    ### How To  
    To **walk through the recipe**:  
    •  :grey[_Ask me to **step through recipe** in your query_]  
    •  :grey[_I will read you one step at a time_]  
    •  :grey[_To see the next step, type **next step**_]  
    •  :grey[_To see the previous step, type **previous step**_]  
    •  :grey[_To see a specific step, type **step number 1, step number 2**, etc._]  
                 
                
    To see the list of **ingredients**:  
    •  :grey[_Use they keywords **ingredient** & **list** in your query_]
                
    To see **nutritional info**:  
    •  :grey[_Use they keywords **nutritional info** in your query_]  
    •  :grey[_Or specify the fact you'd like to see (i.e. calories, fat, protein, carbs, servings)_]  
                
    To see the **time required**:   
    •  :grey[_Use they keywords **prep time** or **total time** in your query_]    
                
    To change the **number of servings**:   
    •  :grey[_Ask me to **change the serving size**, then you'll be prompted to specify by what amount_]    
                        
    '''
    )
    st.caption("Developed by Alfonso Napoles and Nicole Taylor for CS337 @ Northwestern")

##########################GET RECIPE URL#######################
###############################################################
@st.cache_data
def get_recipe(url):
    exitcode2, soup = parser_1.read_recipe_from_url(url)
    recipe = parser_1.make_recipe(soup)
    return recipe

#get URL for recipe
soup = None
url = st.text_input(label=":gray[Please type URL below]")
if url:
    exitcode1, recipename = parser_1.check_url(url)
    exitcode2, soup = parser_1.read_recipe_from_url(url)
    if exitcode1 == 1 or exitcode2 == 1:
        #invalid URL
        st.error("Invalid URL. Please try again.")
        st.stop()
    else:
        #valid URL, display title
        random_response = random.choice(
        [
            "Yum!", "That sounds good!", 
            "That's my favorite recipe!", "Save some for me please!",
            "Great choice!", "Delish!", "I ❤️ that!"
        ]
        )
        response = f":gray[{recipename} ... {random_response}]"
        st.write(response)

st.divider()

def get_last_step(messages):
    me = [ele["content"] for ele in messages if ele["role"] == "assistant" and "Step #" in ele["content"]]
    if me:
        last_step = me[-1][8]
        if str(last_step).isnumeric():
            return int(last_step)
    return 1
##########################CHAT#################################
###############################################################
if soup:
    recipe = get_recipe(url)
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("How can I help you?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        responded = False

        #NEED LOGIC HERE FOR UNDERSTAND USER QUESTIONS AND COMMANDS!!!

        #HANDLING FOLLOW UP QUESTIONS FIRST
        if len(st.session_state.messages) >= 2:
            last_response = st.session_state.messages[-2]
            if last_response["role"] == "assistant":
                content = last_response["content"]
                #CHANGE SERVING SIZE
                if content == 'Ok, it seems like you want to change the amount of servings... By how much?   \n\n _Type 2 to double it, Type 0.5 to cut it in half_   \n\n ':
                #the last user response should be the amount they want to change it by 
                    user_response = prompt.strip()
                    u = user_response.replace(".", "")
                    if u.isnumeric():
                        amount = float(user_response)
                        lead_in = f"Ok, you want to make {float(amount)}x the recipe for {recipe.name}  \n\n ... \n\n"
                        m = recipe.change_serving_size(amount)
                        response = lead_in + m + "Here's the new ingredient list. \n\n" +  "\n\n".join([str(ingedient) for ingedient in recipe.ingredients])
                    else:
                        response = "{amount} is not a valid number to change the recipe by.\n\n Please try again."
                    d = assistant_respond(response)
                    st.session_state.messages.append(d)
                    responded = True

        #option 1: List Ingredients
        input = prompt.lower()
        input = input.replace("?","")
        if "list" in input and "ingredient" in input:
            lead_in = "Ok, if I'm understanding correctly you'd like to see the list of ingredients.  \n Here they are:  \n\n"
            response = lead_in + "\n\n".join([str(ingedient) for ingedient in recipe.ingredients])
            d = assistant_respond(response)
            st.session_state.messages.append(d)
            responded = True
        
        #option 2: Change serving size of recipe
        if "change" in input and "serving" in input and "size" in input:
            response = "Ok, it seems like you want to change the amount of servings...  \n  By how much?  \n\n  _Type 2 to double it, Type 0.5 to cut it in half_"
            #prompt user for serving size change
            d = assistant_respond(response)
            st.session_state.messages.append(d)
            responded = True

        #option 3: step through recipe
        if "step" in input and "through" in input and "recipe" in input:
            response = f"Ok, you'd like me to walk you through the steps for {recipe.name}...  \n\n"
            step1 = recipe.print_step()
            response += step1
            #prompt user for serving size change
            d = assistant_respond(response)
            st.session_state.messages.append(d)
            responded = True

        if "next step" in input:
            step = get_last_step(st.session_state.messages)
            step += 1
            recipe.next_step()
            stepN = recipe.print_step(step)
            d = assistant_respond(stepN)
            st.session_state.messages.append(d)
            responded = True
        
        if "previous step" in input:
            step = get_last_step(st.session_state.messages)
            step += - 1
            recipe.previous_step()
            stepN = recipe.print_step(step)
            d = assistant_respond(stepN)
            st.session_state.messages.append(d)
            responded = True
        
        if "step #" in input or "step number" in input:
            num = str(input[-1])
            if num.isnumeric():
                step = recipe.print_step(int(num))
                d = assistant_respond(step)
                st.session_state.messages.append(d)
                responded = True
            else:
                response = f"{num} is not a valid step.  \n\n Please try again."
                d = assistant_respond(response)
                st.session_state.messages.append(d)
                responded = True

        #option 5: Ask for nutritional info
        if "nutritional info" in input:
            lead_in = f"Ok, you'd like to see the full nutritional info for {recipe.name}.  \n Here it is:  \n\n"
            response = lead_in + recipe.print_nutritional_facts()
            d = assistant_respond(response)
            st.session_state.messages.append(d)
            responded = True

        #Indiviaul nutritional info
        inputs = prompt.replace("?","").split(" ")
        for i in inputs:
            i = i.capitalize()
            if i in ["Fat", "Carbs", "Protein", "Calories", "Cals"]:
                if i == "Cals":
                    i = "Calories"
                title = recipe.name
                fact = recipe.get_fact(i)
                if fact is None:
                    response = "I'm sorry, but the nutritional info about {i} is unavailable.  \n\n Can I assist you with anything else?"
                else:
                    response = f"Ok, you'd like to see the {i} content.  \n\n {title} has {fact} {i}."
                d = assistant_respond(response)
                st.session_state.messages.append(d)
                responded = True

        #Asking for preptime, total time, servings
        query = " ".join([ele.capitalize() for ele in inputs])

        for i in ["Prep Time", "Total Time", "Servings"]:
            if i in query:
                title = recipe.name
                fact = recipe.get_fact(i)
                if fact is None:
                    response = "I'm sorry, but the info about {i} is unavailable.  \n\n Can I assist you with anything else?"
                else:
                    if i == "Servings":
                        response = f"Ok, you'd like to know about the number of {i}.  \n\n The recipe for {title} will yield **{fact} {i.lower()}**."
                    else:
                        response = f"Ok, you'd like to know about how long the {i.lower()} will take.  \n\n The recipe for {title} will require **{fact}** for **{i.lower()}**."
                d = assistant_respond(response)
                st.session_state.messages.append(d)
                responded = True

        #NO RESPONSE
        if not responded:
            response = "I'm sorry, but I don't understand your message. \n\n See the help section to the left if you need. \n\n Please try again."
            d = assistant_respond(response)
            st.session_state.messages.append(d)
            responded = True
        
