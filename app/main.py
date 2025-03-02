import streamlit as st
from chat import LLMs
from prompt import prompt_context


models = ["gpt-4o", "gpt-4.5-preview-2025-02-27", "gpt-4.5-preview"]
selected_model = st.sidebar.selectbox("Sélectionnez un modèle", models)


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

if "conversations" not in st.session_state:
    st.session_state["conversations"] = [
        {
            "name": "Conversation 1",
            "messages": [
                {
                    "role": "assistant",
                    "content": "Je suis Moussa votre assistant, comment puis-je vous aider ?"
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
                "content": "Je suis Moussa votre assistant, comment puis-je vous aider ?"
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

########################################################    
#st.markdown('<div class="chat-logo">', unsafe_allow_html=True)
st.image("assets/logo.svg", width=300)
#st.markdown('</div>', unsafe_allow_html=True)
##############################################################

if st.session_state["selected_conv_index"] is not None and st.session_state["conversations"]:
    current_conv = st.session_state["conversations"][st.session_state["selected_conv_index"]]
    for msg in current_conv["messages"]:
        avatar_url = "assets/user.svg" if msg["role"] == "user" else "assets/assistant.svg"
        with st.chat_message(msg["role"], avatar=avatar_url):
            st.markdown(msg["content"])

    if user_input := st.chat_input("Posez votre question..."):
        current_conv["messages"].append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="assets/user.svg"):
            st.markdown(user_input)

        if current_conv["name"].startswith("Conversation"):
            current_conv["name"] = generate_conversation_name(user_input)

        full_prompt = format_prompt(current_conv["messages"])
        assistant_response = LLMs([{"role": "user", "content": full_prompt}], selected_model)

        current_conv["messages"].append({"role": "assistant", "content": assistant_response})
else:
    st.info("Créez ou sélectionnez une conversation dans la barre latérale pour commencer.")