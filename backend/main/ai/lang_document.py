from langchain_core.documents import Document

def create_langchain_document(resume_text: str, resume_id: int, file_name: str)-> Document:
    document = Document(page_content=resume_text, metadata = {"resume_id":resume_id, "file_name":file_name})
    return document
