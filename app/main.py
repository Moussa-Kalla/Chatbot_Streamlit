import streamlit as st
from chat import LLMs
from prompt import prompt_context
import ollama

class ChatApp:
    def __init__(self):
        self._init_state()
        self.models = [m.model for m in ollama.list().models]
        self.model = st.sidebar.selectbox("Modèle", self.models)

    def _init_state(self):
        if "convs" not in st.session_state:
            st.session_state["convs"] = [{"name": "Conv 1", "msgs": [{"role": "assistant", "content": "Bonjour!"}]}]
        if "idx" not in st.session_state:
            st.session_state["idx"] = 0

    def gen_name(self, prompt, max_len=20):
        text = prompt.strip() or "Nouv. conv"
        words = text.split()[:5]
        name = " ".join(words)[:max_len] + ("..." if len(text) > max_len else "")
        return name.capitalize()

    def format_prompt(self, msgs, p_context=prompt_context):
        prompt = p_context
        for msg in msgs:
            role = "User" if msg["role"] == "user" else "Assistant"
            prompt += f"{role}: {msg['content']}\n"
        return prompt

    def _sidebar(self):
        st.sidebar.title("Conversations")
        if st.sidebar.button("Nouveau"):
            st.session_state["convs"].append({"name": f"Conv {len(st.session_state['convs']) + 1}", "msgs": [{"role": "assistant", "content": "Bonjour!"}]})
            st.session_state["idx"] = len(st.session_state["convs"]) - 1

        names = [c["name"] for c in st.session_state["convs"]]
        if names:
            st.session_state["idx"] = st.sidebar.radio("Choisir conv", range(len(names)), format_func=lambda i: names[i], index=st.session_state["idx"])
        else:
            st.sidebar.info("Aucune conv.")

    def _chat_ui(self):
        """Affiche UI chat."""
        st.image("assets/logo.svg", width=200)
        if not st.session_state["convs"]:
            st.info("Créer/choisir conv.")
            return

        conv = st.session_state["convs"][st.session_state["idx"]]
        for msg in conv["msgs"]:
            avatar = "assets/user.svg" if msg["role"] == "user" else "assets/assistant.svg"
            with st.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["content"])

        if prompt := st.chat_input("Votre message"):
            conv["msgs"].append({"role": "user", "content": prompt})
            with st.chat_message("user", avatar="assets/user.svg"):
                st.markdown(prompt)

            if conv["name"].startswith("Conv"):
                conv["name"] = self.gen_name(prompt)

            full_prompt = self.format_prompt(conv["msgs"])
            resp = LLMs([{"role": "user", "content": full_prompt}], self.model)
            conv["msgs"].append({"role": "assistant", "content": resp})

    def run(self):
        """Point d'entrée app."""
        self._sidebar()
        self._chat_ui()

if __name__ == "__main__":
    ChatApp().run()