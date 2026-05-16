# src/crew.py
from crewai import Crew, Process
from src.agents import ResearchCrewAgents
from src.tasks import ResearchCrewTasks

def run_market_research_crew(topic: str) -> str:
    # 1. Initialisation des classes de configuration
    agents_config = ResearchCrewAgents()
    tasks_config = ResearchCrewTasks()

    # 2. Instanciation des agents
    researcher = agents_config.researcher_agent()
    analyst = agents_config.analyst_agent()
    writer = agents_config.writer_agent()

    # 3. Instanciation des tâches avec assignation des agents
    task1 = tasks_config.research_task(researcher)
    task2 = tasks_config.analysis_task(analyst)
    task3 = tasks_config.writing_task(writer)

    # 4. Assemblage du Crew (Le Workflow)
    crew = Crew(
        agents=[researcher, analyst, writer],
        tasks=[task1, task2, task3],
        process=Process.sequential, # Exécution en chaîne (1 -> 2 -> 3)
        verbose=True
    )

    # 5. Exécution du workflow et récupération du résultat final
    result = crew.kickoff(inputs={'topic': topic})
    return str(result)