# LLM Chatbot avec l'API d'OpenAI et Streamlit

Ce projet est un chatbot intelligent qui permet d’interagir avec des modèles de LLM (Large Language Models) qui reflètent ma propre personnalité via une interface web conviviale développée avec Streamlit.

## 📁 Structure du projet

```bash
llm/
│── .devcontainer/
│   └──  devcontainer.json
├── assets/
│   ├── assistant.png
│   ├── logo.png  
│   └── user.png 
│── app/         
│   ├── chat.py
│   ├── main.py          
│   └── prompt.py       
│── requirements.txt 
│── README.md
│── app_screeshoot.png          
└── .gitignore
```

## Aperçu du Projet

Liens d'accès : [https://moussa-gpt.streamlit.app/](https://moussa-gpt.streamlit.app/)

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
-	[OpenAI](https://platform.openai.com/) → API d'OpenAI
-	[Streamlit](https://streamlit.io/) → Interface web

## Fonctionnalités

- Poser des questions au chatbot 
- Obtenir des réponses du modèle Gpt4o 
