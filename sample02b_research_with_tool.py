"""
CrewAI Sample 2b - Agent MIT Web-Tool
========================================
Derselbe Recherche-Agent - diesmal MIT einem Google-Such-Tool.

Das Tool heisst SerperDevTool und ermoeglicht echte Google-Suchen.
Benoetigt: SERPER_API_KEY in der .env Datei
Kostenlos registrieren: https://serper.dev (2500 Suchen gratis)

Beobachte den Unterschied:
- Der Agent sucht aktiv im Internet
- Er findet aktuelle Umfragen von heute oder dieser Woche
- Die Zahlen sind viel aktueller und genauer
"""

from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool, WebsiteSearchTool
from display_helper import show

load_dotenv()

# Das Web-Such-Tool - liest SERPER_API_KEY automatisch aus .env
such_tool = SerperDevTool()
# such_tool = WebsiteSearchTool(website='https://dawum.de/')

# Identischer Agent - nur tools=[such_tool] ist neu!
agent_mit_tool = Agent(
    role="Politischer Analyst",
    goal="Recherchiere aktuelle Wahlumfragen und politische Stimmungsbilder in Deutschland.",
    backstory="""\
        Du bist ein erfahrener politischer Analyst mit Fokus auf deutsche Politik.
        Du wertest Wahlumfragen aus und erklaerst politische Trends verstaendlich.
        Du nutzt immer aktuelle Quellen und gibst diese an.
    """,
    verbose=True,
    tools=[such_tool],  # <-- das ist der einzige Unterschied!
)

aufgabe_mit_tool = Task(
    description="""\
        Recherchiere die AKTUELLSTEN Wahlumfragen fuer Deutschland.

        Suche im Internet nach den neuesten Umfrageergebnissen und beantworte:
        1. Welche Umfragewerte haben CDU/CSU, SPD, Gruene, FDP, AfD, BSW aktuell?
        2. Welche Partei liegt vorne?
        3. Von wann ist die neueste Umfrage und wer hat sie durchgefuehrt?

        Nenne konkrete Prozentzahlen, das genaue Datum und die Quelle der Umfragen.
    """,
    expected_output="Uebersicht der Wahlumfragen mit Prozentzahlen, Datum und Quellenangabe.",
    agent=agent_mit_tool,
)

ergebnis_mit = Crew(agents=[agent_mit_tool], tasks=[aufgabe_mit_tool]).kickoff()

show(f"---\n## Ergebnis: Mit Web-Tool\n\n{ergebnis_mit.raw}")
