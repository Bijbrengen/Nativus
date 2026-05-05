import os
import re

tex_dir = r"D:\repos\Nativus\TeX"
cantica_dir = os.path.join(tex_dir, 'Cantica')

for file in os.listdir(cantica_dir):
    if not file.endswith('.tex'): continue
    filepath = os.path.join(cantica_dir, file)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We want to find the \clearpage\n\begin{center}\n\Huge \textbf{Canticum X} ... \end{center}\n\vspace{2em}
    # and replace it with a full dedicated title page.
    
    def repl_title(match):
        return f"\\clearpage\n\\vspace*{{\\fill}}\n\\begin{{center}}\n{match.group(1)}\n\\end{{center}}\n\\vspace*{{\\fill}}\n\\clearpage"
        
    content = re.sub(r'\\clearpage\s*\\begin\{center\}\s*(.*?)\\end\{center\}\s*\\vspace\{2em\}', repl_title, content, flags=re.DOTALL)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Cantica title pages updated.")
