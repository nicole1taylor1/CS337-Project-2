import streamlit as st
import time
import parser_1

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

        

#CHAT BOT APP
st.title("AllRecipes Sous Chef")

#Intialize Chat History 
if "messages" not in st.session_state:
    st.session_state.messages = []

# Accept user input
if prompt := st.chat_input(""):
    # Ask for a URL
    assistant_respond("Hi, I'm your AllRecipes Sous Chef.\nType the url of the recipe you'd like to me to assist with.")
    
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    #Check validity of recipes

    while True:
        code, message = parser_1.check_url(prompt)
        match code:
            case 0:
                #display the title of the recipe
                break
            case 1:
                #error message for invalid url
    
    soup = parser_1.read_recipe_from_url(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = "Hello there! How can I assist you today?"
                
        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})