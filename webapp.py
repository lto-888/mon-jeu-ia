import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# --- CONFIGURATION ---
st.set_page_config(page_title="Mon Studio de Jeux IA", layout="wide")

# ⚠️ COLLE TA CLÉ ICI (Entre les guillemets)
API_KEY = st.secrets["GOOGLE_API_KEY"]

# Configuration de Google Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# --- L'INTERFACE DU SITE ---
st.title("🎮 Créateur de Jeux Vidéo par IA")
st.write("Décris ton idée, et l'IA va coder et lancer le jeu instantanément !")

# Zone de texte pour l'idée
user_idea = st.text_area("Description du jeu :", height=100, placeholder="Ex: Un jeu de tir spatial où on contrôle un vaisseau bleu avec la souris...")

# Le bouton magique
if st.button("Générer le jeu 🚀", type="primary"):
    
    if not user_idea:
        st.warning("Écris une idée d'abord !")
    else:
        with st.spinner("L'IA est en train de coder ton jeu..."):
            try:
                # Le Prompt (Les ordres donnés à l'IA)
                system_prompt = """
                Tu es un expert Javascript. Crée un jeu complet dans un seul fichier HTML.
                - Utilise le Canvas HTML5.
                - Le jeu doit prendre 100% de la largeur/hauteur disponible.
                - Pas d'images externes, dessine tout avec ctx.fillRect/arc.
                - Gère les contrôles (Clavier/Souris).
                - Ajoute un bouton 'Rejouer' quand on perd.
                - Fond noir ou sombre recommandé.
                - Code uniquement, pas de markdown.
                """
                full_prompt = f"{system_prompt}\n\nJeu demandé : {user_idea}"
                
                # Appel à Gemini
                response = model.generate_content(full_prompt)
                game_code = response.text.replace("```html", "").replace("```", "")
                
                st.success("Jeu créé ! Joue ci-dessous 👇")
                
                # Affichage du jeu
                components.html(game_code, height=600, scrolling=False)
                
                # Option pour voir le code
                with st.expander("Voir le code source généré"):
                    st.code(game_code, language='html')

            except Exception as e:
                st.error(f"Une erreur est survenue : {e}")