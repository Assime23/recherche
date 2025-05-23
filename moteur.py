from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser, QueryParser
from whoosh.query import DateRange
from whoosh.sorting import FieldFacet, ScoreFacet
from typing import Dict, List
import logging

def rechercher(query: str, 
              fields: List[str] = None,
              filters: Dict = None,
              sort_by: str = "score",
              limit: int = 20,
              fuzzy_distance: int = 2) -> List[Dict]:
    """
    Recherche avancée avec filtres et tri, supporte la recherche floue
    fuzzy_distance : niveau de tolérance aux fautes (2 ou 3)
    """
    try:
        ix = open_dir("index")
    except Exception as e:
        logging.error(f"Erreur lors de l'ouverture de l'index : {e}")
        return []
    
    if fields is None:
        fields = ["title", "authors", "abstract", "keywords"]

    # Ajout automatique du fuzzy (~fuzzy_distance) à chaque mot de la requête
    fuzzy_distance = max(1, min(fuzzy_distance, 3))  # sécurité
    try:
        fuzzy_query = " ".join([f"{mot}~{fuzzy_distance}" for mot in query.split()])
        parser = MultifieldParser(fields, schema=ix.schema)
        q = parser.parse(fuzzy_query)
    except Exception as e:
        logging.error(f"Erreur lors de la construction de la requête : {e}")
        return []

    # Application des filtres
    if filters:
        try:
            for field, value in filters.items():
                if field == "date_range":
                    q = q & DateRange("pub_date", value[0], value[1])
                elif field == "language":
                    from whoosh.query import Term, Or
                    lang_variations = [
                        value,
                        value.upper(),
                        value.lower(),
                        value.capitalize(),
                    ]
                    lang_query = Or([Term("language", v) for v in lang_variations])
                    q = q & lang_query
                elif field in ix.schema:
                    field_parser = QueryParser(field, schema=ix.schema)
                    q = q & field_parser.parse(value)
        except Exception as e:
            logging.error(f"Erreur lors de l'application des filtres : {e}")
            return []

    # Configuration du tri
    sorting = None
    if sort_by == "date":
        sorting = FieldFacet("pub_date", reverse=True)
    elif sort_by == "score":
        sorting = ScoreFacet()

    results = []
    try:
        with ix.searcher() as searcher:
            hits = searcher.search(q, limit=limit, sortedby=sorting)
            for hit in hits:
                results.append({
                    "docid": hit["docid"],
                    "title": hit["title"],
                    "authors": hit["authors"],
                    "abstract": hit.get("abstract", ""),
                    "keywords": hit.get("keywords", ""),
                    "journal": hit.get("journal", ""),
                    "pub_date": hit.get("pub_date", ""),
                    "language": hit.get("language", ""),
                    "url": hit.get("url", ""),
                    "score": hit.score
                })
    except Exception as e:
        logging.error(f"Erreur lors de la recherche dans l'index : {e}")
        return []
    return results
