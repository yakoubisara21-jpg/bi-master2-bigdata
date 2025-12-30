Description :
Dashboard réalisé avec Python interactif pour analyser les commandes livrées et non livrées.
Affiche les KPI, 5 graphiques principaux et un tableau récapitulatif.

Prérequis :
Python 3.9 ou plus récent
pip (gestionnaire de packages Python)

Structure du dossier :

dashboard python/
├── app.py
├── requirements.txt
└── data/
    ├── Dim_Temps.csv
    ├── TF_Commande.csv
    ├── Dim_Employee.csv
    └── Dim_Client.csv

Installation:
1. Télécharger le code
Téléchargez le fichier app.py et placez-le dans un dossier.

2. Préparer les données
Créez un dossier data dans le même dossier que le script. Placez-y vos 4 fichiers CSV :
Dim_Temps.csv
TF_Commande.csv
Dim_Employee.csv
Dim_Client.csv

3. Installer les dépendances
-Ouvrez un terminal et exécutez :

pip install streamlit pandas plotly
ou bien:
pip install requirements.txt

-Exécution et Lancement du dashboard dans le terminal:
streamlit run app.py

-Accès au dashboard :
Ouvrez votre navigateur et allez à l'adresse :
http://localhost:8501