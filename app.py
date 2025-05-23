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

# Basic CSS styling
st.markdown("""
    <style>
    html, body, .block-container, .main, .search-container {
        background: #fff !important;
        color: #202124 !important;
    }
    .block-container {
        max-width: 1000px;
        margin: 0 auto;
        padding: 20px;
    }
    
    .search-container {
        background: #f8f9fa;
        padding: 20px;
        margin: 10px auto;
    }
    
    .result-card {
        border: 1px solid #ddd;
        padding: 15px;
        margin: 10px 0;
        background: white;
    }
    
    .result-meta {
        display: flex;
        flex-wrap: wrap;
        gap: 5px;
        margin: 10px 0;
    }
    
    .meta-tag {
        background: #f1f3f4;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 14px;
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
