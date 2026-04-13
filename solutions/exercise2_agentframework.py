import asyncio
import os

from agent_framework import Agent, MCPStreamableHTTPTool
from agent_framework.openai import OpenAIResponsesClient
from dotenv import load_dotenv

load_dotenv(override=True)

API_HOST = os.getenv("API_HOST", "azure")

if API_HOST == "azure":
    client = OpenAIResponsesClient(
        base_url=f"{os.environ['AZURE_OPENAI_ENDPOINT']}/openai/v1/",
        api_key=os.environ["AZURE_OPENAI_KEY"],
        model_id=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"],
    )
elif API_HOST == "ollama":
    client = OpenAIResponsesClient(
        base_url=os.environ.get("OLLAMA_ENDPOINT", "http://localhost:11434/v1"),
        api_key=os.getenv("OLLAMA_API_KEY", "no-key-needed"),
        model_id=os.environ.get("OLLAMA_MODEL", "gemma4:e4b"),
    )
elif API_HOST == "openai":
    client = OpenAIResponsesClient(
        api_key=os.environ["OPENAI_API_KEY"],
        base_url=os.getenv("OPENAI_BASE_URL"),
        model_id=os.getenv("OPENAI_MODEL", "gpt-5.4"),
    )
else:
    raise ValueError(f"Unsupported API_HOST '{API_HOST}'. Use one of: azure, ollama, openai.")


async def main():
    async with (
        MCPStreamableHTTPTool(
            name="Microsoft Learn MCP",
            url="https://learn.microsoft.com/api/mcp",
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
