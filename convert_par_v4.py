import io
import multiprocessing
import time

from pypdf import PdfReader, PdfWriter
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from svglib.svglib import svg2rlg


def svg_to_pdf_bytes(svg_index):
    svg_path = f"downloaded/{svg_index}.svg"

    try:
        drawing = svg2rlg(svg_path)
        width, height = drawing.width, drawing.height

        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=(width, height))
        renderPDF.draw(drawing, c, 0, 0)
        c.save()


        return svg_index, buffer.getvalue()
    except Exception as e:
        print(f"[ERROR] Page {svg_index}: {e}")
        return svg_index, None

def convert_to_pdf(last_page_number, output_filename, processes=None):
    ts = time.time()
    """
    Parallel SVG→PDF conversion and in-memory merge.
    - last_page_number: number of SVGs to process (assumes 1.svg through n.svg)
    - output_filename: path to write final PDF
    - processes: number of worker processes (defaults to cpu_count())
    """
    writer = PdfWriter()
    indices = list(range(1, last_page_number + 1))
    print(f"Processing {last_page_number} SVGs in parallel...")

    # 1) Parallel conversion to PDF bytes
    with multiprocessing.Pool(processes=processes) as pool:
        results = pool.map(svg_to_pdf_bytes, indices)

    # 2) Sort and merge
    for idx, pdf_bytes in sorted(results, key=lambda x: x[0]):
        if pdf_bytes is None:
            continue
        reader = PdfReader(io.BytesIO(pdf_bytes))
        writer.add_page(reader.pages[0])

    # 3) Write out final PDF
    with open(output_filename, "wb") as out_f:
        writer.write(out_f)

    print(f"✅ Finished: {output_filename}")
    print("Completed in {:.2f} seconds".format(time.time() - ts))

#convert_to_pdf(200, "out_parv4.pdf")

