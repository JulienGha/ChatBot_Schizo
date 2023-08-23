import json
import PyPDF2


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


convert_pdf_into_json('Hallucinations_visual')
