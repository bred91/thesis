# Model & Embeddings
ONLINE_MODEL_NAME = "qwen3:8b"#"deepseek-r1:8b" #"llama3.1:8b-instruct-q8_0"
OFFLINE_MODEL_NAME = "llama3.1:8b-instruct-q8_0"  # For offline use
EMBEDDING_MODEL = "nomic-embed-text"
SEED = 42
NUM_CTX = 32768

# ChromaDB
CHROMA_METADATA = {"hnsw:space": "cosine"}
CHROMA_PERSIST_DIR = "./chromadb_v1"
COMMITS_COLLECTION_NAME = "commits"
GENERAL_DOCS_COLLECTION_NAME = "general_docs"
SEMANTIC_CODE_COLLECTION = "mujs_code_main"

# SQLite
SQL_PERSIST_DIR = "db_sqllite/sqlite.db"

# MuJS
MUJS_REMOTE_URL = 'https://github.com/ccxvii/mujs.git'
MUJS_LOCAL_PATH = './mujs'
MUJS_DOCS_LOCAL_PATH = './mujs/docs'
MUJS_BRANCH = "master"

# Ollama
OLLAMA_CLIENT_HOST = 'http://localhost:11434'

# Offline pipeline parameters
OFFLINE_PIPELINE_TEST_NAME = "final_exp_8"
NEW_EXAMPLES = True
