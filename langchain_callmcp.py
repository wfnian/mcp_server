import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek


load_dotenv()

llm = ChatDeepSeek(
    model=os.getenv("DEFAULT_MODEL_NAME"),
    base_url=os.getenv("OPENAI_API_BASE_URL"),
    api_key=os.getenv("OPENAI_API_KEY"),
)


async def main():
    client = MultiServerMCPClient(
        {
            "my-mcp-server-59d4a2c0": {
                "url": "http://localhost:8006/sse",
                "transport": "sse",
            },
        }
    )

    tools = await client.get_tools()
    print(f"\033[92mTools: {tools}\033[0m")
    agent = create_agent(llm, tools)
    math_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what's (3 - 5) x 12?"}]}
    )
    print(f"\033[92mMath Response: {math_response}\033[0m")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
# from langchain.agents import create_agent


# def get_weather(city: str) -> str:
#     """Get weather for a given city."""
#     return f"It's always sunny in {city}!"


# agent = create_agent(
#     model=llm,
#     tools=[get_weather],
#     system_prompt="You are a helpful assistant",
# )

# # Run the agent
# res = agent.invoke(
#     {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
# )
# print(res)
