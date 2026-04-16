"""
Hilfsfunktion: Markdown-Ausgabe fuer Notebook und Konsole
"""


def show(markdown_text: str):
    """
    Gibt Markdown-Text aus - formatiert im Notebook, als Text in der Konsole.
    """
    try:
        from IPython import get_ipython

        if get_ipython() is not None:
            from IPython.display import display, Markdown

            display(Markdown(markdown_text))
            return
    except ImportError:
        pass

    # Konsolen-Ausgabe: einfache Markdown-Zeichen entfernen
    import re

    text = markdown_text
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)  # **fett** -> fett
    text = re.sub(r"\*(.+?)\*", r"\1", text)  # *kursiv* -> kursiv
    text = re.sub(r"^#{1,6} ", "", text, flags=re.MULTILINE)  # ## Titel -> Titel
    text = re.sub(r"`(.+?)`", r"\1", text)  # `code` -> code
    print(text)
