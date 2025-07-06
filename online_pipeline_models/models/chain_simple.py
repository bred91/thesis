from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import PromptTemplate
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import OllamaEmbeddings
from langchain_ollama.llms import OllamaLLM

from online_pipeline_models.base_chat_pipeline import BaseChatPipeline
from utils.config import NUM_CTX, ONLINE_MODEL_NAME, COMMITS_COLLECTION_NAME, EMBEDDING_MODEL, CHROMA_PERSIST_DIR, \
    CHROMA_METADATA

# -- Vector store & retriever --------------------------------------------------
chroma_simple = Chroma(
    collection_name=COMMITS_COLLECTION_NAME,
    embedding_function=OllamaEmbeddings(model=EMBEDDING_MODEL),
    collection_metadata=CHROMA_METADATA,
    persist_directory=CHROMA_PERSIST_DIR,
)
retriever = chroma_simple.as_retriever()

# -- LLM -----------------------------------------------------------------------
llm = OllamaLLM(model=ONLINE_MODEL_NAME, num_ctx=NUM_CTX, temperature=0.0)

# -- System Prompt ---------------------------------------------------------
SYSTEM = """
You are a helpful assistant that answers questions about the MuJS project based on the provided context.
You will receive a series of documents, each with metadata including a commit hash, date, message, and content.
If you do not know the answer, you should say "I don't know".
<context>
{context}
</context>
"""
main_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM.strip()),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)

# -- Prompt for individual documents ---------------------------------------------
doc_prompt = PromptTemplate(
    input_variables=["page_content", "commit_hash", "index", "author", "date", "message", "type"],
    template=(
        "COMMIT: {commit_hash}\n"
        "INDEX: {index}\n"
        "AUTHOR: {author}\n"
        "DATE: {date}\n"
        "TYPE: {type}\n"
        "MSG : {message}\n"
        "{page_content}"
    ),
)

# -- Create the retrieval chain ---------------------------------------------
combine_docs_chain = create_stuff_documents_chain(
    llm,
    main_prompt,
    document_prompt=doc_prompt,
    document_separator="\n\n",
    document_variable_name="context",
)

rag_chain = create_retrieval_chain(retriever, combine_docs_chain)


# -- ChainSimple Class ---------------------------------------------------------
class ChainSimple(BaseChatPipeline):
    def __init__(self):
        super().__init__()
        self.chain = rag_chain

    def _respond(self, user_message: str) -> str:
        res = self.chain.invoke({"input": user_message, "chat_history": self.chat_history})
        return res["answer"]