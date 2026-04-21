# ==============================================================================
# Sample 4: KI entwickelt ein Spiel
# ==============================================================================
# In diesem Beispiel arbeiten mehrere KI-Agenten zusammen, um ein Text-Adventure
# zu entwickeln – von der ersten Idee bis zum fertigen Python-Code.
#
# Der Prozess hat drei Phasen:
#   Phase 1: Ein Ideen-Agent erfindet ein Spielkonzept
#   Phase 2: Ein Design-Team entwickelt das genaue Spieldesign
#   Phase 3: Ein Entwicklungs-Team schreibt den fertigen Python-Code
#
# Nach jeder Phase kannst du Feedback geben – die KI ueberarbeitet das Ergebnis
# so lange, bis du zufrieden bist!
#
# Konzepte:
#   - Mehrere Crews hintereinander
#   - Feedback-Schleife pro Phase: Crew laeuft erneut bis Ergebnis passt
#   - Ergebnisse einer Crew als Eingabe fuer die naechste
#   - Datei-Output: das fertige Spiel wird als .py Datei gespeichert
# ==============================================================================

import os
from dotenv import load_dotenv
from display_helper import show

load_dotenv()

# ------------------------------------------------------------------------------
# Schritt 1: Spielthema vom Benutzer erfragen
# (Eingabe VOR dem CrewAI-Import, damit die KI-Initialisierung
#  den Jupyter-Input-Prompt nicht stoert)
# ------------------------------------------------------------------------------
print("\n" + "="*60)
print("  Willkommen beim KI Spielentwicklungs-Studio!")
print("="*60)
thema = input("\nWelches Thema soll dein Text-Adventure haben?\n(z.B. Piraten, Weltraum, Mittelalter, Unterwasser): ").strip()
if not thema:
    thema = "Piraten"

print(f"\nSuper! Wir entwickeln ein {thema}-Abenteuer!")
print("KI wird geladen...\n")

# CrewAI erst nach der ersten Benutzereingabe laden
from crewai import Agent, Task, Crew, Process

# ------------------------------------------------------------------------------
# Hilfsfunktion: Ergebnis anzeigen und Feedback einholen
# ------------------------------------------------------------------------------
def feedback_einholen(phase: str, ergebnis: str) -> str:
    """
    Zeigt das Ergebnis einer Phase an und fragt nach Feedback.
    Gibt den Feedback-Text zurueck, oder einen leeren String wenn zufrieden.
    """
    show(f"## Ergebnis: {phase}\n\n{ergebnis}")
    print("\n" + "="*60)
    print(f"  Phase abgeschlossen: {phase}")
    print("="*60)
    print("Bist du zufrieden? Druecke Enter zum Weitermachen,")
    feedback = input("oder gib Feedback ein (z.B. 'mehr Raetsel', 'lustiger'): ").strip()
    return feedback


# ==============================================================================
# PHASE 1: SPIELIDEE (mit Feedback-Schleife)
# ==============================================================================

ideen_agent = Agent(
    role="Kreative Spieleentwicklerin",
    goal="Fesselnde und originelle Spielideen fuer Text-Adventures erfinden",
    backstory="""Du bist eine kreative Spieleentwicklerin mit viel Erfahrung im
    Erfinden von spannenden Geschichten und Spielkonzepten. Du weisst, was
    Spielerinnen begeistert: eine klare Pramisse, ein interessantes Ziel und
    eine besondere Wendung.""",
    verbose=False,
)

# Die Feedback-Schleife: Crew laeuft erneut wenn Feedback gegeben wird
idee_text = None
feedback = ""
runde = 1

