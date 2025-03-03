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
        if chunk and hasattr(chunk[0].delta, "content"):
            delta_content = chunk[0].delta.content
            if delta_content: 
                content += delta_content
                text_placeholder.markdown(content)

    return content
