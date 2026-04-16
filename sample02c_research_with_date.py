"""
CrewAI Sample 2c - Aktuelles Datum im Prompt übergeben
========================================================
Problem aus Sample 2b: Der Agent sucht zwar im Internet,
aber er weiss nicht welches Datum heute ist!
Er könnte also nach "aktuellen Umfragen 2024" suchen,
obwohl wir 2026 haben.

Lösung: Wir übergeben das heutige Datum direkt im Task.
Das ist ein einfacher aber wichtiger Trick!

Lernziel: KI-Agenten wissen nicht was "heute" ist -
wir müssen es ihnen sagen.
"""

from datetime import date
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool
from display_helper import show

load_dotenv()

# Heutiges Datum automatisch ermitteln
HEUTE = date.today().strftime("%d.%m.%Y")
print(f"Heutiges Datum wird übergeben: {HEUTE}")

such_tool = SerperDevTool()
# such_tool = WebsiteSearchTool(website='https://dawum.de/')

agent_mit_datum = Agent(
    role="Politischer Analyst",
    goal="Recherchiere aktuelle Wahlumfragen und politische Stimmungsbilder in Deutschland.",
    backstory="""\
        Du bist ein erfahrener politischer Analyst mit Fokus auf deutsche Politik.
        Du wertest Wahlumfragen aus und erklaerst politische Trends verstaendlich.
        Du nutzt immer aktuelle Quellen und gibst diese an.
    """,
    verbose=False,
    tools=[such_tool],
)

# <-- das ist der einzige Unterschied zu Teil B: die erste Zeile mit dem Datum!
aufgabe_mit_datum = Task(
    description=f"""\
        Heute ist der {HEUTE}.

        Recherchiere die AKTUELLSTEN Wahlumfragen fuer Deutschland aus den letzten 7 Tagen.

        Beantworte:
        1. Welche Umfragewerte haben CDU/CSU, SPD, Gruene, FDP, AfD, BSW aktuell?
        2. Welche Partei liegt vorne?
        3. Von wann ist die neueste Umfrage und wer hat sie durchgefuehrt?

        Nenne konkrete Prozentzahlen, das genaue Datum und die Quelle.
    """,
    expected_output="Uebersicht der aktuellen Wahlumfragen mit Prozentzahlen, Datum und Quellenangabe.",
    agent=agent_mit_datum,
)

ergebnis_datum = Crew(agents=[agent_mit_datum], tasks=[aufgabe_mit_datum]).kickoff()

show(f"---\n## Ergebnis: Mit Web-Tool + Datum ({HEUTE})\n\n{ergebnis_datum.raw}")
