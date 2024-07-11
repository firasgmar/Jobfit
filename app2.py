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
def main():
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

            # Ajouter des champs de recherche
            search_name = st.text_input("Rechercher par nom")
            search_email = st.text_input("Rechercher par email")

            if search_name or search_email:
                search_results = df[
                    df['name'].str.contains(search_name, case=False, na=False) &
                    df['email'].str.contains(search_email, case=False, na=False)
                ]
                st.write("Résultats de la recherche")
                st.dataframe(search_results[['name', 'contact_number', 'email']])
            else:
                search_results = df

            st.write("Sélectionnez une personne pour afficher les détails")

            # Sélectionner une personne pour afficher les détails
            selected_name = st.selectbox("Sélectionnez une personne", search_results['name'])

            if selected_name:
                st.session_state['selected_person'] = df[df['name'] == selected_name].iloc[0].to_dict()
                st.session_state['page'] = 'details'

        except Exception as e:
            st.error(f"Erreur lors du chargement des fichiers : {e}")
    else:
        st.write("Veuillez entrer le chemin du dossier contenant les fichiers JSON")

def details():
    if 'selected_person' in st.session_state:
        person_details = st.session_state['selected_person']
        st.title(f"Détails de {person_details['name']}")
        
        def colored_text(label, value, color):
            return f'<p style="color:{color};">{label}: {value}</p>'
        
        st.markdown(colored_text("Nom", person_details.get('name', ''), "blue"), unsafe_allow_html=True)
        st.markdown(colored_text("Numéro de contact", person_details.get('contact_number', ''), "green"), unsafe_allow_html=True)
        st.markdown(colored_text("Email", person_details.get('email', ''), "red"), unsafe_allow_html=True)
        
        st.markdown("<p style='color:purple;'>Outils:</p>", unsafe_allow_html=True)
        for tool in person_details.get('Tools', []):
            st.markdown(f"<p style='color:black;'>{tool}</p>", unsafe_allow_html=True)
        
        st.markdown("<p style='color:purple;'>Compétences:</p>", unsafe_allow_html=True)
        for skill in person_details.get('skills', []):
            st.markdown(f"<p style='color:black;'>{skill}</p>", unsafe_allow_html=True)
        
        st.markdown("<p style='color:purple;'>Description du profil:</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:black;'>{person_details.get('Profile_description', '')}</p>", unsafe_allow_html=True)
        
        st.markdown("<p style='color:purple;'>Niveaux d'éducation:</p>", unsafe_allow_html=True)
        for edu in person_details.get('education_levels', []):
            st.markdown(f"<p style='color:black;'>{edu['establishment']} - {edu['level']} ({edu['start_year']})</p>", unsafe_allow_html=True)
        
        st.markdown("<p style='color:purple;'>Expérience professionnelle:</p>", unsafe_allow_html=True)
        for exp in person_details.get('Professional_experience', []):
            st.markdown(f"<p style='color:black;'>{exp['establishment']} - {exp['job']} ({exp['start_year']} - {exp['end_year']})</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:black;'>{exp['description']}</p>", unsafe_allow_html=True)
        
        st.markdown(colored_text("Langues", ", ".join(person_details.get('Languages', [])), "blue"), unsafe_allow_html=True)
        st.markdown(colored_text("Réalisations", person_details.get('Achievements', ''), "blue"), unsafe_allow_html=True)
        st.markdown(colored_text("CV Texte", person_details.get('Text_CV', ''), "blue"), unsafe_allow_html=True)
        st.markdown(colored_text("Emploi recommandé", person_details.get('Job_recommended', ''), "blue"), unsafe_allow_html=True)

        if st.button("Retour"):
            st.session_state['page'] = 'main'
    else:
        st.write("Aucune personne sélectionnée.")

# Gérer la navigation entre les pages
if 'page' not in st.session_state:
    st.session_state['page'] = 'main'

if st.session_state['page'] == 'main':
    main()
elif st.session_state['page'] == 'details':
    details()
