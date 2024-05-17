import fitz


def read_pdf(file_path: str) -> str:
    with fitz.open(file_path) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text
