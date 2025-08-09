from fpdf import FPDF
def export_to_pdf(text):
    # Create a PDF object
    pdf = FPDF()
    pdf.add_page()  # Add a page

    # Set font: 'Courier' font with size 12
    pdf.set_font("Courier", size=12)

    # Add text line-by-line
    for line in text.split('\n'):
        pdf.cell(200, 10, txt=line, ln=True)

    # Output the PDF to a file
    pdf.output("tortoise_output.pdf")

def export_text(text, filename="tortoise_output.txt"):
    """Export the text buffer to a plain text file."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)


