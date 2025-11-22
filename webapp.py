import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# --- 1. CONFIGURATION DE LA PAGE (Doit être la première ligne) ---
st.set_page_config(
    page_title="AI Game Studio",
    page_icon="🕹️",
    layout="wide", # Utilise toute la largeur de l'écran
    initial_sidebar_state="expanded"
)

# --- 2. STYLE CSS PERSONNALISÉ (Pour faire beau) ---
st.markdown("""
<style>
    /* Fond global sombre et texte */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    /* Le Titre Principal */
    h1 {
        text-align: center;
        font-family: 'Courier New', monospace;
        background: -webkit-linear-gradient(45deg, #00C9FF, #92FE9D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem !important;
        font-weight: bold;
        margin-bottom: 20px;
    }
    
    /* Le bouton Générer */
    .stButton>button {
        background: linear-gradient(90deg, #FF4B4B 0%, #FF9068 100%);
        color: white;
        border: none;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        font-size: 20px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0px 0px 15px #FF4B4B;
    }

    /* Zone de code cachée */
    .streamlit-expanderHeader {
        background-color: #262730;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. CONFIGURATION API (Sécurisée) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    st.error("🚨 Erreur de clé API. Vérifie tes secrets sur Streamlit Cloud.")
    st.stop()

# --- 4. SIDEBAR (La colonne de gauche) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/5260/5260498.png", width=100)
    st.title("⚙️ Commandes")
    st.write("Configure ton futur jeu ici.")
    
    # Choix du style
    style_jeu = st.selectbox(
        "Style visuel :",
        ["Néon / Cyberpunk", "Rétro Pixel Art", "Minimaliste Noir & Blanc", "Couleurs Vives / Cartoon"]
    )
    
    # Zone de texte principale
    user_idea = st.text_area(
        "Description du jeu :",
        height=150,
        placeholder="Ex: Un jeu de course infini où j'évite des obstacles rouges..."
    )
    
    # Le Bouton Magique
    generate_btn = st.button("✨ CRÉER LE JEU")
    
    st.markdown("---")
    st.caption("Powered by Gemini 2.0 Flash & Streamlit")

# --- 5. ZONE PRINCIPALE (L'écran de jeu) ---
st.title("👾 AI GAME STUDIO")

if generate_btn:
    if not user_idea:
        st.warning("⚠️ Holà ! Il faut décrire ton jeu d'abord.")
    else:
        # On affiche une animation de chargement stylée
        with st.spinner("🧠 L'IA code tes rêves... (Compilation des pixels)"):
            try:
                # Prompt amélioré avec le style
                system_prompt = f"""
                Tu es un développeur de jeux vidéo expert (Godot/Phaser expert).
                Crée un jeu HTML5 complet dans un SEUL fichier (HTML+JS+CSS).
                
                INSTRUCTIONS VISUELLES :
                - Adopte impérativement un style : {style_jeu}.
                - Le jeu doit être beau, fluide et poli.
                
                INSTRUCTIONS TECHNIQUES :
                - Utilise le Canvas HTML5 en plein écran (width=100%, height=100%).
                - Gère les erreurs (try/catch).
                - Ajoute un écran d'accueil "Appuyez pour jouer".
                - Ajoute un écran "Game Over" avec score et bouton Rejouer stylé.
                - Pas d'images externes (dessine tout avec ctx).
                - Code uniquement, pas de markdown.
                """
                
                full_prompt = f"{system_prompt}\n\nDemande : {user_idea}"
                
                response = model.generate_content(full_prompt)
                game_code = response.text.replace("```html", "").replace("```", "")
                
                # Affichage du résultat
                st.balloons() # Petite fête quand c'est prêt
                st.success("✅ Jeu généré avec succès !")
                
                # Le jeu
                components.html(game_code, height=650, scrolling=False)
                
                # Code source
                with st.expander("🕵️ Voir le code source (pour les curieux)"):
                    st.code(game_code, language='html')

            except Exception as e:
                st.error(f"Oups, une erreur : {e}")

else:
    # Écran d'accueil quand on arrive sur le site
    st.info("👈 Utilise le menu à gauche pour commencer à créer !")
    st.markdown("""
    ### Comment ça marche ?
    1. Choisis un **style visuel**.
    2. Décris ton idée dans la case.
    3. Clique sur **Créer**.
    4. Joue directement sur cette page !
    """)