
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

from llama_index.core.agent.workflow import ReActAgent
from llama_index.core.workflow import Context

from llama_index.core.agent.workflow import AgentStream, ToolCallResult
import asyncio

Settings.embed_model = OllamaEmbedding(
    model_name="dengcao/Qwen3-Embedding-0.6B:F16",
    base_url="http://localhost:11434",
    ollama_additional_kwargs={"mirostat": 0},
)

def multiply(a: int, b: int) -> int:
    """Multiply two integers and returns the result integer"""
    return a * b


def add(a: int, b: int) -> int:
    """Add two integers and returns the result integer"""
    return a + b

llm = Ollama(
    model="qwen3:8b",
    request_timeout=360.0,
    # Manually set the context window to limit memory usage
    context_window=8000,
    thinking=False
)

agent = ReActAgent(
    tools=[multiply, add],
    llm=llm,
    system_prompt="You are a helpful assistant that can multiply two numbers.",
)
# Create a context to store the conversation history/session state
ctx = Context(agent)

# prompt_dict = agent.get_prompts()
# for k, v in prompt_dict.items():
#     print(f"Prompt: {k}\n\nValue: {v.template}")




from llama_index.core import PromptTemplate
react_system_header_str = """\

You are designed to help with a variety of tasks, from answering questions \
    to providing summaries to other types of analyses.

## Tools
You have access to a wide variety of tools. You are responsible for using
the tools in any sequence you deem appropriate to complete the task at hand.
This may require breaking the task into subtasks and using different tools
to complete each subtask.

You have access to the following tools:
{tool_desc}

## Output Format
To answer the question, please use the following format.

```
Thought: I need to use a tool to help me answer the question.
Action: tool name (one of {tool_names}) if using a tool.
Action Input: the input to the tool, in a JSON format representing the kwargs (e.g. {{"input": "hello world", "num_beams": 5}})
```

Please ALWAYS start with a Thought.

Please use a valid JSON format for the Action Input. Do NOT do this {{'input': 'hello world', 'num_beams': 5}}.

If this format is used, the user will respond in the following format:

```
Observation: tool response
```

You should keep repeating the above format until you have enough information
to answer the question without using any more tools. At that point, you MUST respond
in the one of the following two formats:

```
Thought: I can answer without using any more tools.
Answer: [your answer here]
```

```
Thought: I cannot answer the question with the provided tools.
Answer: Sorry, I cannot answer your query.
```

## Additional Rules
- The answer MUST contain a sequence of bullet points that explain how you arrived at the answer. This can include aspects of the previous conversation history.
- You MUST obey the function signature of each tool. Do NOT pass in no arguments if the function expects arguments.

## Current Conversation
Below is the current conversation consisting of interleaving human and assistant messages.

"""
react_system_prompt = PromptTemplate(react_system_header_str)

agent.update_prompts({"react_header": react_system_prompt})

from llama_index.core.agent.workflow import AgentStream, ToolCallResult

# Now we can ask questions about the documents or do calculations
async def main():
    # handler = agent.run("What is 20+(2*4)?", ctx=ctx)

    # async for ev in handler.stream_events():
    #     if isinstance(ev, ToolCallResult):
    #         print(f"\nCall {ev.tool_name} with {ev.tool_kwargs}\nReturned: {ev.tool_output}")
    #     if isinstance(ev, AgentStream):
    #         print(f"{ev.delta}", end="", flush=True)

    # await handler

    handler = agent.run("What is 20+(2*4)+100?", ctx=ctx)

    async for ev in handler.stream_events():
        if isinstance(ev, ToolCallResult):
            print(f"\nCall {ev.tool_name} with {ev.tool_kwargs}\nReturned: {ev.tool_output}")
        if isinstance(ev, AgentStream):
            print(f"{ev.delta}", end="", flush=True)

    await handler


# Run the agent
if __name__ == "__main__":
    asyncio.run(main())




