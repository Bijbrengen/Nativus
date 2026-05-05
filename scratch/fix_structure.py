import os

cantica_dir = r"D:\repos\Nativus\TeX\Cantica"
opere_dir = r"D:\repos\Nativus\TeX\Opere"
trilogie_dir = r"D:\repos\Nativus\TeX\Trilogie"
tex_dir = r"D:\repos\Nativus\TeX"

# 1. Update preamble.tex
preamble_path = os.path.join(tex_dir, 'preamble.tex')
with open(preamble_path, 'w', encoding='utf-8') as f:
    f.write("\\usepackage[utf8]{inputenc}\n")
    f.write("\\usepackage{multicol}\n")
    f.write("\\usepackage{verse}\n")
    f.write("\\usepackage[left=1.5cm, right=1.5cm, top=2cm, bottom=2cm]{geometry}\n")
    f.write("\\setlength{\\columnsep}{1cm}\n")
    f.write("\\usepackage{newunicodechar}\n")
    f.write("\\newunicodechar{♭}{$\\flat$}\n")
    # removed standalone as it's causing issues with \input

# 2. Fix Cantica (Remove preamble and document env)
for file in os.listdir(cantica_dir):
    if not file.endswith('.tex'): continue
    filepath = os.path.join(cantica_dir, file)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace("\\input{../preamble.tex}\n", "")
    content = content.replace("\\begin{document}\n\n", "")
    content = content.replace("\\begin{document}\n", "")
    content = content.replace("\n\\end{document}\n", "")
    content = content.replace("\\end{document}", "")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# 3. Fix Opere (Add documentclass)
for file in os.listdir(opere_dir):
    if not file.endswith('.tex'): continue
    filepath = os.path.join(opere_dir, file)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if "\\documentclass" not in content:
        content = content.replace("\\input{../preamble.tex}\n", "\\documentclass{book}\n\\input{../preamble.tex}\n")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# 4. Fix Trilogie
if os.path.exists(trilogie_dir):
    for file in os.listdir(trilogie_dir):
        if not file.endswith('.tex'): continue
        filepath = os.path.join(trilogie_dir, file)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        if "\\documentclass" not in content:
            content = content.replace("\\input{preamble.tex}\n", "\\documentclass{book}\n\\input{../preamble.tex}\n")
            content = content.replace("\\input{../preamble.tex}\n", "\\documentclass{book}\n\\input{../preamble.tex}\n")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

# 5. Fix Saga Nativus
saga_path = os.path.join(tex_dir, 'Saga Nativus.tex')
if os.path.exists(saga_path):
    with open(saga_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if "\\documentclass" not in content:
        content = content.replace("\\input{preamble.tex}\n", "\\documentclass{book}\n\\input{preamble.tex}\n")
    with open(saga_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Structure fixed.")
