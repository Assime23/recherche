import streamlit as st
from moteur import rechercher
from datetime import datetime, timedelta

st.set_page_config(page_title="Moteur de Recherche Académique", layout="wide", initial_sidebar_state="expanded")
st.title("🔍 Moteur de Recherche Académique KIBAARE")

# Barre latérale pour les filtres
with st.sidebar:
    st.header("Filtres de recherche")
    
    # Sélection des champs
    fields = st.multiselect(
        "Chercher dans",
        ["title", "authors", "abstract", "keywords"],
        default=["title", "authors", "abstract", "keywords"]
    )
    
    # Filtre de date
    date_range = st.date_input(
        "Période de publication",
        value=None
    )
    
    # Filtre de langue
    language = st.selectbox("Langue", ["Toutes", "French", "English"])
    
    # Tri
    sort_by = st.radio("Trier par", ["Pertinence", "Date"])

# Zone de recherche principale
col1, col2 = st.columns([3, 1])
with col1:
    query = st.text_input("Entrez vos mots-clés", placeholder="ex: apprentissage profond, bioinformatique...")
with col2:
    limit = st.number_input("Nombre de résultats", min_value=5, max_value=100, value=20)

# Bouton de recherche
if st.button("Rechercher"):
    if not query.strip():
        st.warning("Veuillez entrer une requête avant de lancer la recherche.")
    else:
        # Préparation des filtres
        filters = {}
        if language != "Toutes":
            filters["language"] = language

        # Conversion explicite des dates en datetime
        if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
            start_date = datetime.combine(date_range[0], datetime.min.time())
            end_date = datetime.combine(date_range[1], datetime.max.time())
            filters["date_range"] = (start_date, end_date)

        # Exécution de la recherche
        resultats = rechercher(
            query=query,
            fields=fields,
            filters=filters,
            sort_by="date" if sort_by == "Date" else "score",
            limit=limit
        )

        if resultats:
            st.success(f"{len(resultats)} résultat(s) trouvé(s)")
            for result in resultats:
                # Valeurs par défaut et gestion des listes
                title = result.get('title', 'Titre inconnu')
                authors = result.get('authors', '')
                if isinstance(authors, list):
                    authors = ", ".join(authors)
                if not authors:
                    authors = "Auteur(s) inconnu(s)"
                pub_date = result.get('pub_date', '')
                if not pub_date or str(pub_date).startswith("2000"):
                    pub_date = "Date inconnue"
                language = result.get('language', '')
                if isinstance(language, list):
                    language = ", ".join(language)
                if not language:
                    language = "?"
                keywords = result.get('keywords', '')
                if isinstance(keywords, list):
                    keywords = ", ".join(keywords)
                if not keywords:
                    keywords = "Aucun"
                abstract = result.get('abstract', '')
                if isinstance(abstract, list):
                    abstract = " ".join(abstract)
                if not abstract:
                    abstract = "Non renseigné"
                score = result.get('score', 0)
                url = result.get('url', '#')

                st.markdown(f"""
<div style="border:1px solid #e0e0e0; border-radius:8px; padding:18px; margin-bottom:18px; background-color:#fafbfc;">
    <h4 style="margin-bottom:0.2em;">
        <a href="{url}" target="_blank" style="color:#1a4d8f; text-decoration:none;">
            {title}
        </a>
    </h4>
    <div style="color:#555; font-size:0.95em; margin-bottom:0.5em;">
        <b>Auteurs :</b> {authors}
        <span style="margin-left:1em;"><b>Date :</b> {pub_date}</span>
        <span style="margin-left:1em;"><b>Langue :</b> {language.upper()}</span>
    </div>
    <div style="margin-bottom:0.5em;">
        <b>Mots-clés :</b>
        <span style="color:#1976d2;">{keywords}</span>
    </div>
    <div style="margin-bottom:0.5em;">
        <b>Résumé :</b>
        <span style="color:#333;">{abstract}</span>
    </div>
    <div style="font-size:0.9em; color:#888;">
        <b>Score de pertinence :</b> {score:.2f} &nbsp; | &nbsp;
        <a href="{url}" target="_blank">🔗 Consulter le document original</a>
    </div>
</div>
""", unsafe_allow_html=True)
        else:
            st.error("❌ Aucun document ne correspond à votre recherche.")
