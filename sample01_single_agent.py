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

from crewai import Agent, Task, Crew

# ─────────────────────────────────────────────
# Schritt 1: Einen Agenten erstellen
# ─────────────────────────────────────────────
# Ein Agent hat:
#   role       - seine Berufsbezeichnung / Rolle
#   goal       - sein Ziel, was er erreichen will
#   backstory  - seine Hintergrundgeschichte (macht die KI "besser" in ihrer Rolle)

tier_experte = Agent(
    role="Tier-Experte und Naturforscher",
    goal="Erstelle faszinierende und lehrreiche Steckbriefe ueber Tiere.",
    backstory=(
        "Du bist ein begeisterter Naturforscher und Biologe mit 20 Jahren Erfahrung. "
        "Du liebst es, Kindern und Jugendlichen die Tierwelt naeher zu bringen. "
        "Deine Steckbriefe sind immer spannend, voller ueberraschender Fakten "
        "und auch fuer Fantasietiere voller Kreativitaet."
    ),
    verbose=True,  # zeigt uns was der Agent denkt
)

# ─────────────────────────────────────────────
# Schritt 2: Eine Aufgabe erstellen
# ─────────────────────────────────────────────
# Eine Task beschreibt:
#   description     - was genau getan werden soll
#   expected_output - wie das Ergebnis aussehen soll
#   agent           - welcher Agent die Aufgabe erledigt

tier = input(
    "Welches Tier soll beschrieben werden? (z.B. Axolotl, Drache, Krake): "
).strip()
if not tier:
    tier = "Axolotl"

aufgabe = Task(
    description=(
        f"Erstelle einen kreativen Steckbrief fuer: {tier}\n\n"
        "Der Steckbrief soll enthalten:\n"
        "- Name und Herkunft\n"
        "- Aussehen (wie sieht es aus?)\n"
        "- Besondere Faehigkeiten oder Superkraefte\n"
        "- Ernaehrung (was frisst es?)\n"
        "- Ein ueberraschendes Fakt das kaum jemand kennt\n\n"
        "Schreibe spannend und fuer 12-14 jaehrige Schueler geeignet. "
        "Falls es ein Fantasietier ist, erfinde kreative aber glaubwuerdige Details."
    ),
    expected_output=(
        "Ein vollstaendiger, spannend geschriebener Tier-Steckbrief "
        "mit allen genannten Punkten, formatiert mit Ueberschriften."
    ),
    agent=tier_experte,
)

# ─────────────────────────────────────────────
# Schritt 3: Eine Crew erstellen und starten
# ─────────────────────────────────────────────
# Die Crew bringt Agenten und Aufgaben zusammen und fuehrt sie aus.

crew = Crew(
    agents=[tier_experte],
    tasks=[aufgabe],
    verbose=True,
)

print(f"\nDer Agent erstellt jetzt einen Steckbrief fuer: {tier}\n")

ergebnis = crew.kickoff()

print("\n" + "=" * 60)
print("FERTIGER STECKBRIEF:")
print("=" * 60)
print(ergebnis)
