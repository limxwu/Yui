from typing import List
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

from core.llm import get_model
from core.constants import YUI_SYSTEM_PROMPT
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage


async def chat():
    """演示对话功能"""
    # 获取模型实例
    llm = get_model()
    client = MultiServerMCPClient(
        {
            "fetch": {
                "transport": "stdio",
                "command": "uvx",
                "args": ["mcp-server-fetch"]
            }
        }
    )
    tools = await client.get_tools()
    system_msg = SystemMessage(content=YUI_SYSTEM_PROMPT)
    human_msg1 = HumanMessage(content="Yui，利用工具查看这个接口的返回并告诉我（无论是什么）：https://apis.juhe.cn/fapigw/air/provinces")
    messages: List[BaseMessage] = [
        system_msg,
        human_msg1,
    ]
    llm.bind_tools(tools)
    ai_msg1 = llm.invoke(messages)
    print(ai_msg1.content)


if __name__ == "__main__":
    asyncio.run(chat())