while True:
    # Beim ersten Durchlauf: Idee zum Thema erfinden
    # Bei weiteren Durchlaeufen: Idee gemaess Feedback ueberarbeiten
    if idee_text is None:
        beschreibung = """Erfinde eine originelle Spielidee fuer ein Text-Adventure zum Thema: {thema}

        Schreibe eine kurze Spielidee (ca. 150 Woerter) mit:
        - Premise: Wer ist die Spielerin? In welcher Situation steckt sie?
        - Ziel: Was muss sie erreichen?
        - Besonderheit: Was macht dieses Spiel einzigartig und spannend?

        Schreibe auf Deutsch und halte es fuer 12-14 jaehrige Schuelerinnen geeignet.
        Kein Blut, keine Gewalt, aber durchaus spannend und abenteuerlich."""
        inputs = {"thema": thema}
    else:
        beschreibung = """Ueberarbeite diese Spielidee gemaess dem Feedback:

        Bisherige Idee:
        {idee}

        Feedback: {feedback}

        Schreibe die verbesserte Spielidee (ca. 150 Woerter) mit den Abschnitten
        **Premise**, **Ziel** und **Besonderheit**. Auf Deutsch."""
        inputs = {"idee": idee_text, "feedback": feedback}

    idee_task = Task(
        description=beschreibung,
        expected_output="""Eine Spielidee mit drei klar beschrifteten Abschnitten:
        **Premise**, **Ziel** und **Besonderheit**. Ca. 150 Woerter, auf Deutsch.""",
        agent=ideen_agent,
    )

    print(f"Phase 1: Spielidee wird {'entwickelt' if runde == 1 else 'ueberarbeitet'} (Runde {runde})...")
    ideen_crew = Crew(agents=[ideen_agent], tasks=[idee_task], process=Process.sequential, verbose=False)
    idee_text = str(ideen_crew.kickoff(inputs=inputs))

    feedback = feedback_einholen("Spielidee", idee_text)
    if not feedback:
        break  # Spielerin ist zufrieden -> weiter zur naechsten Phase
    runde += 1


# ==============================================================================
# PHASE 2: SPIELDESIGN (mit Feedback-Schleife)
# ==============================================================================

game_designer = Agent(
    role="Game Design Spezialistin",
    goal="Detaillierte und spielbare Game Design Dokumente erstellen",
    backstory="""Du bist eine erfahrene Game Designerin, die Text-Adventures
    liebt. Du weisst, wie man eine gute Spielstruktur aufbaut: interessante
    Raeume, logische Raetsel und befriedigende Enden. Du hast ein Gefuehl dafuer,
    was Spass macht und was frustriert.""",
    verbose=False,
)

design_reviewer = Agent(
    role="Spieltest-Expertin",
    goal="Game Designs auf Spassfaktor, Machbarkeit und Logik pruefen",
    backstory="""Du bist eine Spiele-Testerin mit scharfem Blick fuer Probleme.
    Du erkennst sofort wenn ein Raetsel zu schwer oder zu einfach ist, wenn die
    Geschichte keinen Sinn ergibt, oder wenn etwas technisch schwierig
    umzusetzen waere. Du gibst konstruktives Feedback.""",
    verbose=False,
)

ascii_artist = Agent(
    role="ASCII-Art Kuenstlerin",
    goal="Erkennbare, atmosphaerische ASCII-Art Bilder fuer jeden Raum eines Text-Adventures erstellen",
    backstory="""Du bist eine erfahrene ASCII-Art Kuenstlerin. Du weisst, dass gutes ASCII-Art
    erkennbare Umrisse und klare Strukturen hat. Du verwendest Zeichen so dass sie echte
    Formen ergeben – Baeume sehen wie Baeume aus, Haeuser wie Haeuser.

    Hier sind Beispiele fuer gutes ASCII-Art:

    Baum:
         *
        ***
       *****
      *******
         |

    Haus:
        /\\
       /  \\
      /----\\
      |    |
      | [] |
      |____|

    Hoehle:
      .-""""""""-.
     /  (o)  (o)  \\
    |   .------.   |
     \\  |      |  /
      '-.______.-'

    Regeln:
    - Verwende Zeichen die die Form des Objekts nachahmen: / \\ _ | fuer Kanten und Umrisse
    - Zeichen wie * . , fuer Textur (Blaetter, Gras, Wasser)
    - Das Bild muss auf den ersten Blick erkennbar sein
    - Jede Zeile gleich lang (mit Leerzeichen auffuellen)
    - Ca. 8-10 Zeilen hoch, ca. 40 Zeichen breit
    - KEINE willkuerlichen Zeichen oder unleserlichen Muster""",
    verbose=False,
    llm="gpt-4o",
)

