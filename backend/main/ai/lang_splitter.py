from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_resume(document):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=5,
        chunk_overlap=2
    )
    chunks = splitter.split_documents([document])
    return chunks