import streamlit as st
from moteur import rechercher
from datetime import datetime, timedelta

# Configuration de la page avec un thème plus professionnel
st.set_page_config(
    page_title="KIBAARE | Moteur de Recherche Académique",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "KIBAARE - Moteur de recherche académique"
    }
)

# CSS personnalisé pour un look plus professionnel et responsive
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        letter-spacing: -0.011em;
    }
    
    .main {
        padding: 1rem;
        color: #202124;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* Style du conteneur principal */
    .block-container {
        max-width: 1000px !important;
        margin-left: auto !important;
        margin-right: auto !important;
        padding-top: 2rem !important;
    }
    
    /* Style de la barre latérale */
    .sidebar .sidebar-content {
        max-width: 300px;
        margin: 0 auto;
    }
    
    .stTitle {
        color: #1a73e8;
        font-size: 2rem !important;
        padding-bottom: 1rem;
        font-weight: 600;
        letter-spacing: -0.02em;
    }
    
    .stSelectbox, .stMultiSelect {
        background-color: white;
        margin-bottom: 0.5rem;
        font-size: 0.95rem;
    }
    .search-container {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem auto 2rem auto;
        max-width: 800px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .sidebar .block-container {
        padding: 0.2rem 0.5rem;
    }
    
    /* Style des colonnes */
    div[data-testid="column"] {
        padding: 0 0.5rem;
    }
    /* Styles responsifs */
    @media (max-width: 768px) {
        .main {
            padding: 0.5rem;
        }
        .search-container {
            padding: 0.75rem;
        }
        .stTitle {
            font-size: 0.5rem !important;
        }
    }
    /* Réduction des espacements */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    div[data-testid="stVerticalBlock"] > div {
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
    }
    .stMarkdown {
        margin-top: 0.2rem;
        margin-bottom: 0.2rem;
    }
    hr {
        margin: 0.5rem 0;
    }
    /* Style des résultats */
    .result-card {
        border: 1px solid #dadce0;
        border-radius: 8px;
        padding: 1.25rem;
        margin: 0 auto 1.25rem auto;
        background-color: #ffffff;
        box-shadow: 0 1px 2px rgba(0,0,0,0.08);
        transition: box-shadow 0.2s ease;
        max-width: 850px;
    }
    
    .result-card:hover {
        box-shadow: 0 2px 8px rgba(0,0,0,0.12);
    }
    
    .result-card h3 {
        margin: 0 0 0.75rem 0;
        font-size: 1.15rem;
        font-weight: 500;
        line-height: 1.4;
        color: #1a73e8;
    }
    
    .result-card h3 a:hover {
        text-decoration: underline !important;
    }
    
    .result-meta {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-bottom: 0.7rem;
    }
    
    .meta-tag {
        background-color: #f1f3f4;
        padding: 0.4rem 0.8rem;
        border-radius: 16px;
        font-size: 0.875rem;
        color: #3c4043;
        font-weight: 500;
        white-space: nowrap;
        letter-spacing: 0;
    }
    </style>
""", unsafe_allow_html=True)

# En-tête style Google
st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h1 style="color: #1a73e8; font-size: 2.5rem; margin: 0; font-weight: 50; letter-spacing: -0.02em;">KIBAARE</h1>
        <p style="color: #5f6368; font-size: 1.1rem; margin: 0.002rem 0; font-weight: 100;">Moteur de Recherche Académique</p>
    </div>
""", unsafe_allow_html=True)

# Barre latérale améliorée
with st.sidebar:
    st.markdown("<div style='margin-bottom:0.5rem;'><span style='font-size:1.1rem;font-weight:600;'>🔍 Filtres de recherche</span></div>", unsafe_allow_html=True)
    fields = st.multiselect(
        "📚 Chercher dans",
        ["title", "authors", "abstract", "keywords"],
        default=["title", "authors", "abstract", "keywords"]
    )
    st.markdown("<div></div>", unsafe_allow_html=True)
    st.markdown("### 📅 Période", unsafe_allow_html=True)
    date_range = st.date_input(
        "Sélectionnez une période",
        value=None
    )
    st.markdown("<div></div>", unsafe_allow_html=True)
    st.markdown("### 🌐 Langue", unsafe_allow_html=True)
    language = st.selectbox(
        "Sélectionnez une langue",
        ["Toutes", "Français (FR)", "English (EN)"]
    )
    st.markdown("<div></div>", unsafe_allow_html=True)
    st.markdown("### ⚙️ Options de tri", unsafe_allow_html=True)
    sort_by = st.radio(
        "Trier les résultats par",
        ["Pertinence", "Date de publication"]
    )

# Zone de recherche principale dans un containeur
with st.container():
    st.markdown("<div class='search-container'>", unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        query = st.text_input(
            "🔍 Rechercher",
            placeholder="Ex: intelligence artificielle, machine learning..."
        )
    with col2:
        limit = st.number_input(
            "Nombre de résultats",
            min_value=5,
            max_value=100,
            value=20
        )
    
    search_col1, search_col2, search_col3 = st.columns([2, 1, 2])
    with search_col2:
        search_button = st.button("🔍 Rechercher", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Fonction d'affichage des résultats
if search_button:
    # Préparation des filtres
    filters = {}
    
    if language != "Toutes":
        # Extraction du code de langue entre parenthèses
        if "(" in language and ")" in language:
            lang_code = language.split("(")[1].split(")")[0].lower()
        else:
            lang_code = language.lower()
        filters["language"] = lang_code

    # Conversion et validation des dates
    if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
        start_date = datetime.combine(date_range[0], datetime.min.time())
        end_date = datetime.combine(date_range[1], datetime.max.time())
        if start_date > end_date:
            start_date, end_date = end_date, start_date
        filters["date_range"] = (start_date, end_date)

    # Vérification de la requête
    if not query.strip() and not filters:
        st.warning("⚠️ Veuillez entrer une requête ou sélectionner des filtres.")
    else:
        try:
            with st.spinner("🔍 Recherche en cours..."):
                resultats = rechercher(
                    query=query,
                    fields=fields,
                    filters=filters,
                    sort_by="date" if sort_by == "Date de publication" else "score",
                    limit=limit
                )
        except Exception as e:
            st.error(f"❌ Une erreur technique est survenue lors de la recherche : {e}")
            resultats = []

        if resultats:
            st.success(f"✨ {len(resultats)} résultat(s) trouvé(s)")
            for result in resultats:
                # Traitement des valeurs
                title = result.get('title', 'Titre inconnu')
                # Nettoyage du titre (enlever les crochets et guillemets)
                if isinstance(title, list):
                    title = ", ".join(title)
                title = title.strip("[]'")
                
                authors = result.get('authors', 'Auteur(s) inconnu(s)')
                if isinstance(authors, list):
                    authors = ", ".join(authors)
                
                pub_date = result.get('pub_date', '')
                formatted_date = pub_date.strftime("%d/%m/%Y") if isinstance(pub_date, datetime) else "Date inconnue"
                
                language = result.get('language', '?')
                if isinstance(language, list):
                    language = ", ".join(language)
                
                keywords = result.get('keywords', 'Aucun mot-clé')
                if isinstance(keywords, list):
                    keywords = ", ".join(keywords)
                
                abstract = result.get('abstract', 'Résumé non disponible')
                if isinstance(abstract, list):
                    abstract = " ".join(abstract)
                
                url = result.get('url', '#')

                # Affichage du résultat avec le template HTML responsive
                st.markdown(f"""
                <div class="result-card">
                    <h3>
                        <a href="{url}" target="_blank" style="color:#1a4d8f; text-decoration:none; font-weight:600;">
                            {title}
                        </a>
                    </h3>
                    <div class="result-meta">
                        <span class="meta-tag" style="white-space:pre-line;word-break:break-word;max-width:350px;overflow-wrap:break-word;">
                            👥 {authors}
                        </span>
                        <span class="meta-tag">📅 {formatted_date}</span>
                        <span class="meta-tag">🌐 {language.upper()}</span>
                    </div>
                    <div style="margin: 0.5rem 0;">
                        <p style="color:#666; line-height:1.4; margin: 0; font-size: 0.9rem;">
                            {abstract}
                        </p>
                    </div>
                    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem; font-size:0.9rem;">
                        <div style="color:#1976d2;">
                            🏷️ {keywords}
                        </div>
                        <a href="{url}" target="_blank" style="color:#1a4d8f; text-decoration:none;">
                            📎 Voir le document
                        </a>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error("❌ Aucun document ne correspond à votre recherche.")
