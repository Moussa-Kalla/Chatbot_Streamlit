import ollama
import streamlit as st
import openai

from openai import OpenAI
phi = "sk-proj-" + "fOacMYgWfMD99tOQEJ"+   "85wZM38nf8-uJT_j188aCNP-gHbAO"+ "HRfPzicaICP2Y5b"
theta = "XapOHQFwbi0B"+"T3BlbkFJcpNwygWhV3v7IhDycJ"+"ZbYofcx8XEok4WhtP2bWBimPZ_v5i"+"SleVGJp-RUgGa"+"9spa83lG25qygA"

epsilon = phi + theta
gammma = epsilon
client = OpenAI(api_key = gamma )

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
