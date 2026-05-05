import os

tex_dir = r"D:\repos\Nativus\TeX"
trilogie_dir = os.path.join(tex_dir, 'Trilogie')

for file in os.listdir(trilogie_dir):
    if not file.endswith('.tex'): continue
    filepath = os.path.join(trilogie_dir, file)
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    out_lines = []
    in_center = False
    in_cantos = False
    
    # We will build the new content from scratch based on the old content
    trilogia_num = ""
    trilogia_title = ""
    trilogia_subtitle = ""
    trilogia_author = "MAYA"
    
    # Hardcoded mapping based on the files
    if "1." in file:
        trilogia_num = "Trilogia 1"
        trilogia_title = "Op jacht naar Emmy Nativus"
        trilogia_subtitle = "De fysieke en aardse worstelingen"
    elif "2." in file:
        trilogia_num = "Trilogia 2"
        trilogia_title = "Gevangen in Emmy Nativus"
        trilogia_subtitle = "De mentale worstelingen en innerlijke conflicten"
    elif "3." in file:
        trilogia_num = "Trilogia 3"
        trilogia_title = "Bevrijd door Emmy Nativus"
        trilogia_subtitle = "Spirituele groei en uiteindelijke transformatie"
        
    out_lines.append("\\documentclass{book}\n")
    out_lines.append("\\input{../preamble.tex}\n")
    out_lines.append("\\begin{document}\n\n")
    
    out_lines.append(f"\\trilogiatitle{{{trilogia_num}}}{{{trilogia_title}}}{{{trilogia_subtitle}}}{{{trilogia_author}}}\n\n")
    
    # Parse the rest
    for line in lines:
        line = line.strip()
        if not line: continue
        if line.startswith(r"\documentclass") or line.startswith(r"\input") or line.startswith(r"\begin{document}") or line.startswith(r"\end{document}"):
            continue
        if line.startswith(r"\begin{center}") or line.startswith(r"\end{center}"):
            continue
        if line.startswith(r"\vspace") or line.startswith(r"0. Voorpagina"):
            continue
        if line.startswith(r"\Huge") or line.startswith(r"\Large \textbf{Trilogia"):
            continue
        if line.startswith("Op jacht naar") or line.startswith("Gevangen in") or line.startswith("Bevrijd door"):
            continue
        if line.startswith("De fysieke") or line.startswith("De mentale") or line.startswith("Spirituele"):
            continue
        if line == "MAYA" or line == r"MAYA \\":
            continue
            
        # We are left with Opera, Canticum, and Cantos.
        if line.startswith(r"\Large \textbf{Opera"):
            if in_cantos:
                out_lines.append("\\end{cantoindex}\n")
                in_cantos = False
            # extract Opera name
            # format: \Large \textbf{Opera 1: Emmy} \\
            name = line.replace(r"\Large \textbf{", "").replace(r"} \\", "").replace(r"}", "")
            out_lines.append(f"\\operaindex{{{name}}}\n")
        elif line.startswith(r"\large \textit{Canticum"):
            if in_cantos:
                out_lines.append("\\end{cantoindex}\n")
                in_cantos = False
            # extract Canticum name
            name = line.replace(r"\large \textit{", "").replace(r"} \\", "").replace(r"}", "")
            out_lines.append(f"\\canticumindex{{{name}}}\n")
        else:
            # It's a Canto!
            if not in_cantos:
                out_lines.append("\\begin{cantoindex}\n")
                in_cantos = True
            name = line.replace(r" \\", "")
            out_lines.append(f"  \\item{{{name}}}\n")
            
    if in_cantos:
        out_lines.append("\\end{cantoindex}\n")
        
    out_lines.append("\n\\end{document}\n")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(out_lines)

print("Trilogia files parsed and updated.")
