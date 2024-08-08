import fitz  # PyMuPDF
from PIL import Image, ImageFile
import PIL
import pytesseract
import io

ImageFile.LOAD_TRUNCATED_IMAGES = True
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""  # Initialize a variable to store text from both PDF and images
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        
        # Extract text from the PDF page
        text += page.get_text()

        print(text)
        
        # Extract images from the PDF page
        image_list = page.get_images(full=True)
        for image_index, img in enumerate(page.get_images(full=True)):
            # get the XREF of the image
            xref = img[0]
            # extract the image bytes
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            
            try:
                # Load the image with PIL
                image = Image.open(io.BytesIO(image_bytes))
                
                # Apply OCR to the image
                image_text = pytesseract.image_to_string(image, lang='hun')
                
                # Append the OCR'd text to the main text
                text += '\n' + image_text
            except PIL.UnidentifiedImageError:
                pass
    
    return text

def save_text_to_file(text, output_path):
    with open(output_path, 'w') as f:
        f.write(text)


if __name__ == "__main__":
    # Example usage
    pdf_path = 'tak\\01-mako-telepueleskepi-arculati-kezikoenyv-2018.pdf'
    output_text_path = 'output_text.txt'

    extracted_text = extract_text_from_pdf(pdf_path)
    save_text_to_file(extracted_text, output_text_path)
