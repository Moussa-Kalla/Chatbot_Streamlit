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

if "conversations" not in st.session_state:
    st.session_state["conversations"] = [
        {
            "name": "Conversation 1",
            "messages": [
                {
                    "role": "assistant",
                    "content": "Bonjour, je suis votre assistant !"
                }
            ],
        }
    ]
    st.session_state["selected_conv_index"] = 0

st.sidebar.title("Conversations")
if st.sidebar.button("Nouvelle conversation"):
    new_conv = {
        "name": f"Conversation {len(st.session_state['conversations']) + 1}",
        "messages": [
            {
                "role": "assistant",
                "content": "Bonjour, je suis votre assistant !"
            }
        ],
    }
    st.session_state["conversations"].append(new_conv)
    st.session_state["selected_conv_index"] = len(st.session_state["conversations"]) - 1

conv_names = [conv["name"] for conv in st.session_state["conversations"]]
selected = st.sidebar.radio(
    "Sélectionnez une conversation",
    range(len(conv_names)),
    format_func=lambda i: conv_names[i],
    index=st.session_state["selected_conv_index"]
)
st.session_state["selected_conv_index"] = selected

st.markdown("""
    <style>
        .centered-input {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        }
        .chat-input {
            width: 50%;
            font-size: 1.5em;
        }
        .chat-avatar img {
            width: 50px;
            height: 50px;
            border-radius: 50%;
        }
        /* Début des modifications pour le logo */
        .chat-logo {
            text-align: center;
            margin: 20px 0;
        }
        .chat-logo img {
            max-width: 200px !important;  /* Taille personnalisable ici */
            height: auto !important;
            width: auto !important;
        }
        /* Fin des modifications */
        .main {
            overflow-y: auto;
            transition: height 0.5s;
        }
    </style>

    <script>
        function scrollToBottom() {
            const chatContainer = window.parent.document.querySelector('.main');
            if (chatContainer) {
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }
        }
    </script>
""", unsafe_allow_html=True)

# Section du logo modifiée
st.markdown('<div class="chat-logo">', unsafe_allow_html=True)
st.image("app/assets/logo.png", use_container_width =False, width=200)  # Ajustez la valeur 'width' ici
st.markdown('</div>', unsafe_allow_html=True)

if st.session_state["selected_conv_index"] is not None:
    current_conv = st.session_state["conversations"][st.session_state["selected_conv_index"]]
    for msg in current_conv["messages"]:
        avatar_url = "app/assets/user.png" if msg["role"] == "user" else "app/assets/assistant.png"
        with st.chat_message(msg["role"], avatar=avatar_url):
            st.markdown(msg["content"])

    with st.container():
        st.markdown('<div class="centered-input">', unsafe_allow_html=True)
        user_input = st.text_input("Posez votre question...", key="chat_input", placeholder="Posez n'importe quelle question...", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)


    if user_input:
        current_conv["messages"].append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="app/assets/user.png"):
            st.markdown(user_input)
        if current_conv["name"].startswith("Conversation "):
            current_conv["name"] = generate_conversation_name(user_input)
        full_prompt = format_prompt(current_conv["messages"])
        assistant_response = LLMs([{ "role": "user", "content": full_prompt }])
        current_conv["messages"].append({"role": "assistant", "content": assistant_response})
        st.markdown("<script>scrollToBottom();</script>", unsafe_allow_html=True) 
else:
    st.info("Créez ou sélectionnez une conversation dans la barre latérale pour commencer.")
