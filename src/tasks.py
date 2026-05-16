# src/tasks.py
from crewai import Task, Agent

class ResearchCrewTasks:
    def research_task(self, agent: Agent) -> Task:
        return Task(
            description=(
                '1. Utilise le moteur de recherche pour identifier les 3 meilleures sources d\'actualités ou rapports sur : {topic}.\n'
                '2. Si les résumés de recherche (snippets) sont incomplets ou manquent de chiffres précis, '
                'utilise l\'outil de scraping pour lire le contenu complet de ces pages spécifiques.\n'
                '3. Rassemble uniquement les faits marquants et rejette le bruit.'
            ),
            expected_output='Un document brut listant au moins 5 faits majeurs chiffrés et leurs sources (URLs).',
            agent=agent
        )

    def analysis_task(self, agent: Agent) -> Task:
        return Task(
            description=(
                'Analyse les données brutes fournies par le chercheur. Identifie les opportunités majeures '
                'et les risques pour les entreprises du secteur. Synthétise les forces en présence.'
            ),
            expected_output='Une analyse structurée contenant une liste des 3 tendances clés, des risques associés et une synthèse.',
            agent=agent
        )

    def writing_task(self, agent: Agent) -> Task:
        return Task(
            description=(
                'Rédige le rapport final de synthèse en te basant UNIQUEMENT sur l\'analyse fournie par l\'analyste. '
                'Le rapport doit être rédigé en français.'
            ),
            expected_output=(
                'Un rapport au format Markdown parfait, contenant :\n'
                '- Un titre principal\n'
                '- Un Résumé Exécutif (Executive Summary)\n'
                '- Le détail des tendances et impacts business\n'
                '- Une conclusion stratégique.'
            ),
            agent=agent
        )