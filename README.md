# Market Research Studio

Assistant d'études de marché automatisées, propulsé par un système multi-agents autonome (CrewAI) et hébergé sur Azure AI Foundry.

L'application orchestre une équipe de 3 agents IA spécialisés — **Chercheur**, **Analyste**, **Rédacteur** — qui collaborent pour produire un rapport exécutif structuré à partir d'un simple sujet saisi par l'utilisateur.

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Streamlit (app.py)                  │
│              Interface utilisateur web               │
└──────────────────────┬──────────────────────────────┘
                       │ topic
                       ▼
┌─────────────────────────────────────────────────────┐
│               CrewAI Orchestrator (crew.py)          │
│                  Process: Sequential                 │
└──────┬───────────────┬──────────────────┬───────────┘
       │               │                  │
       ▼               ▼                  ▼
┌────────────┐  ┌────────────┐  ┌─────────────────┐
│ Chercheur  │  │ Analyste   │  │   Rédacteur     │
│            │  │            │  │                 │
│ Serper API │  │  (LLM)     │  │  (LLM)          │
│ Web Scrape │  │            │  │  Rapport .md    │
└────────────┘  └────────────┘  └─────────────────┘
       │               │                  │
       └───────────────┴──────────────────┘
                       │
                       ▼
          ┌─────────────────────────┐
          │   Azure AI Foundry      │
          │   gpt-4o (OpenAI v1)    │
          └─────────────────────────┘
```

### Flux de travail

1. **Chercheur** — interroge le web via Serper et scrape les pages pertinentes
2. **Analyste** — reçoit les données brutes, extrait les tendances clés et les risques
3. **Rédacteur** — produit un rapport exécutif en Markdown à partir de l'analyse

---

## Stack technique

| Composant | Technologie |
|---|---|
| Interface web | Streamlit 1.57 |
| Orchestration multi-agents | CrewAI 1.14.4 |
| Modèle LLM | GPT-4o via Azure AI Foundry |
| Recherche web | Serper Dev API |
| Scraping | CrewAI ScrapeWebsiteTool |
| Gestion des secrets | python-dotenv |

---

## Prérequis

- Python 3.11+
- Un projet **Azure AI Foundry** avec un déploiement `gpt-4o`
- Une clé API **[Serper](https://serper.dev)** (100 requêtes/mois gratuites)

---

## Installation

**1. Cloner le dépôt et créer l'environnement virtuel**

```bash
git clone <url-du-repo>
cd agentic_market_research
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux
```

**2. Installer les dépendances**

```bash
pip install -r requirements.txt
```

**3. Configurer les variables d'environnement**

```bash
cp .env.example .env
```

Renseigner les valeurs dans `.env` :

```env
# Azure AI Foundry > votre projet > Settings > Keys and Endpoint
AZURE_API_KEY=your_azure_api_key_here

# Format : https://<resource>.services.ai.azure.com/api/projects/<project>/openai/v1
AZURE_ENDPOINT=https://<resource>.services.ai.azure.com/api/projects/<project>/openai/v1

# https://serper.dev
SERPER_API_KEY=your_serper_api_key_here
```

**4. Lancer l'application**

```bash
streamlit run app.py
```

L'interface est accessible sur `http://localhost:8501`.

---

## Structure du projet

```
agentic_market_research/
├── app.py                  # Point d'entrée Streamlit
├── requirements.txt        # Dépendances épinglées
├── .env                    # Secrets locaux (non commité)
├── .env.example            # Template de configuration
├── .gitignore
└── src/
    ├── __init__.py
    ├── agents.py           # Définition des 3 agents CrewAI
    ├── crew.py             # Assemblage et exécution du Crew
    ├── tasks.py            # Définition des 3 tâches
    └── tools.py            # Outils web (Serper + Scraper)
```

---

## Note sur la compatibilité Azure AI Foundry

CrewAI 1.14.4 utilise nativement le SDK `azure.ai.inference` pour le provider `azure/`. Ce SDK injecte automatiquement un paramètre `api-version` incompatible avec les endpoints Foundry `/openai/v1`.

**La configuration correcte utilise le provider `openai/` avec `base_url` :**

```python
LLM(
    model="openai/gpt-4o",
    api_key=os.getenv("AZURE_API_KEY"),
    base_url=os.getenv("AZURE_ENDPOINT"),  # .../openai/v1
)
```

Voir [TROUBLESHOOTING.md](TROUBLESHOOTING.md) pour le détail complet des erreurs rencontrées.
