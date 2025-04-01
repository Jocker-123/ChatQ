from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings


def load_docs(file_path: str):
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    else:
        loader = TextLoader(file_path)
    return loader.load()


def ingest_to_vector_db(file_path: str, db_path: str = "faiss_index"):
    docs = load_docs(file_path)
    embeddings = HuggingFaceEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(db_path)
    return f"Indexed {len(docs)} documents."

def search_faiss(query: str, db_path: str = "faiss_index", k: int = 3):
    embeddings = HuggingFaceEmbeddings()
    vectorstore = FAISS.load_local(db_path, embeddings, allow_dangerous_deserialization=True)
    results = vectorstore.similarity_search(query, k=k)
    return [doc.page_content for doc in results]

