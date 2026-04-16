"""
CrewAI Sample 1 - Ein einzelner Agent
======================================
Dieses Beispiel zeigt das absolute Minimum von CrewAI:
  - 1 Agent  (eine KI mit einer Rolle)
  - 1 Task   (eine Aufgabe fuer den Agenten)
  - 1 Crew   (startet alles)

Der Agent erstellt einen kreativen Tier-Steckbrief.
Auch Fantasietiere sind erlaubt!

Starte das Skript:
  python sample01_single_agent.py
"""

from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from display_helper import show

load_dotenv()

# ── Hier kannst du das Tier ändern ──────────────────────
TIER = "Axolotl"  # z.B. "Drache", "Krake", "Axolotl"
# ────────────────────────────────────────────────────────

# ─────────────────────────────────────────────
# Schritt 1: Agent erstellen
# ─────────────────────────────────────────────
# Ein Agent hat:
#   role       - seine Berufsbezeichnung / Rolle
#   goal       - sein Ziel, was er erreichen will
#   backstory  - seine Hintergrundgeschichte (macht die KI "besser" in ihrer Rolle)

tier_experte = Agent(
    role="Tier-Experte und Naturforscher",
    goal="Erstelle faszinierende und lehrreiche Steckbriefe ueber Tiere.",
    backstory="""\
        Du bist ein begeisterter Naturforscher und Biologe mit 20 Jahren Erfahrung.
        Du liebst es, Kindern und Jugendlichen die Tierwelt naeher zu bringen.
        Deine Steckbriefe sind immer spannend, voller ueberraschender Fakten
        und auch fuer Fantasietiere voller Kreativitaet.
    """,
    verbose=False,
)

# ─────────────────────────────────────────────
# Schritt 2: Eine Aufgabe erstellen
# ─────────────────────────────────────────────
# Eine Task beschreibt:
#   description     - was genau getan werden soll
#   expected_output - wie das Ergebnis aussehen soll
#   agent           - welcher Agent die Aufgabe erledigt

aufgabe = Task(
    description=f"""\
        Erstelle einen kreativen Steckbrief fuer: {TIER}

        Der Steckbrief soll enthalten:
        - Name und Herkunft
        - Aussehen (wie sieht es aus?)
        - Besondere Faehigkeiten oder Superkraefte
        - Ernaehrung (was frisst es?)
        - Ein ueberraschendes Fakt das kaum jemand kennt

        Schreibe spannend und fuer 12-14 jaehrige Schueler geeignet.
        Falls es ein Fantasietier ist, erfinde kreative aber glaubwuerdige Details.
    """,
    expected_output="""\
        Ein vollstaendiger, spannend geschriebener Tier-Steckbrief
        mit allen genannten Punkten, formatiert mit Ueberschriften.
    """,
    agent=tier_experte,
)

# ─────────────────────────────────────────────
# Schritt 3: Eine Crew erstellen und starten
# ─────────────────────────────────────────────
# Die Crew bringt Agenten und Aufgaben zusammen und fuehrt sie aus.

crew = Crew(
    agents=[tier_experte],
    tasks=[aufgabe],
    verbose=False,
)

ergebnis = crew.kickoff()

show(f"---\n## Steckbrief: {TIER}\n\n{ergebnis.raw}")
