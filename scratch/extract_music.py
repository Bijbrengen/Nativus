import os
import re

canti_dir = r"D:\repos\Nativus\TeX\Canti"
muziek_dir = r"D:\repos\Nativus\TeX\Muziek"

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

ensure_dir(muziek_dir)

music_keywords = [
    'per ', 'con ', 'in re ', 'in sol ', 'in do ', 'in fa ', 'in si ', 'in mi ', 'in la ',
    'minore', 'majeur', 'maggiore', 'andante', 'allegro', 'allegretto', 'adagio', 
    'largo', 'grave', 'moderato', 'lamentum', 'rapsodia', 'sinfonia', 'cantus',
    'arpa', 'flauto', 'violino'
]

def is_music_style(text):
    text_lower = text.lower()
    # If it's a short paragraph that contains music keywords, it's a music style
    for kw in music_keywords:
        if kw in text_lower:
            return True
    return False

count = 0
for root, dirs, files in os.walk(canti_dir):
    for file in files:
        if file.endswith('.tex'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            if not content:
                continue
                
            paragraphs = content.split('\n\n')
            first_par = paragraphs[0].strip()
            
            # Additional check: verse stanzas usually have 2-3 lines. Music style is usually 1 line.
            # But sometimes the music style might be split.
            if is_music_style(first_par) and len(first_par.split('\n')) <= 2:
                # It is a music style!
                music_style = first_par
                rest_of_canto = '\n\n'.join(paragraphs[1:]).strip()
                
                # Write music style to Muziek/Canto Naam.tex
                canto_name = file  # e.g., 'Canto Angst.tex'
                muziek_path = os.path.join(muziek_dir, canto_name)
                
                with open(muziek_path, 'w', encoding='utf-8') as f_muz:
                    f_muz.write(music_style + "\n")
                    
                # Write the rest back to Canto file
                with open(filepath, 'w', encoding='utf-8') as f_canto:
                    f_canto.write(rest_of_canto + "\n")
                    
                count += 1

print(f"Extracted music style from {count} Canto files.")
