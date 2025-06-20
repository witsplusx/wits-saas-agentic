
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

from llama_index.core.agent.workflow import ReActAgent
from llama_index.core.workflow import Context

from llama_index.core.agent.workflow import AgentStream, ToolCallResult
import asyncio

Settings.embed_model = OllamaEmbedding(
    model_name="dengcao/Qwen3-Embedding-0.6B:F16",
    # model_name="dengcao/Qwen3-Embedding-4B:Q8_0",
    base_url="http://localhost:11434",
    ollama_additional_kwargs={"mirostat": 0},
)
Settings.llm = Ollama(
    model="qwen3:8b",
    request_timeout=360.0,
    # Manually set the context window to limit memory usage
    context_window=8000,
    thinking=False
)

from llama_index.core import StorageContext, load_index_from_storage


# 加载向量库
try:
    storage_context = StorageContext.from_defaults(
        persist_dir="./cpnt-check/llamaindex/sty04_rag/storage/lyft"
    )
    lyft_index = load_index_from_storage(storage_context)

    storage_context = StorageContext.from_defaults(
        persist_dir="./cpnt-check/llamaindex/sty04_rag/storage/uber"
    )
    uber_index = load_index_from_storage(storage_context)
    index_loaded = True
except:
    index_loaded = False

# 加载数据
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex

if not index_loaded:
    # load data
    lyft_docs = SimpleDirectoryReader(
        input_files=["./cpnt-check/llamaindex/sty04_rag/data/lyft_2021.pdf"]
    ).load_data()
    uber_docs = SimpleDirectoryReader(
        input_files=["./cpnt-check/llamaindex/sty04_rag/data/uber_2021.pdf"]
    ).load_data()

    # build index
    lyft_index = VectorStoreIndex.from_documents(lyft_docs)
    uber_index = VectorStoreIndex.from_documents(uber_docs)

    # persist index
    lyft_index.storage_context.persist(persist_dir="./cpnt-check/llamaindex/sty04_rag/storage/lyft")
    uber_index.storage_context.persist(persist_dir="./cpnt-check/llamaindex/sty04_rag/storage/uber")


lyft_engine = lyft_index.as_query_engine(similarity_top_k=3)
uber_engine = uber_index.as_query_engine(similarity_top_k=3)

from llama_index.core.tools import QueryEngineTool

query_engine_tools = [
    QueryEngineTool.from_defaults(
        query_engine=lyft_engine,
        name="lyft_10k",
        description=(
            "Provides information about Lyft financials for year 2021. "
            "Use a detailed plain text question as input to the tool."
        ),
    ),
    QueryEngineTool.from_defaults(
        query_engine=uber_engine,
        name="uber_10k",
        description=(
            "Provides information about Uber financials for year 2021. "
            "Use a detailed plain text question as input to the tool."
        ),
    ),
]

from llama_index.core.agent.workflow import ReActAgent
from llama_index.core.workflow import Context

agent = ReActAgent(
    tools=query_engine_tools,
    llm=Ollama(
        model="qwen3:8b",
        request_timeout=360.0,
        # Manually set the context window to limit memory usage
        context_window=8000,
        thinking=False
    ),
    # system_prompt="..."
)

# context to hold this session/state
ctx = Context(agent)


from llama_index.core.agent.workflow import ToolCallResult, AgentStream


# Now we can ask questions about the documents or do calculations
async def main():
    handler = agent.run("What was Lyft's revenue growth in 2021?", ctx=ctx)

    async for ev in handler.stream_events():
        # if isinstance(ev, ToolCallResult):
        #     print(f"\nCall {ev.tool_name} with {ev.tool_kwargs}\nReturned: {ev.tool_output}")
        if isinstance(ev, AgentStream):
            print(f"{ev.delta}", end="", flush=True)

    await handler

    
    # handler = agent.run(
    #     "Compare and contrast the revenue growth of Uber and Lyft in 2021, then give an analysis",
    #     ctx=ctx,
    # )

    # async for ev in handler.stream_events():
    #     # if isinstance(ev, ToolCallResult):
    #     #     print(f"\nCall {ev.tool_name} with {ev.tool_kwargs}\nReturned: {ev.tool_output}")
    #     if isinstance(ev, AgentStream):
    #         print(f"{ev.delta}", end="", flush=True)

    # await handler

# Run the agent
if __name__ == "__main__":
    asyncio.run(main())

