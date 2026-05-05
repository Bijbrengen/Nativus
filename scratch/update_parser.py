import os

tex_dir = r"D:\repos\Nativus\TeX"
preamble_path = os.path.join(tex_dir, 'preamble.tex')

with open(preamble_path, 'r', encoding='utf-8') as f:
    preamble = f.read()

# We need to replace the old macro with the new one.
# Let's just find where it starts and ends.
start_idx = preamble.find(r"\makeatletter")
end_idx = preamble.find(r"\endgroup", start_idx) + len(r"\endgroup") + 2

new_macro = r"""
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
  \par\end{minipage}\vspace{1em}\par\noindent\begin{minipage}{\columnwidth}%
 }%
}
\makeatother

\newcommand{\inputcanto}[1]{%
  \begingroup
  \noindent\begin{minipage}{\columnwidth}%
  \obeylinesandstanzas
  \input{#1}\par\end{minipage}%
  \endgroup
}
"""

if start_idx != -1:
    preamble = preamble[:start_idx] + new_macro + preamble[end_idx:]
    with open(preamble_path, 'w', encoding='utf-8') as f:
        f.write(preamble)

print("Updated preamble with minipage parser.")
