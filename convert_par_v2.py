import os
import io
import multiprocessing
import time
from pathlib import Path
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from pypdf import PdfReader, PdfWriter

TEMP_DIR = Path("temp_pages")
TEMP_DIR.mkdir(exist_ok=True)



def convert_svg_to_pdf(svg_index):
    svg_path = f"downloaded/{svg_index}.svg"
    output_path = TEMP_DIR / f"{svg_index}.pdf"

    try:
        drawing = svg2rlg(svg_path)
        width, height = drawing.width, drawing.height

        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=(width, height))
        renderPDF.draw(drawing, c, 0, 0)
        c.save()

        with open(output_path, "wb") as f:
            f.write(buffer.getvalue())

        return svg_index, str(output_path)
    except Exception as e:
        print(f"[ERROR] Page {svg_index}: {e}")
        return svg_index, None

def convert_to_pdf_parallel(last_page_number, output_filename):
    TEMP_DIR.mkdir(exist_ok=True)
    ts = time.time()

    writer = PdfWriter()
    svg_indices = list(range(1, last_page_number + 1))

    print(f"Processing {last_page_number} SVGs in parallel...")

    with multiprocessing.Pool() as pool:
        results = pool.map(convert_svg_to_pdf, svg_indices)

    # Sort results by index to preserve correct page order
    for idx, path in sorted(results):
        if path is None:
            continue
        reader = PdfReader(path)
        writer.add_page(reader.pages[0])

    with open(output_filename, "wb") as f:
        writer.write(f)

    print(f"✅ Final PDF saved to: {output_filename}")

    # Optional: Cleanup
    for _, path in results:
        if path:
            os.remove(path)
    TEMP_DIR.rmdir()
    print("Completed in {:.2f} seconds".format(time.time() - ts))

#convert_to_pdf_parallel(200, "out_parv2.pdf")

