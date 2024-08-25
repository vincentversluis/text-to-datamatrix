# %% HEADER
# 

# %% IMPORTS
import math
import segno
from fpdf import FPDF
import os
import fitz  # PyMuPDF
from pyzbar.pyzbar import decode
from PIL import Image

# %% FUNCTIONS
def text_to_datamatrix_pdf(text, output_pdf_path, datamatrix_size_mm=(30, 30), page_size_mm=(210, 297)):
    # Convert sizes from mm to pixels (at 300 DPI)
    dpi = 300
    datamatrix_size_px = tuple(int(x * dpi / 25.4) for x in datamatrix_size_mm)
    page_size_px = tuple(int(x * dpi / 25.4) for x in page_size_mm)
    
    # Split the text into chunks that fit into a Data Matrix code
    chunks = [text[i:i+100] for i in range(0, len(text), 100)]  # Adjust size as needed
    num_chunks = len(chunks)
    codes_per_row = page_size_px[0] // datamatrix_size_px[0]
    codes_per_col = page_size_px[1] // datamatrix_size_px[1]
    codes_per_page = codes_per_row * codes_per_col
    
    # Calculate the number of pages needed
    total_pages = math.ceil(num_chunks / codes_per_page)
    
    # Create a PDF object
    pdf = FPDF(unit="pt", format=[page_size_px[0], page_size_px[1]])
    
    for page_num in range(total_pages):
        pdf.add_page()
        
        start_chunk = page_num * codes_per_page
        end_chunk = min(start_chunk + codes_per_page, num_chunks)
        
        for idx, chunk in enumerate(chunks[start_chunk:end_chunk]):
            row = idx // codes_per_row
            col = idx % codes_per_row
            x = col * datamatrix_size_px[0]
            y = row * datamatrix_size_px[1]
            
            # Create Data Matrix code using segno
            dm = segno.make(chunk, encoding='utf-8')  # Removed 'micro' and 'version' parameters
            
            # Save Data Matrix code temporarily as an image
            temp_image_path = f"temp_datamatrix_{page_num}_{idx}.png"
            dm.save(temp_image_path, scale=10)  # Adjust scale for appropriate size
            
            # Insert Data Matrix code into PDF
            pdf.image(temp_image_path, x, y, datamatrix_size_px[0], datamatrix_size_px[1])
            
            # Optionally remove the temporary image file to save disk space
            os.remove(temp_image_path)
    
    # Save the PDF
    pdf.output(output_pdf_path)

def extract_images_from_pdf(pdf_path, output_dir):
    """Extracts images from each page of a PDF and saves them as PNG files."""
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    document = fitz.open(pdf_path)
    image_paths = []

    for page_num in range(document.page_count):
        page = document.load_page(page_num)
        pix = page.get_pixmap()
        image_path = f"{output_dir}/page_{page_num}.png"
        pix.save(image_path)
        image_paths.append((page_num, image_path))  # Store page number with image path

    return image_paths

def decode_datamatrix_from_images(image_paths):
    """Decodes Data Matrix (or QR) codes from a list of image paths, maintaining the order."""
    decoded_text = ""
    
    # Sort image paths by page number (and position if needed)
    sorted_image_paths = sorted(image_paths, key=lambda x: x[0])
    
    for page_num, image_path in sorted_image_paths:
        image = Image.open(image_path)
        codes = decode(image)
        
        if not codes:
            print(f"No Data Matrix/QR code found in image: {image_path}")  # Debugging output
        else:
            for code in codes:
                if code.type == "QRCODE":  # Adjust this to match the actual code type
                    decoded_text = code.data.decode("utf-8") + decoded_text
    
    return decoded_text

# Main function to extract text from Data Matrix/QR codes in PDF
def decode_datamatrix_from_pdf(pdf_path, output_txt_path, temp_image_dir='temp_images'):
    # Step 1: Extract images from the PDF
    image_paths = extract_images_from_pdf(pdf_path, temp_image_dir)
    
    # Step 2: Decode Data Matrix/QR codes from extracted images
    decoded_text = decode_datamatrix_from_images(image_paths)
    
    # Write decoded text to the output file
    with open(output_txt_path, 'w') as output_file:
        output_file.write(decoded_text)
    
    print(f"Decoded text saved to {output_txt_path}")



# %% Turn several files into qr pdfs
input_dir = "../data/"
files = [file for file in os.listdir(input_dir) if file.split('.')[-1] in ['txt', 'md', 'py', '.ipynb']]
for file in files:
    input_file = os.path.join(input_dir, file)
    output_file = f"../output/{file.split('.')[0]}.pdf"
    with open(input_file, 'r') as f:
        text = f.read()
    text_to_datamatrix_pdf(text, output_file)
    
# %% Decode 
input_dir = "../data/"
output_type = ".py"
files = [file for file in os.listdir(input_dir) if file.split('.')[-1] in ['pdf']]

for file in files:
    input_file = os.path.join(input_dir, file)
    output_file = f"../output/{file.split('.')[0]}{output_type}"
    decode_datamatrix_from_pdf(input_file, output_file)
    
# %%
