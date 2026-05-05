import docx
import os

files_to_check = [
    r"D:\repos\Nativus\Google drive\Cantica\Canticum 1_ Emmy's Lichaam.docx",
    r"D:\repos\Nativus\Google drive\Opere\Opera 1_ Emmy.docx"
]

for f in files_to_check:
    print(f"File: {f}")
    if os.path.exists(f):
        doc = docx.Document(f)
        texts = [p.text for p in doc.paragraphs if p.text.strip()]
        print(texts)
    else:
        print("Not found")
