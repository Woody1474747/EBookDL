import os
import io
import time

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from pypdf import PdfWriter, PdfReader


def convert_to_pdf(last_page_number, output_filename):
    ts = time.time()
    # List of SVG files
    svg_files = ["1.svg", "2.svg", "3.svg"]  # Replace with your files

    writer = PdfWriter()

    c = canvas.Canvas(output_filename)
    for i in range(1, last_page_number+1):
        drawing = svg2rlg("downloaded/{}.svg".format(i))

        # Get dynamic width and height of the SVG
        width, height = drawing.width, drawing.height

        # Render SVG to in-memory PDF with matching size
        renderPDF.draw(drawing, c, 0, 0)
        c.showPage()

        # Read the single-page PDF and add it to final output

        print("Added page {}".format(i))

    c.save()


    print(f"Saved combined PDF to {output_filename}")
    print("Completed in {:.2f} seconds".format(time.time() - ts))

