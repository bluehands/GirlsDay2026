"""
CrewAI Sample 2a - Agent OHNE Web-Tool
========================================
Ein Recherche-Agent der nach aktuellen Wahlumfragen gefragt wird -
aber NUR sein Trainingswissen nutzen kann.

Problem: Das KI-Modell wurde zu einem bestimmten Zeitpunkt trainiert.
Alles was danach passiert ist, weiss es nicht!

Beobachte: Der Agent wird veraltete oder ungenaue Zahlen nennen
und zugeben muessen, dass er keine aktuellen Daten hat.
"""

from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from display_helper import show

load_dotenv()

# Agent OHNE Tool - nur Trainingswissen
agent_ohne_tool = Agent(
    role="Politischer Analyst",
    goal="Recherchiere aktuelle Wahlumfragen und politische Stimmungsbilder in Deutschland.",
    backstory="""\
        Du bist ein erfahrener politischer Analyst mit Fokus auf deutsche Politik.
        Du wertest Wahlumfragen aus und erklaerst politische Trends verstaendlich.
        Du bist ehrlich wenn deine Informationen moeglicherweise nicht aktuell sind.
    """,
    verbose=False,
    # Kein tools=[] --> kein Internetzugang!
)

aufgabe_ohne_tool = Task(
    description="""\
        Erstelle eine Uebersicht der aktuellen Wahlumfragen fuer Deutschland.

        Beantworte:
        1. Welche Umfragewerte haben CDU/CSU, SPD, Gruene, FDP, AfD, BSW aktuell?
        2. Welche Partei liegt vorne?
        3. Von wann sind deine Informationen?

        Nenne konkrete Prozentzahlen und das Datum der Umfragen.
    """,
    expected_output="Uebersicht der Wahlumfragen mit Prozentzahlen, Datum und Quellenangabe.",
    agent=agent_ohne_tool,
)

ergebnis_ohne = Crew(agents=[agent_ohne_tool], tasks=[aufgabe_ohne_tool]).kickoff()

show(f"---\n## Ergebnis: Ohne Web-Tool\n\n{ergebnis_ohne.raw}")
