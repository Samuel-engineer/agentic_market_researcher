# app.py
import logging
import streamlit as st
from src.crew import run_market_research_crew

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Configuration de la page Streamlit
st.set_page_config(
    page_title="Europe GenAI - Market Research Studio", 
    page_icon="📊", 
    layout="wide"
)

# Titre de l'application
st.title("📊 Assistant d'Étude de Marché Automatisée")
st.subheader("Propulsé par un système multi-agents autonome (CrewAI)")
st.write("Saisissez un sujet pour activer votre équipe d'agents (Chercheur, Analyste, Rédacteur).")

# Formulaire de saisie pour l'utilisateur
with st.form(key="research_form"):
    topic_input = st.text_input(
        label="Sujet de l'étude de marché :",
        placeholder="Ex: L'impact de la réglementation AI Act sur les startups de santé en Allemagne..."
    )
    submit_button = st.form_submit_button(label="Lancer l'analyse 🚀")

# Gestion du clic sur le bouton
if submit_button:
    if not topic_input.strip():
        st.warning("⚠️ Veuillez saisir un sujet valide avant de lancer l'équipe.")
    else:
        # Zone d'attente visuelle pendant que les agents travaillent
        with st.spinner("🕵️‍♂️ Le Chercheur fouille le web, l'Analyste trie les données et le Rédacteur met en forme... Cela peut prendre 1 à 2 minutes."):
            try:
                # Appel de notre fonction backend (Couche d'orchestration)
                logger.info("Lancement de l'analyse pour le sujet : %s", topic_input)
                logger.info("type(topic_input)=%s", type(topic_input))
                rapport_final = run_market_research_crew(topic_input)
                
                # Affichage du succès et du rapport au format Markdown propre
                st.success("✅ Rapport généré avec succès !")
                st.markdown("---")
                st.markdown(rapport_final)
                
            except Exception as e:
                st.error(f"❌ Une erreur est survenue lors de l'exécution du Crew : {e}")