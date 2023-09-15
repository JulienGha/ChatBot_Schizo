import json
import PyPDF2
import nbformat
from nbconvert import PythonExporter


def convert_notebook_to_python(notebook_path, python_path):
    # Load Jupyter/IPython notebook file
    with open(notebook_path, encoding='utf-8') as f:
        notebook = nbformat.read(f, as_version=4)

    # Convert to Python script
    python_exporter = PythonExporter()
    python_code, _ = python_exporter.from_notebook_node(notebook)

    # Write to Python script file
    with open(python_path, 'w', encoding='utf-8') as f:
        f.write(python_code)


def convert_pdf_into_json(file):
    # Open the PDF file in input
    pdf = open('datasets/Symptoms/' + file + '.pdf', "rb")

    # Create a PDF reader object
    reader = PyPDF2.PdfFileReader(pdf)

    # Get the number of pages in the PDF file
    num_pages = reader.numPages

    # Create an empty list to store the text from the PDF file
    text = []

    # Iterate over the pages in the PDF file
    for i in range(num_pages):
        # Get the text from the current page
        page = reader.getPage(i)
        text.append(page.extractText())

    # Close the PDF file
    pdf.close()

    # Split the text into lists of strings
    for i in range(num_pages):
        text[i] = text[i].split("\n")

    # Create a JSON object from the list of lists of strings
    json_object = json.dumps(text)

    # Save the JSON object to a file
    with open('datasets/' + file + '.json', 'w') as f:
        f.write(json_object)


convert_notebook_to_python('datasets/13.chat-with-multiple-pdfs-using-llama-2-and-langchain.ipynb', 'YourScript.py')