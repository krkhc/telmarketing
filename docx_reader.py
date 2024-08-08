import os
from docx import Document
from docx.shared import Inches
from PIL import Image
import pytesseract
from io import BytesIO
import tempfile

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


# Function to extract text from the document's paragraphs
def extract_text(doc):
    full_text = [para.text for para in doc.paragraphs]
    return "\n".join(full_text)

# Function to perform OCR on an image file
def ocr_image(image_path):
    return pytesseract.image_to_string(Image.open(image_path), lang='hun')

# Extract and OCR images from a DOCX file
def extract_images_and_ocr(docx_path):
    doc = Document(docx_path)
    text = extract_text(doc)
    images_text = []

    # Temporarily save images and perform OCR
    with tempfile.TemporaryDirectory() as tmpdirname:
        for rel in doc.part.rels.values():
            if "image" in rel.target_ref:
                # Extract the image
                image_blob = rel.target_part.blob
                image_path = os.path.join(tmpdirname, os.path.basename(rel.target_ref))
                with open(image_path, 'wb') as img_file:
                    img_file.write(image_blob)
                
                # Perform OCR on the image
                image_text = ocr_image(image_path)
                print(image_text)
                images_text.append(image_text)
    
    return text + "\n" + "\n".join(images_text)

def save_text_to_file(text, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)


if __name__ == "__main__":
    # Example usage
    docx_path = 'tak\\teleki_tak_20181201.docx'
    output_text_path = 'output_text.txt'

    extracted_text = extract_images_and_ocr(docx_path)
    save_text_to_file(extracted_text, output_text_path)
