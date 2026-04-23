"""
CrewAI Sample 1 - Ein einzelner Agent
======================================
Dieses Beispiel zeigt das absolute Minimum von CrewAI:
  - 1 Agent  (eine KI mit einer Rolle)
  - 1 Task   (eine Aufgabe fuer den Agenten)
  - 1 Crew   (startet alles)

Der Agent erstellt einen kreativen Tier-Steckbrief.
Ein zweiter Agent generiert dazu ein passendes Bild mit DALL-E.
Auch Fantasietiere sind erlaubt!

Starte das Skript:
  python sample01_single_agent.py
"""

import json
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai_tools import DallETool
from display_helper import show

load_dotenv()

# ── Hier kannst du das Tier ändern ──────────────────────
TIER = "Axolotl"  # z.B. "Drache", "Krake", "Axolotl"
# ────────────────────────────────────────────────────────

# ─────────────────────────────────────────────
# Schritt 1: Agenten erstellen
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

# Der Bild-Agent hat Zugriff auf das DALL-E Tool und erzeugt ein passendes Bild.
bild_agent = Agent(
    role="Illustrator und Bildkuenstler",
    goal="Erzeuge ein farbenfrohes, ansprechendes Bild das perfekt zum Tier passt.",
    backstory="""\
        Du bist ein kreativer Illustrator mit einem Fable fuer Tiere und Natur.
        Du verwandelst Beschreibungen in lebendige, detailreiche Bilder.
        Dein Stil ist bunt, freundlich und fuer Kinder und Jugendliche geeignet.
    """,
    tools=[DallETool(model="dall-e-3", size="1024x1024", quality="standard")],
    verbose=False,
)

# ─────────────────────────────────────────────
# Schritt 2: Aufgaben erstellen
# ─────────────────────────────────────────────
# Eine Task beschreibt:
#   description     - was genau getan werden soll
#   expected_output - wie das Ergebnis aussehen soll
#   agent           - welcher Agent die Aufgabe erledigt

steckbrief_aufgabe = Task(
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

bild_aufgabe = Task(
    description=f"""\
        Erzeuge ein farbenfrohes, ansprechendes Bild von: {TIER}

        Nutze den Steckbrief des vorherigen Agenten als Inspiration fuer den Bildstil.
        Das Bild soll das Tier in seiner natuerlichen Umgebung zeigen,
        freundlich und fuer Kinder geeignet, im Stil einer Naturillustration.

        Gib die URL des generierten Bildes zurueck.
    """,
    expected_output="""\
        Eine URL die direkt auf das generierte Bild zeigt.
    """,
    agent=bild_agent,
    context=[steckbrief_aufgabe],
)

# ─────────────────────────────────────────────
# Schritt 3: Eine Crew erstellen und starten
# ─────────────────────────────────────────────
# Die Crew bringt Agenten und Aufgaben zusammen und fuehrt sie aus.

crew = Crew(
    agents=[tier_experte, bild_agent],
    tasks=[steckbrief_aufgabe, bild_aufgabe],
    verbose=False,
)

ergebnis = crew.kickoff()

# Steckbrief anzeigen
show(f"---\n## Steckbrief: {TIER}\n\n{steckbrief_aufgabe.output.raw}")

# Bild-URL aus dem JSON-Ergebnis des DallE-Tools extrahieren
try:
    bild_daten = json.loads(bild_aufgabe.output.raw)
    bild_url = bild_daten.get("image_url", bild_aufgabe.output.raw)
except (json.JSONDecodeError, AttributeError):
    bild_url = bild_aufgabe.output.raw

show(f"---\n## Bild: {TIER}\n\n{bild_url}")
