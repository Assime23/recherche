import requests
import json
import os
from datetime import datetime
from typing import List, Dict

def collect_hal(query: str = "intelligence artificielle", 
                max_results: int = 100, 
                sort: str = "submittedDate_tdate desc",
                fields: List[str] = ["docid", "title_s", "authFullName_s", "abstract_s", 
                                   "keyword_s", "publicationDate_s", "journalTitle_s", 
                                   "uri_s", "language_s"]) -> List[Dict]:
    """
    Collecte les documents depuis HAL avec plus de paramètres et de métadonnées
    """
    base_url = "https://api.archives-ouvertes.fr/search/"
    params = {
        "q": query,
        "rows": max_results,
        "fl": ",".join(fields),
        "sort": sort,
        "wt": "json"
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        results = response.json().get("response", {}).get("docs", [])
        
        # Ajout de la date de collecte
        timestamp = datetime.now().isoformat()
        data = {
            "metadata": {
                "query": query,
                "collected_at": timestamp,
                "total_results": len(results)
            },
            "documents": results
        }
        
        os.makedirs("data", exist_ok=True)
        filename = f"data/hal_data_{query.replace(' ', '_')}_{timestamp[:10]}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        return results
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la collecte: {e}")
        return []

if __name__ == "__main__":
    topics = [
        # Informatique générale
        "informatique", "computer science", "sciences informatiques", "information technology", "IT",
        # Intelligence artificielle
        "intelligence artificielle", "artificial intelligence", "machine learning", "apprentissage automatique",
        "deep learning", "apprentissage profond", "IA", "AI",
        # Algorithmique et théorie
        "algorithmique", "algorithms", "algorithm", "complexité", "complexity theory", "théorie des graphes", "graph theory",
        # Programmation
        "programmation", "programming", "langages de programmation", "programming languages", "Python", "Java", "C++", "JavaScript",
        # Systèmes et réseaux
        "systèmes embarqués", "embedded systems", "systèmes d'exploitation", "operating systems", "Linux", "Windows",
        "réseaux", "networks", "networking", "protocoles réseaux", "network protocols",
        # Sécurité
        "sécurité informatique", "cybersécurité", "cybersecurity", "cryptographie", "cryptography", "sécurité des réseaux",
        # Données et bases de données
        "data science", "science des données", "big data", "données massives", "bases de données", "database", "SQL", "NoSQL",
        # Cloud et virtualisation
        "cloud computing", "informatique en nuage", "virtualisation", "virtualization", "containers", "conteneurs", "Docker", "Kubernetes",
        # Blockchain et Web
        "blockchain", "chaîne de blocs", "web", "web sémantique", "semantic web", "web3", "internet",
        # Génie logiciel
        "génie logiciel", "software engineering", "devops", "test logiciel", "software testing", "architecture logicielle", "software architecture",
        # Informatique graphique et vision
        "informatique graphique", "computer graphics", "vision par ordinateur", "computer vision", "traitement d'image", "image processing",
        # Robotique et IoT
        "robotique", "robotics", "internet des objets", "internet of things", "IoT",
        # Informatique quantique
        "informatique quantique", "quantum computing",
        # Bioinformatique
        "bioinformatique", "bioinformatics",
        # Interaction homme-machine
        "interaction homme-machine", "human-computer interaction", "IHM", "HCI",
        # Informatique théorique
        "théorie de l'information", "information theory", "automates", "automata theory",
        # Autres domaines
        "simulation", "modélisation", "modelling", "simulation numérique", "numerical simulation",
        "apprentissage supervisé", "supervised learning", "apprentissage non supervisé", "unsupervised learning",
        "réalité virtuelle", "virtual reality", "réalité augmentée", "augmented reality",
        "industrie 4.0", "industry 4.0", "systèmes multi-agents", "multi-agent systems"
    ]
    for topic in topics:
        collect_hal(query=topic, max_results=500)
