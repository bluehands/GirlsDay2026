"""
CrewAI Sample 3 - Agenten-Zusammenarbeit: Die Debatte
=======================================================
Dieses Beispiel zeigt wie mehrere Agenten zusammenarbeiten:
  - Agent 1 (Pro)     - argumentiert FUER eine These
  - Agent 2 (Contra)  - argumentiert GEGEN dieselbe These
  - Agent 3 (Richter) - hoert beide Seiten und faellt ein Urteil

Neues Konzept: context=[]
  Jeder Agent bekommt die Ergebnisse der vorherigen Agenten
  als Kontext uebergeben. So "lesen" sie was die anderen
  geschrieben haben, bevor sie selbst antworten.

Ausprobieren: Aendere THESE zu einem anderen Thema!
"""

from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from display_helper import show

load_dotenv()

# ── Hier kannst du die These ändern ──────────────────────
THESE = "Soziale Medien sind gut fuer Jugendliche"
# ─────────────────────────────────────────────────────────


# ─────────────────────────────────────────────
# Agenten definieren
# ─────────────────────────────────────────────

pro_agent = Agent(
    role="Anwalt der Pro-Seite",
    goal=f"Verteidige ueberzeugend die These: '{THESE}'",
    backstory="""\
        Du bist ein brillanter Redner und Debattierer.
        Deine Aufgabe ist es, die beste moegliche Argumentation
        FUER eine These zu liefern - egal was du persoenlich denkst.
        Du verwendest Fakten, Beispiele und Logik.
    """,
    verbose=False,
)

contra_agent = Agent(
    role="Anwalt der Contra-Seite",
    goal=f"Widerlege ueberzeugend die These: '{THESE}'",
    backstory="""\
        Du bist ein brillanter Redner und Debattierer.
        Deine Aufgabe ist es, die beste moegliche Argumentation
        GEGEN eine These zu liefern - egal was du persoenlich denkst.
        Du verwendest Fakten, Beispiele und Logik.
        Du gehst gezielt auf die Argumente der Pro-Seite ein.
    """,
    verbose=False,
)

richter_agent = Agent(
    role="Unparteiischer Richter",
    goal="Bewerte die Debatte fair und faelle ein begruendetes Urteil.",
    backstory="""\
        Du bist ein erfahrener Richter und Mediator.
        Du hoerst beide Seiten einer Debatte und bewertest
        die Qualitaet der Argumente sachlich und fair.
        Du gibst keine persoenliche Meinung ab, sondern
        urteilst allein nach der Staerke der Argumentation.
    """,
    verbose=False,
)


# ─────────────────────────────────────────────
# Aufgaben definieren
# ─────────────────────────────────────────────

aufgabe_pro = Task(
    description=f"""\
        Die Debattenthese lautet: "{THESE}"

        Liefere 3 starke Argumente FUER diese These.
        Jedes Argument soll:
        - Eine klare Behauptung enthalten
        - Mit einem Beispiel oder Fakt unterstuetzt werden        

        Schreibe praegnant und ueberzeugend.
    """,
    expected_output="""\
        3 nummerierte Pro-Argumente mit je einer Begruendung
        und einem konkreten Beispiel.
    """,
    agent=pro_agent,
)

aufgabe_contra = Task(
    description=f"""\
        Die Debattenthese lautet: "{THESE}"

        Du hast die Pro-Argumente gelesen. Liefere nun 3 starke
        Argumente GEGEN diese These und gehe dabei gezielt auf
        die Pro-Argumente ein.
        Jedes Argument soll:
        - Eine klare Behauptung enthalten
        - Mit einem Beispiel oder Fakt unterstuetzt werden        
    """,
    expected_output="""\
        3 nummerierte Contra-Argumente mit je einer Begruendung,
        einem konkreten Beispiel und einem direkten Bezug auf
        das jeweilige Pro-Argument.
    """,
    agent=contra_agent,
    context=[aufgabe_pro],  # <-- liest die Pro-Argumente!
)

aufgabe_urteil = Task(
    description=f"""\
        Du hast beide Seiten der Debatte zur These "{THESE}" gelesen.

        Faelle jetzt ein Urteil:
        1. Fasse die staerksten Argumente beider Seiten kurz zusammen
        2. Bewerte welche Seite insgesamt ueberzeugender argumentiert hat
        3. Erklaere warum - bezogen auf Logik und Beweiskraft
        4. Formuliere ein abschliessendes Fazit in 2-3 Saetzen

        Bleibe fair und unparteiisch.
    """,
    expected_output="""\
        Ein strukturiertes Urteil mit Zusammenfassung beider Seiten,
        einer begruendeten Entscheidung und einem klaren Fazit.
    """,
    agent=richter_agent,
    context=[aufgabe_pro, aufgabe_contra],  # <-- liest beide Seiten!
)


# ─────────────────────────────────────────────
# Crew starten
# ─────────────────────────────────────────────

crew = Crew(
    agents=[pro_agent, contra_agent, richter_agent],
    tasks=[aufgabe_pro, aufgabe_contra, aufgabe_urteil],
    process=Process.sequential,
    verbose=False,
)

print(f'\nDebatte startet: "{THESE}"\n')

ergebnis = crew.kickoff()

show(f"""\
---
## Debatte: {THESE}

### Pro-Argumente
{aufgabe_pro.output.raw}

---
### Contra-Argumente
{aufgabe_contra.output.raw}

---
### Urteil des Richters
{ergebnis.raw}
""")
