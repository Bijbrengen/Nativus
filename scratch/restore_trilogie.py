import os

tex_dir = r"D:\repos\Nativus\TeX"
trilogie_dir = os.path.join(tex_dir, 'Trilogie')

data = {
    "Trilogia 1. Op jacht naar Emmy Nativus.tex": {
        "num": "Trilogia 1",
        "title": "Op jacht naar Emmy Nativus",
        "sub": "De fysieke en aardse worstelingen",
        "content": r"""
\operaindex{Opera 1: Emmy}
\canticumindex{Canticum 1: Emmy’s Lichaam}
\begin{cantoindex}
  \cantoitem{Angst}
  \cantoitem{Jagershut}
  \cantoitem{Es}
  \cantoitem{Klooster}
  \cantoitem{Waterbevalling}
  \cantoitem{Uitvlucht}
\end{cantoindex}
\operaindex{Opera 2: Emma}
\canticumindex{Canticum 2: Emma’s Lichaam}
\canticumindex{Canticum 3: Emma’s Geest}
\canticumindex{Canticum 4: Emma’s Ziel}
\operaindex{Opera 3: Svenska}
\canticumindex{Canticum 5: Svenska’s Lichaam}
\canticumindex{Canticum 6: Svenska’s Geest}
\canticumindex{Canticum 7: Svenska’s Ziel}
"""
    },
    "Trilogia 2. Gevangen in Emmy Nativus.tex": {
        "num": "Trilogia 2",
        "title": "Gevangen in Emmy Nativus",
        "sub": "De mentale worstelingen en innerlijke conflicten",
        "content": r"""
\operaindex{Opera 4: Heidi}
\canticumindex{Canticum 8: Heidi’s Lichaam}
\canticumindex{Canticum 9: Heidi’s Geest}
\canticumindex{Canticum 10: Heidi’s Ziel}
\operaindex{Opera 5: Sophia}
\canticumindex{Canticum 11: Sophia’s Lichaam}
\canticumindex{Canticum 12: Sophia’s Geest}
\canticumindex{Canticum 13: Sophia’s Ziel}
\operaindex{Opera 6: Greta}
\canticumindex{Canticum 14: Greta’s Lichaam}
\canticumindex{Canticum 15: Greta’s Geest}
\canticumindex{Canticum 16: Greta’s Ziel}
"""
    },
    "Trilogia 3. Bevrijd door Emmy Nativus.tex": {
        "num": "Trilogia 3",
        "title": "Bevrijd door Emmy Nativus",
        "sub": "Spirituele groei en uiteindelijke transformatie",
        "content": r"""
\operaindex{Opera 7: Jeanne}
\canticumindex{Canticum 17: Jeanne’s Lichaam}
\canticumindex{Canticum 18: Jeanne’s Geest}
\canticumindex{Canticum 19: Jeanne’s Ziel}
\operaindex{Opera 8: Sadeeqat}
\canticumindex{Canticum 20: Sadeeqat’s Lichaam}
\canticumindex{Canticum 21: Sadeeqat’s Geest}
\canticumindex{Canticum 22: Sadeeqat’s Ziel}
\operaindex{Opera 9: Agape}
\canticumindex{Canticum 23: Agape’s Ziel}
\canticumindex{Canticum 24: Nawoord}
"""
    }
}

for filename, info in data.items():
    filepath = os.path.join(trilogie_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("\\documentclass{book}\n")
        f.write("\\input{../preamble.tex}\n")
        f.write("\\begin{document}\n\n")
        f.write(f"\\trilogiatitle{{{info['num']}}}{{{info['title']}}}{{{info['sub']}}}{{MAYA}}\n")
        f.write(info['content'])
        f.write("\n\\end{document}\n")

print("Trilogia files restored.")
