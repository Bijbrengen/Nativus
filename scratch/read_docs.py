import pandas as pd
import docx
import sys
import os

def read_excel(f):
    f.write("=== Indice.xlsx ===\n")
    try:
        excel_path = "D:/repos/Nativus/Google drive/Administratie/Indice.xlsx"
        df = pd.read_excel(excel_path, sheet_name=None)
        for sheet_name, sheet_data in df.items():
            f.write(f"Sheet: {sheet_name}\n")
            f.write(sheet_data.to_string() + "\n")
    except Exception as e:
        f.write(f"Error reading Excel: {e}\n")

def read_word(filename, f):
    f.write(f"=== {os.path.basename(filename)} ===\n")
    try:
        doc = docx.Document(filename)
        for i, para in enumerate(doc.paragraphs):
            if para.text.strip():
                style = para.style.name if para.style else 'Normal'
                f.write(f"[{style}] {para.text}\n")
    except Exception as e:
        f.write(f"Error reading Word: {e}\n")

if __name__ == "__main__":
    with open("D:/repos/Nativus/scratch/docs_output_utf8.txt", "w", encoding="utf-8") as f:
        read_excel(f)
        read_word("D:/repos/Nativus/Google drive/Administratie/Verhaalbijbel.docx", f)