design_text = None
feedback = ""
runde = 1

while True:
    if design_text is None:
        design_inputs = {"kontext": idee_text, "feedback_hinweis": ""}
        feedback_zeile = ""
    else:
        design_inputs = {
            "kontext": idee_text,
            "feedback_hinweis": f"\n\nFeedback der Spielerin: {feedback}\nBitte beruecksichtige dieses Feedback bei der Ueberarbeitung.",
        }
        feedback_zeile = f" (Ueberarbeitung gemaess Feedback: {feedback})"

    design_task = Task(
        description="""Erstelle ein detailliertes Game Design Dokument fuer dieses Text-Adventure:

        Spielidee:
        {kontext}
        {feedback_hinweis}

        Das Design Dokument muss enthalten:
        1. **Raeume** (3-5 Raeume mit Namen und kurzer Beschreibung)
        2. **Gegenstaende** (2-4 Gegenstaende die die Spielerin finden/benutzen kann)
        3. **Raetsel oder Herausforderungen** (1-2 konkrete Raetsel mit Loesung)
        4. **Enden** (1 gutes Ende, 1 schlechtes Ende)
        5. **Befehle** (welche Textbefehle die Spielerin eingeben kann)

        Halte es einfach genug fuer ein Python-Script. Schreibe auf Deutsch.""",
        expected_output="""Ein strukturiertes Game Design Dokument mit den 5 Abschnitten
        (Raeume, Gegenstaende, Raetsel, Enden, Befehle).""",
        agent=game_designer,
    )

    review_task = Task(
        description="""Pruefe das Game Design Dokument und verbessere es wo noetig.

        Achte auf:
        - Sind die Raetsel loesbar und fair?
        - Ist die Struktur logisch und konsistent?
        - Ist es als einfaches Python-Script umsetzbar?
        - Macht es Spass fuer 12-14 jaehrige?

        Gib das verbesserte, vollstaendige Design Dokument zurueck.""",
        expected_output="""Das verbesserte, vollstaendige Game Design Dokument.
        Alle 5 Abschnitte muessen enthalten sein.""",
        agent=design_reviewer,
        context=[design_task],
    )

    ascii_task = Task(
        description="""Erstelle fuer jeden Raum im Game Design Dokument ein passendes ASCII-Art Bild.

        Fuer jeden Raum gilt:
        - Zeichne die typischen Objekte und die Atmosphaere des Raumes
        - Das Bild muss auf den ersten Blick erkennbar sein (Wald = Baeume, Burg = Turm, etc.)
        - Verwende / \\ | _ fuer Umrisse und Kanten
        - Verwende * . , ~ fuer Texturen (Blaetter, Wasser, Gras)
        - Alle Zeilen gleich lang (mit Leerzeichen auffuellen)
        - Ca. 8-10 Zeilen, ca. 40 Zeichen breit
        - Beginne jedes Bild mit ## RAUMNAME (Grossbuchstaben) als Ueberschrift
        - KEINE kryptischen Zeichenkombinationen – nur was wirklich erkennbar ist

        Gib NUR die ASCII-Bilder aus, eines pro Raum.""",
        expected_output="""Eines pro Raum: ## RAUMNAME gefolgt vom ASCII-Bild.
        Nur die Bilder, keine Erklaerungen.""",
        agent=ascii_artist,
        context=[review_task],
    )

    print(f"\nPhase 2: Spieldesign wird {'erstellt' if runde == 1 else 'ueberarbeitet'} (Runde {runde})...")
    design_crew = Crew(
        agents=[game_designer, design_reviewer, ascii_artist],
        tasks=[design_task, review_task, ascii_task],
        process=Process.sequential,
        verbose=False,
    )
    design_crew.kickoff(inputs=design_inputs)

    # Outputs separat abholen und kombinieren
    # .raw kann literal \n enthalten statt echte Zeilenumbrueche – normalisieren
    ascii_output = (ascii_task.output.raw if ascii_task.output else "").replace("\\n", "\n")
    design_output = (review_task.output.raw if review_task.output else "").replace("\\n", "\n")
    # ASCII-Art in Codeblock einwickeln damit Leerzeichen und Zeilenumbrueche
    # beim Anzeigen (Markdown / Terminal) erhalten bleiben
    design_text = f"## ASCII-Art\n\n```\n{ascii_output}\n```\n\n---\n\n{design_output}"

    feedback = feedback_einholen("Spieldesign", design_text)
    if not feedback:
        break
    runde += 1


