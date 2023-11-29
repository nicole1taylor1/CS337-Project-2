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

        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

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
                
    Within the chat, you can ask me to list ingredients or walk through the recipe. If you need to go back a step or to remind you the details of an ingredients just ask!            
    
    ### Help
    Here go any additional how to use me details   

    ### Features         
    '''
    )
    st.caption("Developed by Alfonso Napoles and Nicole Taylor for CS337 @ Northwestern")

##########################GET RECIPE URL#######################
###############################################################
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


##########################CHAT#################################
###############################################################
if soup:
    # Accept user input
    if prompt := st.chat_input("How can I help you?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        #NEED LOGIC HERE FOR UNDERSTAND USER QUESTIONS AND COMMANDS!!!

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            assistant_response = random.choice(
                [
                    "Hello there! How can I assist you today?",
                    "Hi, human! Is there anything I can help you with?",
                    "Do you need help?",
                ]
            )
            # Simulate stream of response with milliseconds delay
            for chunk in assistant_response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})