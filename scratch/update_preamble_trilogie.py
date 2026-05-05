import os

tex_dir = r"D:\repos\Nativus\TeX"
preamble_path = os.path.join(tex_dir, 'preamble.tex')

with open(preamble_path, 'r', encoding='utf-8') as f:
    preamble = f.read()

macros = r"""
\usepackage{xcolor}

\newcommand{\trilogiatitle}[4]{%
  \begin{center}
    {\Large #1} \\[0.5em]
    {\Huge \textbf{#2}} \\[0.5em]
    {\large \textcolor{gray}{#3}} \\[1em]
    {\small \textbf{#4}}
  \end{center}
  \vspace{3em}
}

\newcommand{\operaindex}[1]{%
  \vspace{1.5em}
  \noindent{\Large #1} \par\vspace{1em}
}

\newcommand{\canticumindex}[1]{%
  \vspace{0.5em}
  \noindent\textcolor{blue}{\underline{#1}} \par
}

\newenvironment{cantoindex}{%
  \begin{enumerate}
    \color{blue}
    \let\olditem\item
    \renewcommand{\item}[1]{\olditem \underline{##1}}
}{%
  \end{enumerate}
}
"""

if r"\trilogiatitle" not in preamble:
    preamble += "\n" + macros + "\n"
    with open(preamble_path, 'w', encoding='utf-8') as f:
        f.write(preamble)

print("Updated preamble with Trilogie macros.")
