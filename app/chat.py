import ollama
import streamlit as st
import openai

from openai import OpenAI


client = OpenAI(api_key = api_key )

def LLMs(conversation):

    response = client.chat.completions.create(
        model="gpt-4",
        messages=conversation,
        max_tokens=1000,
        stream=True  
    )

    content = ""  
    text_placeholder = st.empty() 

    for chunk in response:
        if chunk.choices and hasattr(chunk.choices[0].delta, "content"):
            delta_content = chunk.choices[0].delta.content
            if delta_content: 
                content += delta_content
                text_placeholder.markdown(content)

    return content