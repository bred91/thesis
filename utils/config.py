# Model & Embeddings
MODEL_NAME = "llama3.1:8b-instruct-q8_0"
EMBEDDING_MODEL = "nomic-embed-text"
SEED = 42
NUM_CTX = 32768

# ChromaDB
CHROMA_METADATA = {"hnsw:space": "cosine"}
CHROMA_PERSIST_DIR = "./chromadb_v1"
COMMITS_COLLECTION_NAME = "commits"
GENERAL_DOCS_COLLECTION_NAME = "general_docs"

# SQLite
SQL_PERSIST_DIR = "db_sqllite/sqlite.db"

# MuJS
MUJS_REMOTE_URL = 'https://github.com/ccxvii/mujs.git'
MUJS_LOCAL_PATH = './mujs'

# Ollama
OLLAMA_CLIENT_HOST = 'http://localhost:11434'
