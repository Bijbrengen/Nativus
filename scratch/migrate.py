import os
import shutil
import docx
import pandas as pd
import re

SRC_DIR = r"D:\repos\Nativus\Google drive"
DEST_DIR = r"D:\repos\Nativus\TeX"

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def escape_latex(text):
    # Escape special LaTeX characters except % because it is used for comments
    # Also escape ^ and ~ with text versions if needed, but simple sub is okay
    text = re.sub(r'([_&$#{}])', r'\\\1', text)
    return text

def process_canto(docx_path, dest_tex_path):
    doc = docx.Document(docx_path)
    lines = [p.text for p in doc.paragraphs]
    
    # Extract Header (first two lines usually)
    canto_title = ""
    music_style = ""
    start_idx = 0
    
    if len(lines) > 0 and lines[0].startswith("Canto"):
        canto_title = lines[0].strip()
        start_idx += 1
        if len(lines) > 1 and lines[1].strip() != "":
            music_style = lines[1].strip()
            start_idx += 1
            
    # Fallback
    if not canto_title:
        for i, line in enumerate(lines):
            if line.strip().startswith("Canto"):
                canto_title = line.strip()
                start_idx = i + 1
                if start_idx < len(lines) and lines[start_idx].strip() != "":
                    music_style = lines[start_idx].strip()
                    start_idx += 1
                break

    # Extract Verses
    stanzas = []
    current_stanza = []
    
    for line in lines[start_idx:]:
        text = line.strip()
        if text.startswith('%'):
            current_stanza.append(text)
        elif text == "":
            if current_stanza:
                stanzas.append(current_stanza)
                current_stanza = []
        else:
            if '%' in text:
                parts = text.split('%', 1)
                text = escape_latex(parts[0].strip()) + " % " + parts[1].strip()
            else:
                text = escape_latex(text)
            current_stanza.append(text)
            
    if current_stanza:
        stanzas.append(current_stanza)
        
    # Write to .tex
    ensure_dir(os.path.dirname(dest_tex_path))
    with open(dest_tex_path, 'w', encoding='utf-8') as f:
        for stanza in stanzas:
            f.write("\\begin{minipage}{\\columnwidth}\n")
            f.write("\\begin{verse}\n")
            for i, line in enumerate(stanza):
                if line.startswith('%'):
                    f.write(line + "\n")
                else:
                    if i < len(stanza) - 1:
                        f.write(line + "\\\\\n")
                    else:
                        f.write(line + "\n")
            f.write("\\end{verse}\n")
            f.write("\\end{minipage}\n\\vspace{1em}\n\n")
            
    return escape_latex(canto_title), escape_latex(music_style)

