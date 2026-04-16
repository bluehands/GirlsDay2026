"""
Quiz-Spiel mit CrewAI
=====================
Dieses Spiel verwendet drei KI-Agenten, die zusammenarbeiten:
  1. Fragen-Ersteller  - erfindet Quiz-Fragen zu einem Thema
  2. Quiz-Master       - stellt die Fragen und wertet aus
  3. Erklaerer         - erklaert nach jeder Frage die richtige Antwort

Voraussetzungen:
  pip install -r requirements.txt
  Umgebungsvariable OPENAI_API_KEY muss gesetzt sein (oder .env Datei)
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool

# .env Datei laden (z.B. OPENAI_API_KEY=sk-...)
load_dotenv()


# ─────────────────────────────────────────────
# Eigenes Tool: Spieler-Antwort einlesen
# ─────────────────────────────────────────────
class PlayerInputTool(BaseTool):
    """Ein Tool, das dem Agenten erlaubt, die Antwort des Spielers einzulesen."""

    name: str = "player_input"
    description: str = (
        "Zeigt dem Spieler eine Frage an und liest seine Antwort ein. "
        "Eingabe: die Frage als Text. Ausgabe: die Antwort des Spielers."
    )

    def _run(self, question: str) -> str:
        print(f"\n{'=' * 60}")
        print(f"FRAGE: {question}")
        print(f"{'=' * 60}")
        answer = input("Deine Antwort: ").strip()
        return answer


# ─────────────────────────────────────────────
# Spielzustand (globale Variable fur die Crew)
# ─────────────────────────────────────────────
game_state = {
    "thema": "",
    "anzahl_fragen": 5,
    "punkte": 0,
    "runde": 0,
    "verlauf": [],  # Liste von {frage, antwort_spieler, richtig, erklaerung}
}


# ─────────────────────────────────────────────
# AGENTEN DEFINIEREN
# ─────────────────────────────────────────────


def erstelle_agenten():
    """Erstellt die drei Quiz-Agenten."""

    # Agent 1: Fragen-Ersteller
    fragen_ersteller = Agent(
        role="Quiz-Fragen-Ersteller",
        goal=(
            "Erstelle {anzahl} interessante Multiple-Choice-Fragen "
            "zum Thema '{thema}'. Jede Frage hat genau 4 Antwortoptionen (A, B, C, D) "
            "und eine klar markierte richtige Antwort."
        ),
        backstory=(
            "Du bist ein erfahrener Quizmaster und Lehrer. "
            "Du erstellst Fragen, die lehrreich, fair und klar verstaendlich sind. "
            "Deine Fragen sind weder zu leicht noch zu schwer - genau richtig "
            "fuer einen allgemeinen Wissensquiz."
        ),
        verbose=True,
        allow_delegation=False,
    )

    # Agent 2: Quiz-Master (stellt Fragen, wertet aus)
    quiz_master = Agent(
        role="Quiz-Master",
        goal=(
            "Fuehre das Quiz durch. Stelle dem Spieler die Fragen nacheinander, "
            "nehme seine Antworten entgegen und pruefe ob sie richtig sind. "
            "Zaehle die Punkte und gib am Ende eine Zusammenfassung."
        ),
        backstory=(
            "Du bist ein freundlicher und motivierender Quiz-Master. "
            "Du moderierst das Quiz professionell, gibst sofortiges Feedback "
            "und hast immer ein aufmunterndes Wort fuer den Spieler."
        ),
        verbose=True,
        allow_delegation=False,
        tools=[PlayerInputTool()],
    )

    # Agent 3: Erklaerer (erklaert richtige Antworten)
    erklaerer = Agent(
        role="Wissens-Erklaerer",
        goal=(
            "Erklaere nach dem Quiz jede Frage kurz und verstaendlich. "
            "Erklaere warum die richtige Antwort korrekt ist und was man daraus lernen kann."
        ),
        backstory=(
            "Du bist ein begeisterter Wissensvermittler und Lehrer. "
            "Du erklaerst komplizierte Dinge auf einfache, einpraegsame Weise. "
            "Deine Erklaerungen sind kurz (2-3 Saetze), praezise und interessant."
        ),
        verbose=True,
        allow_delegation=False,
    )

    return fragen_ersteller, quiz_master, erklaerer


# ─────────────────────────────────────────────
# AUFGABEN (TASKS) DEFINIEREN
# ─────────────────────────────────────────────


def erstelle_aufgaben(agenten, thema: str, anzahl: int):
    """Erstellt die Tasks fuer jede Phase des Quiz."""

    fragen_ersteller, quiz_master, erklaerer = agenten

    # Task 1: Fragen generieren
    aufgabe_fragen = Task(
        description=(
            f"Erstelle genau {anzahl} Multiple-Choice-Fragen zum Thema '{thema}'.\n\n"
            "Format fuer jede Frage (genau so einhalten):\n"
            "FRAGE 1: [Fragetext]\n"
            "A) [Option A]\n"
            "B) [Option B]\n"
            "C) [Option C]\n"
            "D) [Option D]\n"
            "RICHTIG: [Buchstabe]\n\n"
            "Stelle sicher dass die Fragen verschiedene Schwierigkeitsgrade haben."
        ),
        expected_output=(
            f"Eine Liste von {anzahl} gut formatierten Multiple-Choice-Fragen "
            f"zum Thema '{thema}', jede mit 4 Optionen und der markierten richtigen Antwort."
        ),
        agent=fragen_ersteller,
    )

    # Task 2: Quiz durchfuehren
    aufgabe_quiz = Task(
        description=(
            "Du hast eine Liste von Quiz-Fragen erhalten. "
            "Fuhre jetzt das Quiz mit dem Spieler durch:\n\n"
            "1. Begrueesse den Spieler freundlich\n"
            "2. Stelle jede Frage einzeln mit dem 'player_input' Tool\n"
            "3. Pruefe ob die Antwort korrekt ist (Grossschreibung ignorieren)\n"
            "4. Gib sofort Feedback: 'Richtig!' oder 'Leider falsch!'\n"
            "5. Zaehle die Punkte mit\n"
            "6. Am Ende: zeige Gesamtpunktzahl und ein motivierendes Schlusswort\n\n"
            "Wichtig: Verwende das Tool 'player_input' fuer jede Frage!\n"
            "Uebergib am Ende alle Fragen mit den Spielerantworten und ob sie richtig waren."
        ),
        expected_output=(
            "Eine vollstaendige Liste aller Fragen mit:\n"
            "- Der Frage selbst\n"
            "- Der Antwort des Spielers\n"
            "- Ob die Antwort richtig oder falsch war\n"
            "- Der korrekten Antwort\n"
            "- Die Gesamtpunktzahl"
        ),
        agent=quiz_master,
        context=[aufgabe_fragen],  # benoetigt die Fragen aus Task 1
    )

    # Task 3: Erklaerungen geben
    aufgabe_erklaerung = Task(
        description=(
            "Das Quiz ist abgeschlossen. Jetzt ist deine Aufgabe:\n\n"
            "Schreibe fuer JEDE Frage eine kurze, lehrreiche Erklaerung (2-3 Saetze):\n"
            "- Warum ist die richtige Antwort korrekt?\n"
            "- Was ist der interessante Hintergrund?\n"
            "- Was kann man daraus lernen?\n\n"
            "Formatiere die Erklaerungen uebersichtlich mit der Fragennummer."
        ),
        expected_output=(
            "Eine lehrreiche Zusammenfassung aller Quiz-Fragen mit "
            "kurzen, verstaendlichen Erklaerungen zur richtigen Antwort."
        ),
        agent=erklaerer,
        context=[aufgabe_fragen, aufgabe_quiz],  # benoetigt Fragen + Spielergebnisse
    )

    return [aufgabe_fragen, aufgabe_quiz, aufgabe_erklaerung]


# ─────────────────────────────────────────────
# HAUPTPROGRAMM
# ─────────────────────────────────────────────


def main():
    """Startet das Quiz-Spiel."""

    print("\n" + "=" * 60)
    print("  WILLKOMMEN BEIM CrewAI QUIZ-SPIEL!")
    print("=" * 60)
    print("\nDrei KI-Agenten werden zusammenarbeiten:")
    print("  - Fragen-Ersteller: erfindet Fragen zu deinem Thema")
    print("  - Quiz-Master:      stellt dir die Fragen")
    print("  - Erklaerer:        erklaert die Antworten am Ende")
    print()

    # Spieler nach Thema und Anzahl fragen
    thema = input(
        "Welches Thema soll das Quiz haben? (z.B. 'Weltall', 'Tiere', 'Geschichte'): "
    ).strip()
    if not thema:
        thema = "Allgemeinwissen"

    anzahl_str = input(f"Wie viele Fragen? (Standard: 5, Maximum: 10): ").strip()
    try:
        anzahl = max(1, min(10, int(anzahl_str)))
    except ValueError:
        anzahl = 5

    print(f"\nGut! Das Quiz startet jetzt zum Thema '{thema}' mit {anzahl} Fragen.")
    print("Die KI-Agenten bereiten sich vor...\n")

    # Agenten und Aufgaben erstellen
    agenten = erstelle_agenten()
    aufgaben = erstelle_aufgaben(agenten, thema, anzahl)

    # Crew zusammenstellen
    # Process.sequential = die Agenten arbeiten nacheinander (einer nach dem anderen)
    crew = Crew(
        agents=list(agenten),
        tasks=aufgaben,
        process=Process.sequential,  # erst Fragen erstellen, dann Quiz, dann erklaeren
        verbose=True,
    )

    # Quiz starten!
    ergebnis = crew.kickoff()

    print("\n" + "=" * 60)
    print("  QUIZ BEENDET - DANKE FUERS SPIELEN!")
    print("=" * 60)
    print("\nErgebnis-Zusammenfassung:")
    print(ergebnis)


if __name__ == "__main__":
    # Pruefe ob API-Key gesetzt ist
    if not os.getenv("OPENAI_API_KEY"):
        print("FEHLER: OPENAI_API_KEY ist nicht gesetzt!")
        print("Erstelle eine .env Datei mit dem Inhalt:")
        print("  OPENAI_API_KEY=sk-dein-api-key-hier")
        print()
        print("Oder setze die Umgebungsvariable direkt:")
        print("  Windows: set OPENAI_API_KEY=sk-dein-api-key")
        print("  Linux/Mac: export OPENAI_API_KEY=sk-dein-api-key")
        exit(1)

    main()
