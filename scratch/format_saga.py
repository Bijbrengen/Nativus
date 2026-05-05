import os

tex_dir = r"D:\repos\Nativus\TeX"
saga_path = os.path.join(tex_dir, 'Saga Nativus.tex')

with open(saga_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    
out_lines = []
out_lines.append("\\documentclass{book}\n")
out_lines.append("\\input{preamble.tex}\n")
out_lines.append("\\begin{document}\n\n")
out_lines.append("\\sagatitle{Saga Nativus}\n\n")

in_cantos = False
current_trilogia = ""

# Hardcoded mapping for subtitles
subtitles = {
    "Trilogia 1": "De fysieke en aardse worstelingen",
    "Trilogia 2": "De mentale worstelingen en innerlijke conflicten",
    "Trilogia 3": "Spirituele groei en uiteindelijke transformatie"
}
titles = {
    "Trilogia 1": "Op jacht naar Emmy Nativus",
    "Trilogia 2": "Gevangen in Emmy Nativus",
    "Trilogia 3": "Bevrijd door Emmy Nativus"
}

for line in lines:
    line = line.strip()
    if not line: continue
    if line.startswith(r"\documentclass") or line.startswith(r"\input") or line.startswith(r"\begin{document}") or line.startswith(r"\end{document}"):
        continue
    if line.startswith(r"\begin{center}") or line.startswith(r"\end{center}"):
        continue
    if line.startswith(r"\vspace") or line.startswith(r"0. Voorpagina"):
        continue
    if line.startswith(r"\Huge \textbf{Saga"):
        continue
        
    if line.startswith(r"\Large \textbf{Trilogia"):
        if in_cantos:
            out_lines.append("\\end{cantoindex}\n")
            in_cantos = False
        num = line.replace(r"\Large \textbf{", "").replace(r"}", "").replace(r" \\", "").strip()
        current_trilogia = num
        out_lines.append(f"\\trilogiatitle{{{num}}}{{{titles.get(num, '')}}}{{{subtitles.get(num, '')}}}{{MAYA}}\n")
    elif line.startswith(r"\Large \textbf{Opera"):
        if in_cantos:
            out_lines.append("\\end{cantoindex}\n")
            in_cantos = False
        name = line.replace(r"\Large \textbf{", "").replace(r"}", "").replace(r" \\", "").strip()
        out_lines.append(f"\\operaindex{{{name}}}\n")
    elif line.startswith(r"\large \textit{Canticum"):
        if in_cantos:
            out_lines.append("\\end{cantoindex}\n")
            in_cantos = False
        name = line.replace(r"\large \textit{", "").replace(r"}", "").replace(r" \\", "").strip()
        out_lines.append(f"\\canticumindex{{{name}}}\n")
    elif any(trig in line for trig in titles.values()) or any(sub in line for sub in subtitles.values()) or line == "MAYA":
        continue
    else:
        # Canto
        if not in_cantos:
            out_lines.append("\\begin{cantoindex}\n")
            in_cantos = True
        name = line.replace(r" \\", "").strip()
        out_lines.append(f"  \\item{{{name}}}\n")

if in_cantos:
    out_lines.append("\\end{cantoindex}\n")

out_lines.append("\n\\end{document}\n")

with open(saga_path, 'w', encoding='utf-8') as f:
    f.writelines(out_lines)

print("Saga Nativus.tex updated.")
