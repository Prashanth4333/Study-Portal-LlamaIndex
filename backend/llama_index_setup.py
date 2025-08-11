import os
from dotenv import load_dotenv
from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
    Settings,
    SimpleDirectoryReader
)
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.readers.file import PyMuPDFReader


# Load environment variables

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")


# Project Paths & Constants

DATA_DIR = "data"
STORAGE_DIR = "storage"
FILE_TRACKER = "file_tracker.txt"
MAX_FILE_SIZE_MB = 15


#  Configure Gemini (with big timeouts)

Settings.llm = Gemini(
    api_key=google_api_key,
    model="models/gemini-1.5-flash",
    request_timeout=300
)
Settings.embed_model = GeminiEmbedding(
    model_name="models/embedding-001",
    api_key=google_api_key,
    request_timeout=300
)

# Parser for chunking documents
parser = SimpleNodeParser.from_defaults(chunk_size=1024, chunk_overlap=100)


#  Utility Functions

def get_file_snapshot():
    """Snapshot of files with last modified timestamps."""
    file_snapshot = []
    for root, _, files in os.walk(DATA_DIR):
        for file in files:
            path = os.path.join(root, file)
            file_snapshot.append(f"{path}|{os.path.getmtime(path)}")
    return sorted(file_snapshot)

def has_files_changed():
    """Check if data folder content changed since last index build."""
    current_snapshot = get_file_snapshot()
    if not os.path.exists(FILE_TRACKER):
        return True
    with open(FILE_TRACKER, "r") as f:
        old_snapshot = f.read().splitlines()
    return current_snapshot != old_snapshot

def save_file_snapshot():
    """Save snapshot to detect future changes."""
    with open(FILE_TRACKER, "w") as f:
        f.write("\n".join(get_file_snapshot()))

def read_single_file(file_path):
    """
    Reads a single file with the appropriate parser.
    Returns a list of Document objects (or empty list).
    """
    try:
        # Skip large files
        if os.path.getsize(file_path) > MAX_FILE_SIZE_MB * 1024 * 1024:
            print(f" Skipping large file (> {MAX_FILE_SIZE_MB} MB): {file_path}")
            return []

        if file_path.lower().endswith(".pdf"):
            try:
                pdf_reader = PyMuPDFReader()
                docs = pdf_reader.load(file_path)
                if docs:
                    print(f" Loaded PDF: {file_path}")
                    return docs
                else:
                    print(f" Empty PDF: {file_path}")
                    return []
            except Exception as e:
                print(f" Failed to read PDF {file_path}: {e}")
                return []

        # For text and other supported formats
        docs = SimpleDirectoryReader(input_files=[file_path]).load_data()
        if docs and any(doc.text.strip() for doc in docs):
            print(f" Loaded text file: {file_path}")
            return docs
        else:
            print(f" Empty/non-text file: {file_path}")
            return []

    except Exception as e:
        print(f" Error reading file {file_path}: {e}")
        return []


#  Index Loader/Builder

def load_or_create_index():
    """Load index from storage or rebuild if files changed."""
    if os.path.exists(STORAGE_DIR) and os.listdir(STORAGE_DIR) and not has_files_changed():
        print(" Loading existing index...")
        storage_context = StorageContext.from_defaults(persist_dir=STORAGE_DIR)
        return load_index_from_storage(storage_context)

    print(" Changes detected. Rebuilding index...")
    all_docs = []

    for root, _, files in os.walk(DATA_DIR):
        if not files:
            print(f" Skipping empty folder: {root}")
            continue

        for file in files:
            file_path = os.path.join(root, file)
            file_docs = read_single_file(file_path)
            if file_docs:
                chunks = parser.get_nodes_from_documents(file_docs)
                all_docs.extend(chunks)

    if not all_docs:
        raise ValueError(" No valid documents found to index.")

    print(f" Total chunks to embed: {len(all_docs)}")
    index = VectorStoreIndex.from_documents(all_docs)
    index.storage_context.persist(persist_dir=STORAGE_DIR)
    save_file_snapshot()
    print(" Index built successfully.")
    return index


#  Query Function

def query_index(query_text):
    
    index = load_or_create_index()
    query_engine = index.as_query_engine()
    response = query_engine.query(query_text)
    return response.response
