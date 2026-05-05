import os
import re

canti_dir = r"D:\repos\Nativus\TeX\Canti"

def strip_latex_from_canti():
    count = 0
    for root, dirs, files in os.walk(canti_dir):
        for file in files:
            if file.endswith('.tex'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Strip specific latex commands
                content = content.replace("\\begin{minipage}{\\columnwidth}\n", "")
                content = content.replace("\\begin{verse}\n", "")
                content = content.replace("\\end{verse}\n", "")
                content = content.replace("\\end{minipage}\n", "")
                content = content.replace("\\vspace{1em}\n", "")
                # remove linebreaks \\
                content = re.sub(r'\\\\(?=\n)', '', content)
                
                # reduce multiple empty lines to a single empty line
                content = re.sub(r'\n{3,}', '\n\n', content)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content.strip() + "\n")
                count += 1
    print(f"Stripped LaTeX from {count} Canto files.")

if __name__ == "__main__":
    strip_latex_from_canti()
