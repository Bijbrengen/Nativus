import os
import re

tex_dir = r"D:\repos\Nativus\TeX"
trilogie_dir = os.path.join(tex_dir, 'Trilogie')
cantica_dir = os.path.join(tex_dir, 'Cantica')

# Get a list of all Canticum files to match numbers
canticum_files = [f for f in os.listdir(cantica_dir) if f.endswith('.tex')]

def get_canticum_file(num):
    for f in canticum_files:
        if f"Canticum {num}_" in f:
            return f"../Cantica/{f}"
    return None

# Update Trilogia files
for file in os.listdir(trilogie_dir):
    if not file.endswith('.tex'): continue
    filepath = os.path.join(trilogie_dir, file)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the manual index part with automated calls
    # We look for \operaindex and then any canticum/canto lists
    # We will reconstruct the index part
    
    # 1. Keep the preamble and title
    header_match = re.search(r'(\\trilogiatitle\{[^}]+\}\{[^}]+\}\{[^}]+\}\{[^}]+\})', content)
    header = header_match.group(1) if header_match else ""
    
    new_content = "\\documentclass{book}\n\\input{../preamble.tex}\n\\begin{document}\n\n"
    new_content += header + "\n\n"
    
    # 2. Extract Opera names and their Canticum numbers
    operas = re.findall(r'\\operaindex\{Opera (\d+): ([^}]+)\}', content)
    for op_num, op_name in operas:
        new_content += f"\\operaindex{{Opera {op_num}: {op_name}}}\n"
        
        # Find which Canticum numbers belong to this opera
        # This is a bit tricky to parse from the old file, so we'll use the numbering logic
        # Opera 1 -> Canticum 1
        # Opera 2 -> Canticum 2, 3, 4
        # Opera 3 -> Canticum 5, 6, 7
        # Opera 4 -> Canticum 8, 9, 10
        # Opera 5 -> Canticum 11, 12, 13
        # Opera 6 -> Canticum 14, 15, 16
        # Opera 7 -> Canticum 17, 18, 19
        # Opera 8 -> Canticum 20, 21, 22
        # Opera 9 -> Canticum 23, 24
        
        op_num_int = int(op_num)
        cantica_nums = []
        if op_num_int == 1: cantica_nums = [1]
        elif op_num_int == 2: cantica_nums = [2, 3, 4]
        elif op_num_int == 3: cantica_nums = [5, 6, 7]
        elif op_num_int == 4: cantica_nums = [8, 9, 10]
        elif op_num_int == 5: cantica_nums = [11, 12, 13]
        elif op_num_int == 6: cantica_nums = [14, 15, 16]
        elif op_num_int == 7: cantica_nums = [17, 18, 19]
        elif op_num_int == 8: cantica_nums = [20, 21, 22]
        elif op_num_int == 9: cantica_nums = [23, 24]
        
        for c_num in cantica_nums:
            c_file = get_canticum_file(c_num)
            if c_file:
                new_content += f"\\includeCanticumIndex{{{c_file}}}\n"
                
    new_content += "\n\\end{document}\n"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

print("Trilogia files automated.")

# Update Saga file
saga_path = os.path.join(tex_dir, 'Saga Nativus.tex')
with open(saga_path, 'w', encoding='utf-8') as f:
    f.write("\\documentclass{book}\n\\input{preamble.tex}\n\\begin{document}\n\n")
    f.write("\\sagatitlepage{Saga}{Emmy Nativus}{een beschamende autobiografie}{van een innerlijk leven}{in een mystiek-erotische versroman}{MAYA BEEBRINGER}\n\n")
    
    # Loop through all 3 Trilogies
    trilogies = [
        ("Trilogia 1", "Op jacht naar Emmy Nativus", "De fysieke en aardse worstelingen", [1, 2, 3]),
        ("Trilogia 2", "Gevangen in Emmy Nativus", "De mentale worstelingen en innerlijke conflicten", [4, 5, 6]),
        ("Trilogia 3", "Bevrijd door Emmy Nativus", "Spirituele groei en uiteindelijke transformatie", [7, 8, 9])
    ]
    
    operas_data = {
        1: "Emmy", 2: "Emma", 3: "Svenska",
        4: "Heidi", 5: "Sophia", 6: "Greta",
        7: "Jeanne", 8: "Sadeeqat", 9: "Agape"
    }
    
    for t_num, t_title, t_sub, op_nums in trilogies:
        f.write(f"\\trilogiatitle{{{t_num}}}{{{t_title}}}{{{t_sub}}}{{MAYA}}\n")
        for op_num in op_nums:
            f.write(f"\\operaindex{{Opera {op_num}: {operas_data[op_num]}}}\n")
            
            cantica_nums = []
            if op_num == 1: cantica_nums = [1]
            elif op_num == 2: cantica_nums = [2, 3, 4]
            elif op_num == 3: cantica_nums = [5, 6, 7]
            elif op_num == 4: cantica_nums = [8, 9, 10]
            elif op_num == 5: cantica_nums = [11, 12, 13]
            elif op_num == 6: cantica_nums = [14, 15, 16]
            elif op_num == 7: cantica_nums = [17, 18, 19]
            elif op_num == 8: cantica_nums = [20, 21, 22]
            elif op_num == 9: cantica_nums = [23, 24]
            
            for c_num in cantica_nums:
                # In Saga, the path is relative to the TeX folder
                c_file_raw = get_canticum_file(c_num)
                if c_file_raw:
                    c_file = c_file_raw.replace("../", "")
                    f.write(f"\\includeCanticumIndex{{{c_file}}}\n")
        f.write("\\clearpage\n\n")
    
    f.write("\\end{document}\n")

print("Saga Nativus.tex automated.")
