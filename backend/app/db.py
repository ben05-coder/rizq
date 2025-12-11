from chromadb import Client
from chromadb.config import Settings
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

# 1. Create persistent client (NEW API)
client = Client(
    Settings(
        anonymized_telemetry=False,
        persist_directory="chroma_data"
    )
)

# 2. Embedding model
embedding_fn = SentenceTransformerEmbeddingFunction(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 3. Create or load collection
collection = client.get_or_create_collection(
    name="notes",
    embedding_function=embedding_fn
)
