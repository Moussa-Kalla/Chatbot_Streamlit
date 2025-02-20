# LLM Chatbot avec Ollama et Streamlit

Ce projet est un chatbot basé sur **Ollama** et **Streamlit** qui permet d'interagir avec un modèle **LLM** comme llama3.2.

## 📁 Structure du projet
```bash
llm/
│── app/                            
│   ├── chat.py          
│   └── main.py         
│── requirements.txt 
│── README.md
│── app_screeshoot.png          
└── .gitignore
```

## Aperçu du Projet

liens d'accès :  [Kalla-chat.streamlit.app](Kalla-chat.streamlit.app)

![Aperçu du projet](https://github.com/Moussa-Kalla/LLM/blob/master/app_screeshoot.png?raw=true)  


##  Installation et Exécution

1. **Cloner le projet** :
```bash
git clone hhttps://github.com/Moussa-Kalla/LLM
```
2. **Installer les dépendances** :
```bash
pip install -r requirements.txt
```
3. **Lancer l’application** :
```bash
streamlit run app/main.py
```

## Technologies utilisées
-	[Ollama](https://ollama.com/) → Exécution du modèle de LLM
-	[streamlit](https://streamlit.io/) → Interface web

## ✨ Fonctionnalités

- Poser des questions au chatbot 
- Obtenir des réponses du modèle Llama3.2:1b
