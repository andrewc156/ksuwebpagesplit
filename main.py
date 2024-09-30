import pdfplumber
import time

from PyPDF2 import PdfReader, PdfWriter

start_time = time.time()


pdf_path = "KSU Catalog 2024-2025 (1).pdf"

formatted_sections = {}

with pdfplumber.open(pdf_path) as pdf:
    for page_num in range(len(pdf.pages)):
        page = pdf.pages[page_num]
        words = page.extract_words(extra_attrs=["size", "fontname"])
        lines = {}
        for word in words:
            font_size = word.get("size", 0)
            if font_size >= 15:
                top_position = round(word['top'], 1)
                lines.setdefault(top_position, []).append(word)
        sorted_line_positions = sorted(lines.keys())
        page_text = ''
        for top in sorted_line_positions:
            line_words = lines[top]
            line_words.sort(key=lambda w: w['x0'])
            line_text = ' '.join(word['text'] for word in line_words)
            page_text += line_text.strip() + ' '
        if page_text:
            formatted_sections[page_num + 1] = page_text.strip()

print(formatted_sections)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Done in {elapsed_time} seconds!")




keys = []
titles = []
def split_pdf(input_pdf_path, output_dir):
    pdf_reader = PdfReader(input_pdf_path)
    total_pages = len(pdf_reader.pages)
    counter = 0


    for key in formatted_sections:
        keys.append(key)
        titles.append(formatted_sections[key])
    for i in range(0,len(keys)-1):
        pdf_writer = PdfWriter()
        for j in range(keys[i]-1,keys[i+1]-1):
            pdf_writer.add_page(pdf_reader.pages[j])

        output_pdf_path = f"{output_dir}/{titles[i].replace("/", "")}.pdf"
        with open(output_pdf_path, 'wb') as output_pdf_file:
            pdf_writer.write(output_pdf_file)
        print(f"Saved: {output_pdf_path}")
    pdf_writer = PdfWriter()
    for j in range(keys[-1], len(pdf.pages)):
        pdf_writer.add_page(pdf_reader.pages[j])

    output_pdf_path = f"{output_dir}/{titles[-1].replace("/", "")}.pdf"
    with open(output_pdf_path, 'wb') as output_pdf_file:
        pdf_writer.write(output_pdf_file)
    print(f"Saved: {output_pdf_path}")

input_pdf_path = 'KSU Catalog 2024-2025 (1).pdf'
output_dir = 'output'
pages_per_split = 2

split_pdf(input_pdf_path, output_dir)
print(keys)