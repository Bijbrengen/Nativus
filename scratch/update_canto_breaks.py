import os
import re

tex_dir = r"D:\repos\Nativus\TeX"
cantica_dir = os.path.join(tex_dir, 'Cantica')

for file in os.listdir(cantica_dir):
    if not file.endswith('.tex'): continue
    filepath = os.path.join(cantica_dir, file)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace \vspace{2em} before \begin{center} \Large \textbf{Canto with \clearpage
    content = re.sub(r'\\vspace\{2em\}\s*\\begin\{center\}\s*\\Large \\textbf\{Canto', r'\\clearpage\n\\begin{center}\n\\Large \\textbf{Canto', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Cantica Canto page breaks updated.")
