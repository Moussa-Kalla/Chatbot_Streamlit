import ollama
import streamlit as st

def LLMs(conversation):
    stream = ollama.chat(
        model="llama3.2:1b",
        messages=conversation,
        stream=True,
    )

    content = ""
    text_placeholder = st.empty()

    for chunk in stream:
        content += chunk["message"]["content"]
        text_placeholder.markdown(content)

    return content