# ==============================================================================
# PHASE 3: IMPLEMENTIERUNG (mit Feedback-Schleife)
# ==============================================================================

developer = Agent(
    role="Python Spieleentwicklerin",
    goal="Funktionierende und gut lesbare Text-Adventure Spiele in Python schreiben",
    backstory="""Du bist eine erfahrene Python-Entwicklerin, die sich auf
    Text-Adventure Spiele spezialisiert hat. Du schreibst sauberen, gut
    kommentierten Code der genau dem Game Design Dokument folgt. Dein Code
    laeuft ohne Fehler und macht Spass zu spielen. In jedem Raum wird das passende ASCII-Art Bild 
    angezeigt und es muss klar sein, wohin man sich bewegen kann.""",
    verbose=False,
)

code_reviewer = Agent(
    role="Code Review Spezialistin",
    goal="Python Code auf Fehler, Vollstaendigkeit und Spielbarkeit pruefen und verbessern",
    backstory="""Du bist eine sorgfaeltige Code-Reviewerin. Du pruefst ob der
    Code syntaktisch korrekt ist, ob alle Spielelemente aus dem Design umgesetzt
    wurden, und ob das Spiel tatsaechlich spielbar ist. Du gibst immer den
    vollstaendigen, korrigierten Code zurueck.""",
    verbose=False,
)

code_text = None
feedback = ""
runde = 1

