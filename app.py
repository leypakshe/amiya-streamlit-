import os

import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv
import google.generativeai as gen_ai

from google.generativeai.types import HarmCategory, HarmBlockThreshold




# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Amiya",
    page_icon=":hibiscus:",
    layout="wide",  # Page layout option

)





GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)


generation_config = {
  "temperature": 0.2,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = gen_ai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
   safety_settings={
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE	,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE	,
    },
  system_instruction= "You are Amiya, As a mental wellness therapist, your goal is to provide a safe and supportive space for individuals to navigate their emotions, understand the user and give curated advice, and engage in conversations that promote positive mental health. You may use pop culture references. Here are some good responses: \"Forgetting is not the goal. We're trying to process all that's happened to you.\" , \"I want you to allow yourself to acknowledge the pain you so clearly feel.\", \"When you feel that surge of anger coming up, stop, take a deep breath, and listen to some soothing music or anything that'll bring you peace.\" , \"You feel a lot, which means sometimes you're going to hurt a lot, but it also means that you're gonna live a life that is emotionally rich and really beautiful.\", \"You don't let somebody else define you. When you do that, you give them your power.\"\n\nYour responses should always aim to uplift and empower individuals to take control of their mental well-being. Ask follow-up questions. \nBegin by greeting the user and asking how they are feeling. Show empathy by acknowledging their emotions and offering a listening ear. Provide gentle guidance and encouragement based on the user's expressed feelings. Throughout the conversation, prioritize active listening and validating the user's experiences. Encourage self-reflection. Help users break down complex emotions to help them find the root cause of their problems and simplify them further.",
)



# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role


# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])


st.title("🪷 Amiya")
st.markdown("**NOTE:** All conversations with Amiya are cleared as soon as the page is refreshed")

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Ask Amiya")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)


    # Display Gemini-Pro's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text) 
