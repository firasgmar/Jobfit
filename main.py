import streamlit as st
import pandas as pd
import os
import json

# Fonction pour charger les fichiers JSON
def load_json_files(directory):
    data = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
                data.append(json.load(f))
    return data

# Interface utilisateur avec Streamlit
st.title("Application de gestion des CV")

# Renseigner le dossier contenant les fichiers JSON
directory = st.text_input("Entrez le chemin du dossier contenant les fichiers JSON")

if directory:
    try:
        # Charger les fichiers JSON
        json_data = load_json_files(directory)
        # Créer un DataFrame
        df = pd.json_normalize(json_data)
        # Afficher la liste des personnes dans un tableau
        st.write("Liste des personnes")
        st.dataframe(df[['name', 'contact_number', 'email']])


        search_results = df
        st.write("Sélectionnez une personne pour afficher les détails")

        # Sélectionner une personne pour afficher les détails
        selected_name = st.selectbox("Sélectionnez une personne", search_results['name'])

        if selected_name:
            person_details = df[df['name'] == selected_name].iloc[0]
            st.write("Détails de la personne")
            st.json(person_details.to_dict())

    except Exception as e:
        st.error(f"Erreur lors du chargement des fichiers : {e}")
else:
    st.write("Veuillez entrer le chemin du dossier contenant les fichiers JSON")