def main():
    ensure_dir(DEST_DIR)
    
    # 1. Parse Indice
    indice_path = os.path.join(SRC_DIR, "Administratie", "Indice.xlsx")
    df = pd.read_excel(indice_path, sheet_name="Canti")
    
    # Create mappings
    canticum_to_canti = {}
    opera_to_cantica = {}
    
    for idx, row in df.iterrows():
        canto_name = str(row['Canto']).strip()
        canticum_num = row['Canticum']
        opera_name = str(row['Plot']).strip()
        
        if pd.isna(canto_name) or canto_name == 'nan':
            continue
            
        canto_full_name = f"Canto {canto_name}"
        
        # Determine Opera
        if pd.notna(opera_name) and opera_name != 'nan':
            opera_full = f"Opera {opera_name}"
        else:
            opera_full = "Opera Onbekend"
            
        # Determine Canticum
        if pd.notna(canticum_num):
            try:
                canticum_int = int(canticum_num)
                cant_str = str(canticum_int)
            except ValueError:
                cant_str = str(canticum_num)
        else:
            cant_str = "Onbekend"
            
        if cant_str not in canticum_to_canti:
            canticum_to_canti[cant_str] = []
        
        canticum_to_canti[cant_str].append({
            'canto': canto_full_name,
            'opera': opera_full,
            'raw_name': canto_name
        })
        
        if opera_full not in opera_to_cantica:
            opera_to_cantica[opera_full] = set()
        opera_to_cantica[opera_full].add(cant_str)

    # Walk source directory for Canti
    canti_src_dir = os.path.join(SRC_DIR, "Canti")
    canto_metadata = {}
    
    for root, dirs, files in os.walk(canti_src_dir):
        for file in files:
            if file.endswith('.docx') and file.startswith('Canto'):
                docx_path = os.path.join(root, file)
                rel_path = os.path.relpath(docx_path, canti_src_dir)
                dest_tex_path = os.path.join(DEST_DIR, "Canti", rel_path).replace('.docx', '.tex')
                
                canto_title, music_style = process_canto(docx_path, dest_tex_path)
                canto_metadata[file.replace('.docx', '')] = {
                    'title': canto_title,
                    'music': music_style,
                    'tex_path': os.path.join("Canti", rel_path).replace('.docx', '.tex').replace('\\', '/')
                }
                
    print(f"Processed {len(canto_metadata)} Canto files.")
    
    # Map real Canticum docx names
    cantica_src_dir = os.path.join(SRC_DIR, "Cantica")
    canticum_real_names = {}
    if os.path.exists(cantica_src_dir):
        for file in os.listdir(cantica_src_dir):
            if file.endswith('.docx') and file.startswith('Canticum'):
                parts = file.split('_', 1)
                if len(parts) > 1:
                    num_part = parts[0].replace('Canticum', '').strip()
                    canticum_real_names[num_part] = file.replace('.docx', '')
                    
    # Generate Cantica files
    cantica_dest_dir = os.path.join(DEST_DIR, "Cantica")
    ensure_dir(cantica_dest_dir)
    
    opere_dest_dir = os.path.join(DEST_DIR, "Opere")
    ensure_dir(opere_dest_dir)
    
    generated_opere = []
    
    for opera, cantica_nums in opera_to_cantica.items():
        if opera == "Opera Onbekend": continue
        
        opera_src_dir = os.path.join(SRC_DIR, "Opere")
        real_opera_name = opera
        if os.path.exists(opera_src_dir):
            for file in os.listdir(opera_src_dir):
                if file.endswith('.docx') and opera.split()[-1] in file:
                    real_opera_name = file.replace('.docx', '')
                    break
                    
        opera_tex_path = os.path.join(opere_dest_dir, f"{real_opera_name}.tex")
        generated_opere.append(f"Opere/{real_opera_name}.tex")
        
        with open(opera_tex_path, 'w', encoding='utf-8') as f_op:
            f_op.write("\\documentclass{book}\n")
            f_op.write("\\usepackage[utf8]{inputenc}\n")
            f_op.write("\\usepackage{multicol}\n")
            f_op.write("\\usepackage{verse}\n")
            f_op.write("\\usepackage{standalone}\n\n")
            f_op.write("\\begin{document}\n\n")
            
            escaped_opera_name = escape_latex(real_opera_name)
            f_op.write(f"\\chapter*{{{escaped_opera_name}}}\n\n")
            
            sorted_cant_nums = sorted(list(cantica_nums), key=lambda x: int(x) if str(x).isdigit() else 999)
            
            for cant_num in sorted_cant_nums:
                real_cant_name = canticum_real_names.get(str(cant_num), f"Canticum {cant_num}")
                cant_tex_path = os.path.join(cantica_dest_dir, f"{real_cant_name}.tex")
                
                with open(cant_tex_path, 'w', encoding='utf-8') as f_cant:
                    escaped_cant_name = escape_latex(real_cant_name)
                    f_cant.write(f"\\chapter{{{escaped_cant_name}}}\n\n")
                    
                    canti_list = canticum_to_canti.get(str(cant_num), [])
                    for c in canti_list:
                        canto_name = c['canto']
                        meta = canto_metadata.get(canto_name)
                        
                        if meta:
                            title = meta['title']
                            music = meta['music']
                            tex_path = meta['tex_path']
                            
                            f_cant.write(f"\\section*{{{title} --- {music}}}\n")
                            f_cant.write(f"\\input{{../Muziek/{canto_name}.tex}} % Placeholder for MusixTeX\n")
                            f_cant.write("\\begin{multicols}{3}\n")
                            f_cant.write(f"\\input{{../{tex_path}}}\n")
                            f_cant.write("\\end{multicols}\n\n")
                        else:
                            pass
                            
                f_op.write(f"\\input{{../Cantica/{real_cant_name}.tex}}\n")
                
            f_op.write("\n\\end{document}\n")

    # Generate Saga Nativus master file
    saga_path = os.path.join(DEST_DIR, "Saga Nativus.tex")
    with open(saga_path, 'w', encoding='utf-8') as f_saga:
        f_saga.write("\\documentclass{book}\n")
        f_saga.write("\\usepackage[utf8]{inputenc}\n")
        f_saga.write("\\usepackage{multicol}\n")
        f_saga.write("\\usepackage{verse}\n")
        f_saga.write("\\usepackage{standalone}\n\n")
        f_saga.write("\\title{Saga Nativus}\n")
        f_saga.write("\\author{Author}\n")
        f_saga.write("\\begin{document}\n\n")
        f_saga.write("\\maketitle\n\n")
        
        def get_op_num(path):
            import re
            m = re.search(r'Opera (\d+)', path)
            return int(m.group(1)) if m else 999
            
        generated_opere.sort(key=get_op_num)
        
        for op_path in generated_opere:
            f_saga.write(f"\\input{{{op_path}}}\n")
            
        f_saga.write("\n\\end{document}\n")
        
    print("Migration complete!")

if __name__ == "__main__":
    main()