while True:
    if code_text is None:
        impl_beschreibung = """Implementiere das folgende Text-Adventure als Python-Script:

        {kontext}

        Technische Anforderungen:
        - Reines Python, keine externen Bibliotheken
        - Eine Hauptfunktion spiele_spiel() die das Spiel startet
        - Am Ende: if __name__ == "__main__": spiele_spiel()
        - Gut kommentierter Code auf Deutsch
        - Spielerin gibt Textbefehle ein (input())
        - Klare Ausgaben was passiert (print())
        - Das Spiel hat ein klares Ende (gut oder schlecht)

        WICHTIG – ASCII-Art:
        Im Design-Dokument gibt es einen Abschnitt "## ASCII-Art" mit einem Bild pro Raum
        (jeweils als Codeblock). Speichere jeden Bild-Text als Python-String in einem
        Dictionary namens ASCII_ART.

        ACHTUNG: Das Dictionary wird innerhalb eines normalen Python-Strings definiert,
        daher NIEMALS dreifache Anfuehrungszeichen (triple quotes) verwenden!
        Verwende stattdessen einfache Strings mit \\n fuer Zeilenumbrueche, z.B.:
        ASCII_ART = {{
            "Eingang": "+-------+\\n|  ...  |\\n+-------+",
            "Hoehle":  "  ()()  \\n  (0_0) \\n /|   |\\ "
        }}
        Verwende print(ASCII_ART.get(raum_name, "")) wenn die Spielerin einen Raum betritt.

        Schreibe NUR den Python-Code, keine Erklaerungen darum herum."""
        impl_inputs = {"kontext": design_text}
    else:
        impl_beschreibung = """Ueberarbeite diesen Python-Code gemaess dem Feedback:

        Feedback: {feedback}

        Bestehender Code:
        {kontext}

        Schreibe den vollstaendigen, verbesserten Python-Code.
        Nur reiner Code, kein Markdown."""
        impl_inputs = {"feedback": feedback, "kontext": code_text}

    implementierung_task = Task(
        description=impl_beschreibung,
        expected_output="""Vollstaendiger, ausfuehrbarer Python-Code fuer das Text-Adventure.
        Kein Markdown, nur reiner Python-Code.""",
        agent=developer,
    )

    code_review_task = Task(
        description="""Pruefe den Python-Code fuer das Text-Adventure:

        - Ist der Code syntaktisch korrekt?
        - Sind alle Raeume, Gegenstaende und Raetsel implementiert?
        - Kann die Spielerin gewinnen UND verlieren?
        - Werden unbekannte Befehle sinnvoll behandelt?
        - Ist ein ASCII_ART Dictionary vorhanden und wird es beim Betreten jedes Raumes angezeigt?
        - Enthaelt ASCII_ART KEINE dreifachen Anfuehrungszeichen (\"\"\" oder ''')? Falls doch,
          ersetze sie durch einfache Strings mit \\n als Zeilenumbruch.

        Korrigiere alle Probleme und gib den vollstaendigen Python-Code zurueck.
        Nur reiner Code, kein Markdown.""",
        expected_output="""Vollstaendiger, korrigierter Python-Code. Nur reiner Code.""",
        agent=code_reviewer,
        context=[implementierung_task],
    )

    print(f"\nPhase 3: Spiel wird {'programmiert' if runde == 1 else 'ueberarbeitet'} (Runde {runde})...")
    dev_crew = Crew(
        agents=[developer, code_reviewer],
        tasks=[implementierung_task, code_review_task],
        process=Process.sequential,
        verbose=False,
    )
    code_text = str(dev_crew.kickoff(inputs=impl_inputs))

    # Code bereinigen: manchmal schreibt die KI ```python ... ``` drum herum
    if "```python" in code_text:
        code_text = code_text.split("```python")[1].split("```")[0].strip()
    elif "```" in code_text:
        code_text = code_text.split("```")[1].split("```")[0].strip()

    # Spiel nach jeder Runde speichern, damit es direkt getestet werden kann
    dateiname = thema.lower().replace(" ", "_").replace("-", "_")
    ausgabe_pfad = os.path.join(os.path.dirname(__file__) if '__file__' in dir() else os.getcwd(), f"mein_{dateiname}_spiel.py")
    with open(ausgabe_pfad, "w", encoding="utf-8") as f:
        f.write(code_text)

    show(f"""## Spiel gespeichert – teste es jetzt! 🎮

`{ausgabe_pfad}`

Oeffne ein **neues Terminal** in VS Code und starte das Spiel mit:
```
python {os.path.basename(ausgabe_pfad)}
```
Danach kannst du hier Feedback geben oder Enter druecken um fertig zu sein.
""")

    feedback = feedback_einholen("Spiel-Code (nach dem Testen)", f"```python\n{code_text}\n```")
    if not feedback:
        break
    runde += 1


# ==============================================================================
# ERGEBNIS: ABSCHLUSSMELDUNG
# ==============================================================================

show(f"""## Entwicklung abgeschlossen! 🎉

Das fertige Spiel liegt hier:
`{ausgabe_pfad}`

Starte es in einem Terminal mit:
```
python {os.path.basename(ausgabe_pfad)}
```

### Was die KI gemacht hat:
1. **Spielidee** erfunden – und so lange ueberarbeitet bis du zufrieden warst
2. **Spieldesign** erstellt – mit Raeumen, Raetseln und Enden
3. **Python-Code** geschrieben, reviewed und nach jedem Test gespeichert

Das ist echter Software-Entwicklungs-Workflow – nur von KI-Agenten durchgefuehrt!
""")
