import os
import re

cantica_dir = r"D:\repos\Nativus\TeX\Cantica"
muziek_dir = r"D:\repos\Nativus\TeX\Muziek"

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

ensure_dir(muziek_dir)

for file in os.listdir(cantica_dir):
    if not file.endswith('.tex'): continue
    filepath = os.path.join(cantica_dir, file)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # We will rebuild the content
    lines = content.split('\n')
    new_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Match \section*{Canto [Naam] --- [Stijl]}
        match = re.match(r'\\section\*\{(Canto [A-Za-z0-9_ëïéáíóúàèìòù ]+)(?:\s*---\s*(.*))?\}', line)
        if match:
            canto_name = match.group(1).strip()
            style_part_1 = match.group(2)
            if style_part_1 is None:
                style_part_1 = ""
            style_part_1 = style_part_1.strip()
            
            # Read old Muziek file if it exists
            old_muziek_path = os.path.join(muziek_dir, f"{canto_name}.tex")
            style_part_2 = ""
            if os.path.exists(old_muziek_path):
                with open(old_muziek_path, 'r', encoding='utf-8') as f_old:
                    style_part_2 = f_old.read().strip()
                # Remove the old file
                os.remove(old_muziek_path)
                
            # Combine
            full_style = style_part_1
            if style_part_2:
                if full_style:
                    full_style += "\n" + style_part_2
                else:
                    full_style = style_part_2
                    
            # Write _Stijl.tex and _Noten.tex
            stijl_path = os.path.join(muziek_dir, f"{canto_name}_Stijl.tex")
            with open(stijl_path, 'w', encoding='utf-8') as f_stijl:
                f_stijl.write(full_style + "\n")
                
            noten_path = os.path.join(muziek_dir, f"{canto_name}_Noten.tex")
            if not os.path.exists(noten_path):
                with open(noten_path, 'w', encoding='utf-8') as f_noten:
                    f_noten.write("% Plaats hier de MusixTeX notenbalk\n")
                    
            # Write new Canticum structure
            new_lines.append(f"\\section*{{{canto_name}}}")
            new_lines.append("\\begin{center}")
            new_lines.append(f"\\textit{{\\input{{../Muziek/{canto_name}_Stijl.tex}}}}")
            new_lines.append("\\end{center}")
            new_lines.append(f"\\input{{../Muziek/{canto_name}_Noten.tex}}")
            
            # Skip the next line if it is the old \input{../Muziek/Canto Naam.tex}
            if i + 1 < len(lines) and '\\input{../Muziek/Canto ' in lines[i+1]:
                i += 1
                
        else:
            new_lines.append(line)
        i += 1
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))

print("Refactored Cantica and Muziek files successfully.")
