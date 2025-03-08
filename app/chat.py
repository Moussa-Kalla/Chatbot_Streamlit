from ollama import chat
import streamlit as st

def LLMs(conversation, model):
    response = chat(
        model=model,
        messages=conversation,
        stream=True  
    )

    content = ""  
    text_placeholder = st.empty() 

    for chunk in response:
        content += chunk['message']['content']
        text_placeholder.markdown(content)

    return content