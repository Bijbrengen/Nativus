import os

tex_dir = r"D:\repos\Nativus\TeX"
cantica_dir = os.path.join(tex_dir, 'Cantica')

# 1. Update preamble.tex
preamble_path = os.path.join(tex_dir, 'preamble.tex')
with open(preamble_path, 'r', encoding='utf-8') as f:
    preamble = f.read()

macro = r"""
\makeatletter
{\catcode`\^^M=\active %
 \gdef\obeylinesandstanzas{%
  \catcode`\^^M=\active %
  \def^^M{\futurelet\next\check@newline}%
 }%
 \gdef\check@newline{%
  \ifx\next^^M%
    \expandafter\stanza@break%
  \else%
    \\%
  \fi%
 }%
 \gdef\stanza@break^^M{%
  \par\vspace{1em}\noindent%
 }%
}
\makeatother

\newcommand{\inputcanto}[1]{%
  \begingroup
  \interlinepenalty=10000
  \obeylinesandstanzas
  \noindent\input{#1}%
  \endgroup
}
"""

if r"\inputcanto" not in preamble:
    preamble += "\n" + macro + "\n"
    with open(preamble_path, 'w', encoding='utf-8') as f:
        f.write(preamble)

# 2. Update Cantica files
for file in os.listdir(cantica_dir):
    if not file.endswith('.tex'): continue
    filepath = os.path.join(cantica_dir, file)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace("\\obeylines\n\\input", "\\inputcanto")
    
    # Add clearpage before Canticum title if not there
    if "\\begin{center}\n\\Huge \\textbf{Canticum" in content:
        content = content.replace("\\begin{center}\n\\Huge \\textbf{Canticum", "\\clearpage\n\\begin{center}\n\\Huge \\textbf{Canticum")
        
    # Also add clearpage before each Canto
    # The user said "Daarna komt elke canto op een nieuwe regel" but earlier we determined they might want spacing.
    # Let's just fix the \clearpage for Canticum for now, as they specifically mentioned "Tussen Opera Emmy en het eerste canto zit GEEN /newpage".
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Parser installed and Cantica updated with clearpage.")
