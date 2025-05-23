from whoosh.fields import Schema, TEXT, KEYWORD, ID, DATETIME
from whoosh.analysis import StemmingAnalyzer
from whoosh.index import create_in
import os
import json
from datetime import datetime

def parse_date(date_str: str) -> datetime:
    """Analyse différents formats de date possibles"""
    formats = [
        "%Y-%m-%d",  # 2023-01-01
        "%Y",        # 2023
        "%Y-%m",     # 2023-01
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except Exception:
            continue
            
    # Si aucun format ne correspond, retourne une date par défaut
    return datetime(2000, 1, 1)

# Schéma amélioré
schema = Schema(
    docid=ID(stored=True, unique=True),
    title=TEXT(stored=True, analyzer=StemmingAnalyzer()),
    authors=TEXT(stored=True),
    abstract=TEXT(stored=True, analyzer=StemmingAnalyzer()),
    keywords=KEYWORD(stored=True, commas=True, lowercase=True),
    pub_date=DATETIME(stored=True),
    journal=TEXT(stored=True),
    language=TEXT(stored=True),
    url=ID(stored=True)
)

def index_data(data_directory: str = "data"):
    """Indexe tous les fichiers JSON du répertoire data"""
    if not os.path.exists("index"):
        os.mkdir("index")
    
    ix = create_in("index", schema)
    writer = ix.writer()
    total_docs = 0

    try:
        for file in os.listdir(data_directory):
            if file.endswith('.json'):
                with open(os.path.join(data_directory, file), "r", encoding="utf-8") as f:
                    data = json.load(f)
                    docs = data.get("documents", []) if isinstance(data, dict) else data

                    for doc in docs:
                        # Champs HAL robustes
                        title = " ".join(doc.get("title_s", [])) if isinstance(doc.get("title_s", []), list) else doc.get("title_s", "") or "Sans titre"
                        authors = ", ".join(doc.get("authFullName_s", [])) if isinstance(doc.get("authFullName_s", []), list) else doc.get("authFullName_s", "") or "Auteur inconnu"
                        abstract = " ".join(doc.get("abstract_s", [])) if isinstance(doc.get("abstract_s", []), list) else doc.get("abstract_s", "")
                        keywords = ", ".join(doc.get("keyword_s", [])) if isinstance(doc.get("keyword_s", []), list) else doc.get("keyword_s", "")
                        language = ", ".join(doc.get("language_s", [])) if isinstance(doc.get("language_s", []), list) else doc.get("language_s", "")
                        journal = doc.get("journalTitle_s", "")
                        url = doc.get("uri_s", "")
                        date_str = doc.get("publicationDate_s", "2000-01-01")
                        pub_date = parse_date(date_str)
                        docid = doc.get("docid", "")

                        try:
                            writer.add_document(
                                docid=docid,
                                title=title,
                                authors=authors,
                                abstract=abstract,
                                keywords=keywords,
                                pub_date=pub_date,
                                journal=journal,
                                language=language,
                                url=url
                            )
                            total_docs += 1
                        except Exception as e:
                            print(f"Erreur lors de l'indexation du document {docid}: {e}")
                            continue

        writer.commit()
        print(f"Indexation terminée avec succès. {total_docs} documents indexés.")
    except Exception as e:
        print(f"Erreur lors de l'indexation: {e}")
        writer.cancel()

if __name__ == "__main__":
    index_data()
