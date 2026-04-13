import asyncio
import os
from datetime import datetime

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

load_dotenv(override=True)

API_HOST = os.getenv("API_HOST", "azure")

if API_HOST == "azure":
    model = ChatOpenAI(
        model=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"],
        base_url=os.environ["AZURE_OPENAI_ENDPOINT"] + "/openai/v1/",
        api_key=SecretStr(os.environ["AZURE_OPENAI_KEY"]),
        use_responses_api=True,
    )
elif API_HOST == "ollama":
    model = ChatOpenAI(
        model=os.environ.get("OLLAMA_MODEL", "gemma4:e4b"),
        base_url=os.environ.get("OLLAMA_ENDPOINT", "http://localhost:11434/v1"),
        api_key=SecretStr(os.getenv("OLLAMA_API_KEY", "no-key-needed")),
        use_responses_api=True,
    )
elif API_HOST == "openai":
    model = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-5.4"),
        base_url=os.getenv("OPENAI_BASE_URL"),
        use_responses_api=True,
    )
else:
    raise ValueError(f"Unsupported API_HOST '{API_HOST}'. Use one of: azure, ollama, openai.")


async def run_agent():
    client = MultiServerMCPClient(
        {
            "microsoft-learn": {
                "url": "https://learn.microsoft.com/api/mcp",
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
