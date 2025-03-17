# LLM Chatbot avec l'API d'OpenAI et Streamlit

Ce projet est un chatbot intelligent qui permet d’interagir avec des modèles de LLM (Large Language Models) qui reflètent ma propre personnalité via une interface web conviviale développée avec Streamlit.

## 📁 Structure du projet

```bash
llm/
│── .devcontainer/
│   └──  devcontainer.json
├── assets/
│   ├── assistant.png
│   ├── app_screeshoot.gif
│   ├── logo.png  
│   └── user.png 
│── app/         
│   ├── chat.py
│   ├── main.py  
│   └── prompt.py   
│── Dockerfile     
│── requirements.txt 
│── README.md     
└── .gitignore
```

## Aperçu du Projet

Liens d'accès : [https://moussa-gpt.streamlit.app/](https://moussa-gpt.streamlit.app/)

![Aperçu du projet](https://github.com/Moussa-Kalla/Chatbot_Streamlit/blob/master/assets/app_screeshoot.gif?raw=true)  


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


Merci pour votre visite, et surtout, n’hésitez pas à me laisser une petite étoile sur le repo ! J’aime collectionner les étoiles autant que j’aime coder.

