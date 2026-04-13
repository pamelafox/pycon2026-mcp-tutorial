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

API_HOST = os.getenv("API_HOST", "azure")

if API_HOST == "azure":
    openai_client = AsyncOpenAI(
        base_url=os.environ["AZURE_OPENAI_ENDPOINT"] + "/openai/v1",
        api_key=os.environ["AZURE_OPENAI_KEY"],
    )
    model = OpenAIChatModel(
        os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"],
        provider=OpenAIProvider(openai_client=openai_client),
    )
elif API_HOST == "ollama":
    openai_client = AsyncOpenAI(
        base_url=os.environ.get("OLLAMA_ENDPOINT", "http://localhost:11434/v1"),
        api_key="no-key-needed",
    )
    model = OpenAIChatModel(
        os.environ.get("OLLAMA_MODEL", "gemma4:e4b"),
        provider=OpenAIProvider(openai_client=openai_client),
    )
elif API_HOST == "openai":
    openai_client = AsyncOpenAI(
        api_key=os.environ["OPENAI_API_KEY"],
        base_url=os.getenv("OPENAI_BASE_URL"),
    )
    model = OpenAIChatModel(
        os.getenv("OPENAI_MODEL", "gpt-5.4"),
        provider=OpenAIProvider(openai_client=openai_client),
    )
else:
    raise ValueError(f"Unsupported API_HOST '{API_HOST}'. Use one of: azure, ollama, openai.")

server = MCPServerStreamableHTTP(url="https://learn.microsoft.com/api/mcp")

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
