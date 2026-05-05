import os
import re

cantica_dir = r"D:\repos\Nativus\TeX\Cantica"

for file in os.listdir(cantica_dir):
    if not file.endswith('.tex'): continue
    filepath = os.path.join(cantica_dir, file)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Replace \chapter{Canticum 1\_ Emmys Lichaam}
    # Note: the \_ might literally be \_ or just _. Let's match carefully.
    def chapter_repl(match):
        num = match.group(1)
        name = match.group(2)
        return f"\\begin{{center}}\n\\Huge \\textbf{{Canticum {num}}} \\\\\n\\vspace{{0.5em}}\n\\Huge \\textbf{{{name}}}\n\\end{{center}}\n\\vspace{{2em}}"
        
    content = re.sub(r'\\chapter\{Canticum\s*(\d+)\\?_\s*(.*?)\}', chapter_repl, content)
    
    # We want to find the Canto block and reformat it.
    # It currently looks like:
    # \section*{Canto Naam}
    # \begin{center}
    # \textit{\input{../Muziek/Canto Naam_Stijl.tex}}
    # \end{center}
    # \input{../Muziek/Canto Naam_Noten.tex}
    # \begin{multicols}{3}
    # \input{../Canti/Opera Naam/Canto Naam.tex}
    # \end{multicols}
    
    # Let's rebuild the file line by line to be safer.
    lines = content.split('\n')
    new_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        canto_match = re.match(r'\\section\*\{(Canto .*?)\}', line)
        if canto_match:
            canto_name = canto_match.group(1).strip()
            
            # Skip the next few lines that we know are part of the old block
            # \begin{center}, \textit{\input{...}}, \end{center}, \input{..._Noten.tex}
            # \begin{multicols}{3}, \input{../Canti/...}, \end{multicols}
            
            j = i + 1
            input_line = ""
            while j < len(lines):
                if '\\input{../Canti/' in lines[j]:
                    input_line = lines[j]
                if '\\end{multicols}' in lines[j]:
                    break
                j += 1
                
            # Now output the new block
            new_lines.append("\\vspace{2em}")
            new_lines.append("\\begin{center}")
            new_lines.append(f"\\Large \\textbf{{{canto_name}}} \\\\")
            new_lines.append("\\vspace{0.5em}")
            new_lines.append(f"\\normalsize \\input{{../Muziek/{canto_name}_Stijl.tex}}")
            new_lines.append("\\end{center}")
            new_lines.append(f"\\input{{../Muziek/{canto_name}_Noten.tex}}")
            new_lines.append("\\vspace{1em}")
            new_lines.append("\\begin{multicols}{3}")
            new_lines.append("\\raggedright")
            new_lines.append("\\obeylines")
            if input_line:
                new_lines.append(input_line)
            else:
                new_lines.append(f"\\input{{../Canti/Opera Onbekend/{canto_name}.tex}}") # Fallback
            new_lines.append("\\end{multicols}")
            
            i = j # Move pointer to \end{multicols}
        else:
            new_lines.append(line)
        i += 1
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))

print("Cantica formatting updated successfully.")
