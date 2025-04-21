import streamlit as st
from chat import LLMs
from prompt import prompt_context
import ollama
import os
import requests
import re

# bs4 n'est pas obligatoire ; on l'utilise si disponible pour un parsing plus fiable
try:
    from bs4 import BeautifulSoup  # type: ignore
except ImportError:  # pragma: no cover
    BeautifulSoup = None  # fallback en regex seule

SIZE_RE = re.compile(r"(?i)^(?:\d+(?:\.\d+)?(?:x\d+)?)(?:[bm])$")
LIBRARY_URL = "https://ollama.ai/library"


class ChatApp:
    """Application de chat Streamlit utilisant les modèles Ollama (installation locale) et
    la bibliothèque en ligne pour télécharger de nouveaux modèles."""

    #######################################
    # Initialisation
    #######################################
    def __init__(self):
        self._init_state()
        self._load_models()

    def _init_state(self):
        ss = st.session_state
        ss.setdefault(
            "convs",
            [
                {
                    "name": "Conv 1",
                    "msgs": [
                        {"role": "assistant", "content": "Bonjour!"},
                    ],
                }
            ],
        )
        ss.setdefault("idx", 0)
        ss.setdefault("ollama_models_cache", None)
        ss.setdefault(
            "thinking_models",
            [
                "llama3",
                "gemma3",
                "mistral",
            ],
        )
        ss.setdefault("thinking_visibility", {})

    #######################################
    # Chargement des modèles installés
    #######################################
    def _load_models(self):
        try:
            self.models = [m.model for m in ollama.list().models]
        except Exception as e:
            st.error(f"Erreur lors du chargement des modèles Ollama: {e}")
            self.models = []

        self.model = (
            st.sidebar.selectbox("Modèle installé", self.models) if self.models else ""
        )
        if not self.models:
            st.sidebar.info("Aucun modèle installé 💤")

    #######################################
    # Scraping de la bibliothèque Ollama
    #######################################
    def _scrape_library(self):
        """Interroge https://ollama.ai/library et extrait nom, description et tailles."""
        try:
            resp = requests.get(
                LIBRARY_URL,
                headers={"User-Agent": "Mozilla/5.0 (ChatApp)"},
                timeout=15,
            )
            resp.raise_for_status()
            html = resp.text
        except Exception as e:
            raise RuntimeError(f"Impossible de récupérer la bibliothèque : {e}") from e

        items = []

        # --- Parsing avec BeautifulSoup si dispo, sinon regex --------------
        if BeautifulSoup:
            soup = BeautifulSoup(html, "html.parser")  # type: ignore
            # Chaque entrée est un <li><a ...> ... Pulls</a></li>
            for a in soup.select("main a"):
                text = a.get_text(" ", strip=True)
                if "Pulls" not in text:
                    continue  # pas une entrée modèle
                parts = text.split()
                if not parts:
                    continue
                name = parts[0]
                # Recherche des tailles (7b, 70b, 8x22b, 135m…)
                sizes = [tok.lower() for tok in parts if SIZE_RE.match(tok.lower())]
                # Description : du mot après le nom jusqu'à la 1re taille ou «Pulls»
                try:
                    first_special = min(
                        parts.index(sizes[0]) if sizes else len(parts),
                        parts.index("Pulls"),
                    )
                except ValueError:
                    first_special = len(parts)
                description = " ".join(parts[1:first_special])
                items.append({"name": name.lower(), "sizes": sizes, "description": description})
        else:
            # Fallback très basique
            for line in html.splitlines():
                if "Pulls" in line and ">" in line:
                    text = re.sub(r"<[^>]+>", " ", line)
                    text = " ".join(text.split())
                    if not text:
                        continue
                    parts = text.split()
                    name = parts[0]
                    sizes = [tok.lower() for tok in parts if SIZE_RE.match(tok.lower())]
                    try:
                        first_special = parts.index(sizes[0]) if sizes else len(parts)
                        first_special = min(first_special, parts.index("Pulls"))
                    except ValueError:
                        first_special = len(parts)
                    description = " ".join(parts[1:first_special])
                    items.append({"name": name.lower(), "sizes": sizes, "description": description})
        return items

    def fetch_ollama_models(self, *, refresh: bool = False):
        """Retourne la liste de modèles depuis le site. Mise en cache en session."""
        ss = st.session_state
        if not refresh and ss["ollama_models_cache"] is not None:
            return ss["ollama_models_cache"]

        try:
            models = self._scrape_library()
            # Tri par popularité : plus de tailles → plus haut
            models.sort(key=lambda m: (-len(m["sizes"]), m["name"]))
            ss["ollama_models_cache"] = models
            return models
        except Exception as e:
            st.sidebar.error(str(e))
            # Fallback minimal si scraping KO
            return [
                {
                    "name": "llama3",
                    "sizes": ["8b", "70b"],
                    "description": "Meta Llama 3",
                }
            ]

    #######################################
    # Utilitaires divers
    #######################################
    def gen_name(self, prompt: str, max_len: int = 20) -> str:
        text = prompt.strip() or "Nouv. conv"
        words = text.split()[:5]
        name = " ".join(words)[:max_len] + ("..." if len(text) > max_len else "")
        return name.capitalize()

    def format_prompt(self, msgs, p_context: str = prompt_context) -> str:
        formatted = p_context
        for msg in msgs:
            role = "User" if msg["role"] == "user" else "Assistant"
            formatted += f"{role}: {msg['content']}\n"
        return formatted

    def process_thinking_response(self, resp: str):
        start_tag, end_tag = "<THINKING>", "</THINKING>"
        has_thinking = start_tag in resp and end_tag in resp
        thinking, final_response = "", resp
        if has_thinking:
            thinking = resp.split(start_tag)[1].split(end_tag)[0].strip()
            final_response = resp.split(end_tag, 1)[1].strip() or "(réponse vide)"
        return {"has_thinking": has_thinking, "thinking": thinking, "final_response": final_response}

    #######################################
    # Sidebar
    #######################################
    def _sidebar(self):
        st.sidebar.title("Conversations")

        # ---- Téléchargement de nouveaux modèles -------------------------
        with st.sidebar.expander("Bibliothèque Ollama", expanded=False):
            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button("↻", help="Rafraîchir la liste depuis ollama.ai"):
                    st.session_state["ollama_models_cache"] = None

            models = self.fetch_ollama_models()
            if not models:
                st.warning("Impossible de récupérer la bibliothèque.")
                return

            selected_model_name = st.selectbox(
                "Modèle distant",
                options=[m["name"] for m in models],
                format_func=lambda x: x.capitalize(),
            )
            model_info = next(m for m in models if m["name"] == selected_model_name)
            st.info(model_info["description"] or "(Pas de description)")
            selected_size = st.selectbox("Paramètres", model_info["sizes"])
            full_model = f"{selected_model_name}:{selected_size}"

            if st.button("Télécharger ➡️"):
                try:
                    with st.spinner(f"Téléchargement de {full_model} …"):
                        progress = st.progress(0)
                        status = st.empty()
                        for p in ollama.pull(full_model, stream=True):
                            if p.get("status"):
                                status.text(p["status"])
                            if p.get("completed") and p.get("total"):
                                percent = int(p["completed"] / p["total"] * 100)
                                progress.progress(percent)
                    st.success("Modèle téléchargé ✅")
                    self._load_models()
                except Exception as e:
                    st.error(f"Erreur : {e}")

        # ---- Gestion des conversations ----------------------------------
        if st.sidebar.button("Nouvelle conversation"):
            ss = st.session_state
            ss["convs"].append(
                {"name": f"Conv {len(ss['convs']) + 1}", "msgs": [{"role": "assistant", "content": "Bonjour!"}]}
            )
            ss["idx"] = len(ss["convs"]) - 1

        names = [c["name"] for c in st.session_state["convs"]]
        if names:
            st.session_state["idx"] = st.sidebar.radio("Choisir conv", range(len(names)), index=st.session_state["idx"], format_func=lambda i: names[i])
        else:
            st.sidebar.info("Aucune conversation.")

    #######################################
    # Zone principale (chat)
    #######################################
    def _chat_ui(self):
        logo_path = "assets/logo.svg"
        if os.path.exists(logo_path):
            st.image(logo_path, width=200)

        if not st.session_state["convs"]:
            st.info("Créez ou choisissez une conversation.")
            return

        conv = st.session_state["convs"][st.session_state["idx"]]
        conv_id = f"conv_{st.session_state['idx']}"

        current_model = self.model
        supports_thinking = any(m in current_model for m in st.session_state["thinking_models"])

        for i, msg in enumerate(conv["msgs"]):
            msg_id = f"{conv_id}_msg_{i}"
            avatar = "assets/user.svg" if msg["role"] == "user" else "assets/assistant.svg"
            with st.chat_message(msg["role"], avatar=avatar):
                if msg["role"] == "assistant":
                    if not supports_thinking:
                        st.markdown(msg["content"])
                    else:
                        processed = self.process_thinking_response(msg["content"])
                        st.markdown(processed["final_response"])
                        if processed["has_thinking"]:
                            vis = st.session_state["thinking_visibility"].setdefault(msg_id, False)
                            if st.button("Afficher réflexion" if not vis else "Masquer réflexion", key=f"{msg_id}_toggle"):
                                st.session_state["thinking_visibility"][msg_id] = not vis
                                st.rerun()
                            if vis:
                                st.markdown("---")
                                st.markdown("**Réflexion :**")
                                st.code(processed["thinking"], language="markdown")
                else:
                    st.markdown(msg["content"])

        # --------- Entrée utilisateur ------------------------------------
        if prompt := st.chat_input("Votre message"):
            conv["msgs"].append({"role": "user", "content": prompt})
            with st.chat_message("user", avatar="assets/user.svg"):
                st.markdown(prompt)

            if conv["name"].startswith("Conv"):
                conv["name"] = self.gen_name(prompt)

            full_prompt = self.format_prompt(conv["msgs"])
            with st.chat_message("assistant", avatar="assets/assistant.svg"):
                with st.spinner("En train de réfléchir …"):
                    resp = LLMs([{"role": "user", "content": full_prompt}], current_model)

                if not supports_thinking:
                    st.markdown(resp)
                else:
                    processed = self.process_thinking_response(resp)
                    st.markdown(processed["final_response"])
                    if processed["has_thinking"]:
                        new_msg_id = f"{conv_id}_msg_{len(conv['msgs'])}"
                        st.session_state["thinking_visibility"][new_msg_id] = False
                        if st.button("Afficher réflexion", key=f"{new_msg_id}_toggle"):
                            st.session_state["thinking_visibility"][new_msg_id] = True
                            st.rerun()

            conv["msgs"].append({"role": "assistant", "content": resp})

    #######################################
    # Exécution
    #######################################
    def run(self):
        self._sidebar()
        self._chat_ui()


if __name__ == "__main__":
    ChatApp().run()
