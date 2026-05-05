import os
import re

tex_dir = r"D:\repos\Nativus\TeX"
cantica_dir = os.path.join(tex_dir, 'Cantica')

for file in os.listdir(cantica_dir):
    if not file.endswith('.tex'): continue
    filepath = os.path.join(cantica_dir, file)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Extract Canticum number and title
    # \Huge \textbf{Canticum (\d+)}
    # \Huge \textbf{([^}]+)}
    num_match = re.search(r'Canticum (\d+)', content)
    num = num_match.group(1) if num_match else "?"
    
    # Title is the next \Huge \textbf
    title_match = re.search(r'\\Huge \\textbf\{Canticum ' + num + r'\}' + r'.*?\\Huge \\textbf\{([^}]+)\}', content, re.DOTALL)
    if not title_match:
        # try simpler match
        title_match = re.search(r'\\Huge \\textbf\{([^}]+)\}', content.split('Canticum')[1])
    title = title_match.group(1).strip() if title_match else "?"

    # 2. Extract Canto blocks
    # We look for \Large \textbf{Canto ([^}]+)}
    # and \inputcanto{../Canti/([^/]+)/
    cantos = []
    # Find all occurrences of Canto titles and their subdirs
    canto_titles = re.findall(r'\\Large \\textbf\{Canto ([^}]+)\}', content)
    subdirs = re.findall(r'\\inputcanto\{\.\./Canti/([^/]+)/', content)
    
    new_content = f"\\canticumtitle{{{num}}}{{{title}}}\n\n"
    
    for c_title, c_subdir in zip(canto_titles, subdirs):
        new_content += f"\\renderCanto{{{c_title}}}{{{c_subdir}}}\n"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

print("Cantica files refactored to use macros.")
