# Exercise 2: Code a Python Agent with MCP Tools

In this exercise, you'll write a Python script that creates an AI agent and connects it to an MCP server. The agent will use the MCP server's tools to answer questions — just like the coding agents from Exercise 1, but now you're building the agent yourself.

- [Step 1: Set up an LLM connection](#step-1-set-up-an-llm-connection)
- [Step 2: Build an agent with MCP tools](#step-2-build-an-agent-with-mcp-tools)
  - [Option A: Microsoft Agent Framework](#option-a-microsoft-agent-framework)
  - [Option B: LangChain v1](#option-b-langchain-v1)
  - [Option C: Pydantic AI](#option-c-pydantic-ai)
- [Try it out](#try-it-out)
- [Full reference examples](#full-reference-examples)

---

## Step 1: Set up an LLM connection

Your agent needs access to an LLM that supports **tool calling**. Pick **one** of the providers below and create a `.env` file in the repo root with the required variables.

### Option 1: Ollama (local, no account needed)

Run a local LLM on your machine using [Ollama](https://ollama.com/). No API key required.

1. [Install Ollama](https://ollama.com/download) if you don't have it.
2. Pull a model that supports tool calling:

   ```bash
   ollama pull gemma4:e4b
   ```

3. Add to your `.env`:

   ```text
   API_HOST=ollama
   OLLAMA_MODEL=gemma4:e4b
   ```

    If you're using the repository Dev Container, also add:

    ```text
    OLLAMA_ENDPOINT=http://host.docker.internal:11434/v1
    ```

> **Note:** Ollama runs entirely on your machine. A model like `gemma4:e4b` needs ~32 GB of RAM. If your machine has has less RAM, try `llama3.1:8b` instead.

### Option 2: OpenRouter

[OpenRouter](https://openrouter.ai/) gives you access to many models through a single API key, including free-tier models.

1. Sign up at [openrouter.ai](https://openrouter.ai/) and get an API key.
2. Add to your `.env`:

   ```text
   API_HOST=openai
   OPENAI_API_KEY=<your OpenRouter API key>
   OPENAI_BASE_URL=https://openrouter.ai/api/v1
   OPENAI_MODEL=google/gemma-3-27b-it
   ```

> **Tip:** OpenRouter uses the OpenAI-compatible API, so we set `API_HOST=openai` and override the base URL.

### Option 3: OpenAI

Use the [OpenAI API](https://platform.openai.com/) directly.

1. Get an API key from [platform.openai.com/api-keys](https://platform.openai.com/api-keys).
2. Add to your `.env`:

   ```text
   API_HOST=openai
   OPENAI_API_KEY=<your OpenAI API key>
   OPENAI_MODEL=gpt-5.4
   ```

### Option 4: Azure OpenAI

<!-- TODO: We may be able to provide shared Azure OpenAI keys for the tutorial. -->

Use [Azure OpenAI Service](https://learn.microsoft.com/azure/ai-services/openai/).

1. You need an Azure OpenAI endpoint and a deployed chat model.
2. Add to your `.env`:

   ```text
   API_HOST=azure
   AZURE_OPENAI_ENDPOINT=<your endpoint>
   AZURE_OPENAI_CHAT_DEPLOYMENT=<your deployment name>
   AZURE_OPENAI_KEY=<your API key>
   ```

### Verify your LLM connection

Run a quick check to make sure your LLM is reachable (we'll use it in Step 2):

```bash
uv run python -c "from dotenv import load_dotenv; load_dotenv(); print('Environment loaded OK')"
```

---

## Step 2: Build an agent with MCP tools

Now pick **one** of the three framework options below. Each gives you a skeleton — your job is to fill in the MCP server connection details.

### Option A: Microsoft Agent Framework

Create `agents/exercise2_agentframework.py` with this skeleton:

```python
import asyncio
import os

from agent_framework import Agent, MCPStreamableHTTPTool
from agent_framework.openai import OpenAIChatClient
from dotenv import load_dotenv

load_dotenv(override=True)

# TODO: Configure the OpenAI client for your chosen provider.
# For OpenAI:
client = OpenAIChatClient(
    api_key=os.environ["OPENAI_API_KEY"],
    model=os.getenv("OPENAI_MODEL", "gpt-5.4"),
)


async def main():
    async with (
        MCPStreamableHTTPTool(
            name="________",  # TODO: Give the MCP server a name
            url="________",  # TODO: Set the MCP server URL
        ) as mcp_server,
        Agent(
            client=client,
            name="DocsAgent",
            instructions="You help answer questions using documentation.",
            tools=[mcp_server],
        ) as agent,
    ):
        result = await agent.run("What are the available hosting options for a Python web app on Azure?")
        print(result.text)


if __name__ == "__main__":
    asyncio.run(main())
```

**What you need to fill in:**

1. The `name` for the MCP tool (e.g. `"Microsoft Learn MCP"`)
2. The `url` for the MCP server (use the Microsoft Learn URL from Exercise 1)

Run it:

```bash
uv run agents/exercise2_agentframework.py
```

---

### Option B: LangChain v1

Create `agents/exercise2_langchain.py` with this skeleton:

```python
import asyncio
import os
from datetime import datetime

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI

load_dotenv(override=True)

# TODO: Configure the ChatOpenAI model for your chosen provider.
# For OpenAI:
model = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "gpt-5.4"),
    use_responses_api=True,
)


async def run_agent():
    client = MultiServerMCPClient(
        {
            "________": {  # TODO: Set a server name
                "url": "________",  # TODO: Set the MCP server URL
                "transport": "streamable_http",
            }
        }
    )

    tools = await client.get_tools()
    agent = create_agent(model, tools)

    today = datetime.now().strftime("%Y-%m-%d")
    response = await agent.ainvoke(
        {
            "messages": [
                SystemMessage(content=f"Today's date is {today}."),
                HumanMessage(content="What are the available hosting options for a Python web app on Azure?"),
            ]
        }
    )

    print(response["messages"][-1].text)


if __name__ == "__main__":
    asyncio.run(run_agent())
```

**What you need to fill in:**

1. The server name key in the `MultiServerMCPClient` dict (e.g. `"microsoft-learn"`)
2. The `url` for the MCP server (use the Microsoft Learn URL from Exercise 1)

Run it:

```bash
uv run agents/exercise2_langchain.py
```

---

### Option C: Pydantic AI

Create `agents/exercise2_pydanticai.py` with this skeleton:

```python
import asyncio
import logging
import os

from dotenv import load_dotenv
from openai import AsyncOpenAI
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

load_dotenv(override=True)

# TODO: Configure the OpenAI client for your chosen provider.
# For OpenAI:
openai_client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
model = OpenAIChatModel(
    os.getenv("OPENAI_MODEL", "gpt-5.4"),
    provider=OpenAIProvider(openai_client=openai_client),
)

server = MCPServerStreamableHTTP(
    url="________",  # TODO: Set the MCP server URL
)

agent: Agent[None, str] = Agent(
    model,
    system_prompt="You help answer questions using documentation.",
    output_type=str,
    toolsets=[server],
)


async def main():
    result = await agent.run("What are the available hosting options for a Python web app on Azure?")
    print(result.output)


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    asyncio.run(main())
```

**What you need to fill in:**

1. The `url` for the MCP server (use the Microsoft Learn URL from Exercise 1)

Run it:

```bash
uv run agents/exercise2_pydanticai.py
```

---

## Try it out

Once your agent works with the Microsoft Learn server, try changing the MCP server URL to connect to a different server, like the Hugging Face MCP server (`https://huggingface.co/mcp`), and ask it a question like "What are the most popular text generation models?"

## Full reference examples

If you get stuck, check out these complete working examples:

- **Agent Framework:** [agentframework_learn.py](https://github.com/Azure-Samples/python-mcp-demos/blob/main/agents/agentframework_learn.py)
- **LangChain v1:** [langchainv1_http.py](https://github.com/Azure-Samples/python-mcp-demos/blob/main/agents/langchainv1_http.py)
- **Pydantic AI:** [pydanticai_mcp_http.py](https://github.com/Azure-Samples/python-ai-agent-frameworks-demos/blob/main/examples/pydanticai_mcp_http.py)
