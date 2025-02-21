import streamlit as st
from chat import LLMs
from prompt import prompt_context

def generate_conversation_name(prompt, max_len=30):
    text = prompt.replace("\n", " ").strip()
    if not text:
        return "Nouvelle conversation"

    words = text.split()
    if len(words) > 8:
        words = words[:8]

    short_name = " ".join(words)

    if len(short_name) > max_len:
        short_name = short_name[:max_len] + "..."

    return short_name[0].upper() + short_name[1:] if short_name else "Conversation"

def format_prompt(messages, prompt=prompt_context):
    for message in messages:
        role = "User" if message["role"] == "user" else "Assistant"
        prompt += f"{role}: {message['content']}\n"
    return prompt

# Initialisation des conversations dans la session
if "conversations" not in st.session_state:
    st.session_state["conversations"] = [
        {
            "name": "Conversation 1",
            "messages": [
                {
                    "role": "assistant",
                    "content": "Bonjour, je suis un nouvel assistant !"
                }
            ],
        }
    ]
    st.session_state["selected_conv_index"] = 0

if "selected_conv_index" not in st.session_state:
    st.session_state["selected_conv_index"] = 0

st.sidebar.title("Conversations")

if st.sidebar.button("Nouvelle conversation"):
    new_conv = {
        "name": f"Conversation {len(st.session_state['conversations']) + 1}",
        "messages": [
            {
                "role": "assistant",
                "content": "Bonjour, je suis un nouvel assistant !"
            }
        ],
    }
    st.session_state["conversations"].append(new_conv)
    st.session_state["selected_conv_index"] = len(st.session_state["conversations"]) - 1

conv_names = [conv["name"] for conv in st.session_state["conversations"]]
if conv_names:
    selected = st.sidebar.radio(
        "Sélectionnez une conversation",
        range(len(conv_names)),
        format_func=lambda i: conv_names[i],
        index=st.session_state["selected_conv_index"]
    )
    st.session_state["selected_conv_index"] = selected
else:
    st.sidebar.info("Aucune conversation disponible.")

#st.title("chat")

if st.session_state["selected_conv_index"] is not None and st.session_state["conversations"]:
    current_conv = st.session_state["conversations"][st.session_state["selected_conv_index"]]

    for msg in current_conv["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_input := st.chat_input("Posez votre question..."):
        current_conv["messages"].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        if current_conv["name"].startswith("Conversation "):
            current_conv["name"] = generate_conversation_name(user_input)

        full_prompt = format_prompt(current_conv["messages"])
        assistant_response = LLMs([{"role": "user", "content": full_prompt}])

        current_conv["messages"].append({"role": "assistant", "content": assistant_response})
        with st.chat_message("assistant"):
            st.markdown(assistant_response)
else:
    st.info("Créez ou sélectionnez une conversation dans la barre latérale pour commencer.")
