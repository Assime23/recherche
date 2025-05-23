import os
import json
from datetime import datetime
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID, KEYWORD, DATETIME
from whoosh.analysis import StemmingAnalyzer

# Définition du schéma d'indexation
schema = Schema(
    docid=ID(stored=True, unique=True),
    title=TEXT(stored=True, analyzer=StemmingAnalyzer()),
    authors=TEXT(stored=True),
    abstract=TEXT(stored=True, analyzer=StemmingAnalyzer()),
    keywords=KEYWORD(stored=True, commas=True, lowercase=True),
    pub_date=DATETIME(stored=True),
    journal=TEXT(stored=True),
    language=KEYWORD(stored=True, commas=True, lowercase=True),
    url=ID(stored=True)
)

def index_data(data_directory: str = None):
    """Indexe tous les fichiers JSON du répertoire data"""
    # Utiliser le chemin absolu pour le dossier data
    if data_directory is None:
        data_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    
    # Créer les dossiers nécessaires
    os.makedirs(data_directory, exist_ok=True)
    index_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index")
    os.makedirs(index_dir, exist_ok=True)

    ix = create_in(index_dir, schema)
    writer = ix.writer(procs=4, limitmb=256)
    total_docs = 0

    try:
        if not os.path.exists(data_directory) or not os.listdir(data_directory):
            print(f"Aucun fichier à indexer dans {data_directory}")
            return

        for file in os.listdir(data_directory):
            if file.endswith('.json'):
                try:
                    with open(os.path.join(data_directory, file), "r", encoding="utf-8") as f:
                        data = json.load(f)
                        docs = data.get("documents", []) if isinstance(data, dict) else data
                        
                        for doc in docs:
                            title = doc.get("title_s", "") or "Sans titre"
                            authors = ", ".join(doc.get("authFullName_s", [])) if isinstance(doc.get("authFullName_s", []), list) else doc.get("authFullName_s", "")
                            abstract = " ".join(doc.get("abstract_s", [])) if isinstance(doc.get("abstract_s", []), list) else doc.get("abstract_s", "")
                            keywords = doc.get("keyword_s", "")
                            language = ", ".join(doc.get("language_s", [])) if isinstance(doc.get("language_s", []), list) else doc.get("language_s", "")
                            journal = doc.get("journalTitle_s", "")
                            url = doc.get("uri_s", "")
                            docid = doc.get("docid", "")

                            # Conversion de la date
                            try:
                                pub_date = datetime.strptime(doc.get("publicationDate_s", ""), "%Y-%m-%d")
                            except (ValueError, TypeError):
                                pub_date = datetime(2000, 1, 1)  # Date par défaut

                            writer.add_document(
                                docid=docid,
                                title=title,
                                authors=authors,
                                abstract=abstract,
                                keywords=keywords,
                                journal=journal,
                                pub_date=pub_date,
                                language=language,
                                url=url
                            )
                            total_docs += 1

                except Exception as e:
                    print(f"Erreur lors de l'indexation du document: {e}")
                    continue

        writer.commit()
        print(f"Indexation terminée avec succès. {total_docs} documents indexés.")

    except Exception as e:
        print(f"Erreur lors de l'indexation: {e}")
        writer.cancel()

if __name__ == "__main__":
    index_data()
