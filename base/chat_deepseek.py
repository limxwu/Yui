from typing import List

from langchain_deepseek import ChatDeepSeek
import getpass
import os
from base import constants
from langchain_core.messages import BaseMessage
from langchain.messages import SystemMessage,HumanMessage,AIMessage

if not os.getenv("DEEPSEEK_API_KEY"):
    os.environ["DEEPSEEK_API_KEY"] = getpass.getpass(prompt="Enter your DeepSeek API key: ")

model = ChatDeepSeek(
    model="deepseek-chat"
)


def chat1():
    system_msg=SystemMessage(content=constants.ROLE_SYSTEM_DEFINE)
    human_msg1=HumanMessage(content="Yui，我是uu，请称呼我讲个爆笑的笑话，哈哈")
    messages:List[BaseMessage] = [
        system_msg,
        human_msg1,
    ]
    ai_msg1 = model.invoke(messages)
    print(ai_msg1.content)
    messages.append(ai_msg1)
    messages.append(HumanMessage(content="谢谢"))
    ai_msg2 = model.invoke(messages)
    print(ai_msg2.content)
