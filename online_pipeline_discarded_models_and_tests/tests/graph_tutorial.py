from typing import Literal

from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode

# VECTOR STORES
chroma = Chroma(
    collection_name="commits",
    embedding_function=OllamaEmbeddings(model="nomic-embed-text"),
    collection_metadata={"hnsw:space": "cosine"},
    persist_directory="./chromadb_v1",
)


# TOOLS
@tool
def retrieve_context(query: str):
    """Tool for searching relevant information about MuJS commits."""
    print("Retrieving documents...")
    retriever = chroma.as_retriever(search_kwargs={"k": 6})
    results = retriever.invoke(query)
    print(f"Retrieved documents...{len(results)}")
    print(results)

    # Include metadata in the document content
    def format_doc(doc):
        meta = doc.metadata
        return (
            f"COMMIT: {meta.get('commit_hash', '')}\n"
            f"INDEX: {meta.get('index', '')}\n"
            f"AUTHOR: {meta.get('author', '')}\n"
            f"DATE: {meta.get('date', '')}\n"
            f"TYPE: {meta.get('type', '')}\n"
            f"MSG : {meta.get('message', '')}\n"
            f"{doc.page_content}"
        )
    return "\n\n".join([format_doc(doc) for doc in results])


tools = [retrieve_context]
tool_node = ToolNode(tools)

# OpenAI LLM model
model = ChatOllama(model="llama3.1:8b-instruct-q8_0", temperature=0.0).bind_tools(tools)


# Function to decide whether to continue or stop the workflow
def should_continue(state: MessagesState) -> Literal["tools", END]:
    messages = state['messages']
    last_message = messages[-1]
    # If the LLM makes a tool call, go to the "tools" node
    if last_message.tool_calls:
        return "tools"
    # Otherwise, finish the workflow
    return END


# Function that invokes the model
def call_model(state: MessagesState):
    messages = state['messages']
    response = model.invoke(messages)
    return {"messages": [response]}  # Returns as a list to add to the state


# Define the workflow with LangGraph
workflow = StateGraph(MessagesState)

# Add nodes to the graph
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

# Connect nodes
workflow.add_edge(START, "agent")  # Initial entry
workflow.add_conditional_edges("agent", should_continue)  # Decision after the "agent" node
workflow.add_edge("tools", "agent")  # Cycle between tools and agent

# Configure memory to persist the state
checkpointer = MemorySaver()

# Compile the graph into a LangChain Runnable application
app = workflow.compile(checkpointer=checkpointer)

system_prompt = SystemMessage(
    content="""
    You are a helpful assistant that answers questions based on the provided context about MuJS Repository.
    If you need information about the commits and/or the code, you can use the `retrieve_context` tool.
    If you do not know the answer, you should say "I don't know".
    """
)

def main():
    """Simple CLI loop to interact with the LangGraph agent."""
    messages = [system_prompt]  # Conversation history preserved across turns
    user_input_s: str = ''

    print('Digita la tua domanda ("/exit" per uscire)')
    while True:
        try:
            user_input_s = input("❯ ").strip()

            if user_input_s.lower() in {"/exit", "exit", "quit"}:
                print("Uscita dal programma.")
                break

            if not user_input_s:
                continue  # Skip empty inputs

        except (KeyboardInterrupt, EOFError):
            print("\nUscita dal programma.")
            break

        # Add the user's question to the message history
        messages.append(HumanMessage(content=user_input_s))

        # Run the workflow
        final_state = app.invoke({"messages": messages}, config={"thread_id": 5})
        assistant_msg = final_state["messages"][-1]

        # Display and store the assistant's reply
        print(assistant_msg.content)
        messages.append(assistant_msg)


if __name__ == "__main__":
    main()