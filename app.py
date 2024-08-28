import openai
import streamlit as st
from PIL import Image
import os
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header

st.set_page_config(page_title="Peace pal Chatbot", page_icon=":robot:")

openai.api_key =""
# # And the root-level secrets are also accessible as environment variables:
 #os.environ["openai_secret_key"] == st.secrets["openai_secret_key"]

page_bg = f"""
<style>
[data-testid="stSidebar"] {{
background-color:white;

}}

[data-testid="stToolbar"] {{
background-color:white;

}}
</style>
"""
st.markdown(page_bg,unsafe_allow_html=True)
 
# Sidebar contents
with st.sidebar:
    

    image = Image.open('example.jpg')
    st.image(image, width=280)
    st.markdown("<h2 style='text-align: center; color: black;'> Mental Health Chatbot </h2>", unsafe_allow_html= True)

    st.markdown("<h1 style='text-align: left; color: black;'> About </h1>", unsafe_allow_html= True)
    st.markdown("""
    <p style='text-align: left; color: black;'> Meet Peace pal, your friendly mental health chatbot! Whether you're feeling down, anxious, or stressed, 
    Peace pal is here to help you navigate through your emotions and provide you with the guidance you need to feel better.
    With Peace pal, you can talk about your mental health concerns in a comfortable way, 
    using Tagalog and English slangs.  So don't hesitate to chat with Peace pal anytime, anywhere! </p><br><br>
    """, unsafe_allow_html=True)





# Generate empty lists for generated and past.
## generated stores AI generated responses
if 'generated' not in st.session_state:
    st.session_state['generated'] = ['Hello Pal, how may I help you?']
## past stores User's questions
if 'past' not in st.session_state:
    st.session_state['past'] = ['Hi']

# Layout of input/response containers
# colored_header(label='', description='', color_name="green-70")
response_container = st.container()
input_container = st.container()

# User input
## Function for taking user provided prompt as input
def get_text():
    text = st.text_input("You: ", "", key="input")
    return text

def clear_text():
    st.session_state["input"] = ""

## Applying the user input box
with input_container:
    user_input = get_text()
    st.button("Clear Text", on_click=clear_text)
 

messages = [{"role": "system", "content": "You are a friendly mental health adviser providing mental health support and service. \
              Make sure evrery responses is distinctive do not provide same responses each time"}]

def CustomChatGPT(user_input):
    messages.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages,
        temperature=0,
    )
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply


## Conditional display of AI generated responses as a function of user provided prompts
with response_container:
    if user_input:
        response = CustomChatGPT(user_input)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)
        
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))
            
                
