# Sprint S2 - Dashboard Analytique Streamlit 

Ce projet est un tableau de bord interactif développé avec Python, Streamlit et Plotly. Il permet d'explorer les indicateurs socio-économiques (Population, Consommation, Énergie) de 54 pays africains

# Installation et exécution

1. **Créer et activer l'environnement virtuel :**
   python3 -m venv env
   source env/bin/activate

# Installer les dépendances :
pip install streamlit plotly pandas

# Lancer l'application :
streamlit run app.py

# Structure du projet
app.py : Script principal du dashboard interactif Streamlit

dataset_afrique.csv : Données nettoyées (valeurs manquantes imputées par la médiane, outliers traités via la méthode IQR)

INSIGHTS.md : 5 conclusions analytiques clés tirées de l'exploration des données