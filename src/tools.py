# src/tools.py
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

# Moteur de recherche (Les yeux)
search_tool = SerperDevTool()

# Scrapper de contenu (Les mains)
scrape_tool = ScrapeWebsiteTool()