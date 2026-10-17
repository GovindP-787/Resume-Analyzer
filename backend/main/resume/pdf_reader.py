import pymupdf
def text_extracter(file_path: str) -> str:
    text = ""
    with pymupdf.open(file_path) as pdf:
        for page in pdf:
            text += page.get_text()
    return text