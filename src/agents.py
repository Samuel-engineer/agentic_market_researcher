# src/agents.py
import os

from crewai import Agent, LLM
from src.tools import search_tool, scrape_tool
from dotenv import load_dotenv

load_dotenv()

def _build_llm() -> LLM:
    api_key = os.getenv("AZURE_API_KEY")
    base_url = os.getenv("AZURE_ENDPOINT")
    if not api_key or not base_url:
        raise EnvironmentError(
            "Variables manquantes dans .env : AZURE_API_KEY et AZURE_ENDPOINT sont requis."
        )
    return LLM(
        model="openai/gpt-4o",
        api_key=api_key,
        base_url=base_url,
    )

class ResearchCrewAgents:
    def __init__(self):
        self._llm = _build_llm()

    def researcher_agent(self) -> Agent:
        return Agent(
            role='Senior Market Researcher',
            goal='Trouver les données, actualités et chiffres les plus récents et pertinents sur {topic}',
            backstory=(
                'Tu es un chercheur d\'élite travaillant pour un cabinet de conseil européen. '
                'Tu es reconnu pour ta capacité à fouiller le web et trouver des données chiffrées exactes. '
                'Tu ne te bases que sur des faits et tu cites tes sources de manière rigoureuse.'
            ),
            verbose=True,
            allow_delegation=False,
            llm=self._llm,
            tools=[search_tool, scrape_tool]  # Seul cet agent a accès à Internet
        )

    def analyst_agent(self) -> Agent:
        return Agent(
            role='Data Insights Analyst',
            goal='Analyser les données brutes de recherche et en extraire les tendances stratégiques majeures',
            backstory=(
                'Tu es un analyste stratégique pragmatique et brillant. Tu détestes le bla-bla. '
                'Tu prends des volumes d\'informations brutes et tu en tires les insights clés. '
                'Tu sais repérer immédiatement les risques et les opportunités business cachés derrière les chiffres.'
            ),
            verbose=True,
            llm=self._llm,
            allow_delegation=False
        )

    def writer_agent(self) -> Agent:
        return Agent(
            role='Corporate Content Strategist',
            goal='Rédiger un rapport exécutif clair, structuré et convaincant en Markdown',
            backstory=(
                'Tu es le rédacteur principal pour le comité de direction. Tu sais formater '
                'un document pour qu\'il soit immédiatement assimilable par des cadres pressés : '
                'titres percutants, listes à puces logiques, et un ton professionnel, neutre et corporate.'
            ),
            verbose=True,
            llm=self._llm,
            allow_delegation=False
        )