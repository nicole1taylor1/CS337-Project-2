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

##########################GET RECIPE URL#######################
###############################################################
#get URL for recipe
url = st.text_input(label=":gray[Please type URL below]")
if url:
    code, message = parser_1.check_url(url)
    match code:
        case 1:
            #invalid URL
            st.error(message)
        case 0:
            #valid URL, display title
            random_response = random.choice(
            [
                "Yum!", "That sounds good!", 
                "That's my favorite recipe!", "Save some for me please!",
                "Great choice!", "Delish!", "I ❤️ that!"
            ]
            )
            response = f":gray[{message} ... {random_response}]"
            st.write(response)

##########################SIDEBAR##############################
###############################################################
with st.sidebar:
    st.title("The Sous Chef")
    st.markdown('''
    ### About Me :male-cook:
    I'm designed to parse recipes from [AllRecipes](http://allrecipes.com/).  
    I can help you by
    - Listing ingredients
    - Stepping through the recipe
    
    ### Getting Started
    
    '''
    )

##########################CHAT#################################
###############################################################

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Accept user input
if prompt := st.chat_input(""):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

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