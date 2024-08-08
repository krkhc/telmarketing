import os
from docx_reader import extract_images_and_ocr
from pdf_reader import extract_text_from_pdf

def save_text_to_file(text, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)

for file in os.listdir("tak")[106:]:
    if file.endswith(".pdf"):
        pdf_path = os.path.join("tak", file)
        extracted_text = extract_text_from_pdf(pdf_path)
    elif file.endswith(".docx"):
        docx_path = os.path.join("tak", file)
        extracted_text = extract_images_and_ocr(docx_path)
    else:
        print(file)

    output_text_path = os.path.join("txt_tak", file + ".txt")
    save_text_to_file(extracted_text, output_text_path)



