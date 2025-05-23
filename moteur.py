from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser, QueryParser
from whoosh.query import DateRange
from whoosh.sorting import FieldFacet, ScoreFacet
from typing import Dict, List

def rechercher(query: str, 
              fields: List[str] = None,
              filters: Dict = None,
              sort_by: str = "score",
              limit: int = 20) -> List[Dict]:
    """
    Recherche avancée avec filtres et tri, supporte la recherche floue
    """
    ix = open_dir("index")
    
    if fields is None:
        fields = ["title", "authors", "abstract", "keywords"]

    # Ajout automatique du fuzzy (~2) à chaque mot de la requête
    fuzzy_query = " ".join([f"{mot}~2" for mot in query.split()])
    parser = MultifieldParser(fields, schema=ix.schema)
    q = parser.parse(fuzzy_query)

    # Application des filtres
    if filters:
        for field, value in filters.items():
            if field == "date_range":
                q = q & DateRange("pub_date", value[0], value[1])
            elif field in ix.schema:
                field_parser = QueryParser(field, schema=ix.schema)
                q = q & field_parser.parse(value)

    # Configuration du tri
    sorting = None
    if sort_by == "date":
        sorting = FieldFacet("pub_date", reverse=True)
    elif sort_by == "score":
        sorting = ScoreFacet()

    results = []
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
    
    return results
