from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_resume(document):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=60
    )
    chunks = splitter.split_documents([document])
    return chunks