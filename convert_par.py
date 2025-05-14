import os
import io
from concurrent.futures import ThreadPoolExecutor, as_completed
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from pypdf import PdfReader, PdfWriter
import time


TEMP_DIR = "temp_pages"
os.makedirs(TEMP_DIR, exist_ok=True)

def convert_svg_to_pdf(svg_index):
    svg_path = f"downloaded/{svg_index}.svg"
    output_path = os.path.join(TEMP_DIR, f"{svg_index}.pdf")

    try:
        drawing = svg2rlg(svg_path)
        width, height = drawing.width, drawing.height

        with open(output_path, "wb") as f:
            buffer = io.BytesIO()
            c = canvas.Canvas(buffer, pagesize=(width, height))
            renderPDF.draw(drawing, c, 0, 0)
            c.save()
            f.write(buffer.getvalue())

        return output_path
    except Exception as e:
        print(f"Error processing {svg_path}: {e}")
        return None

def convert_to_pdf_parallel(last_page_number, output_filename):
    os.makedirs(TEMP_DIR, exist_ok=True)
    ts = time.time()

    writer = PdfWriter()

    print("Starting parallel rendering of SVGs...")

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(convert_svg_to_pdf, i) for i in range(1, last_page_number + 1)]
        pdf_paths = []

        for future in as_completed(futures):
            result = future.result()
            if result:
                pdf_paths.append(result)

    # Sort to ensure correct order
    pdf_paths.sort(key=lambda x: int(os.path.basename(x).split('.')[0]))

    print("Merging PDF pages...")

    for path in pdf_paths:
        reader = PdfReader(path)
        writer.add_page(reader.pages[0])

    with open(output_filename, "wb") as f:
        writer.write(f)

    print(f"Saved final PDF to {output_filename}")

    # Optional cleanup
    for path in pdf_paths:
        os.remove(path)

    os.rmdir(TEMP_DIR)
    print("Completed in {:.2f} seconds".format(time.time() - ts))


#convert_to_pdf_parallel(200, "output_par.pdf")


