import pdfplumber


def extract_text(path: str) -> str:
    '''
    Extract all text from the PDF file at the given path, concatenating pages with blank lines.

    Args:
        path (str): The file path to the PDF document.
    Returns:
        str: The concatenated text from all pages of the PDF.
    '''

    all_text = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text(x_tolerance=3, y_tolerance=3) or ""
            all_text.append(text)
    return "\n\n".join(all_text)
