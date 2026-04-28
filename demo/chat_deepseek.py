from typing import List

from core.llm import get_model
from core.constants import YUI_SYSTEM_PROMPT
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage


def chat1():
    """演示对话功能"""
    # 获取模型实例
    model = get_model()
    
    system_msg = SystemMessage(content=YUI_SYSTEM_PROMPT)
    human_msg1 = HumanMessage(content="Yui，我是uu，请称呼我讲个爆笑的笑话，哈哈")
    messages: List[BaseMessage] = [
        system_msg,
        human_msg1,
    ]
    ai_msg1 = model.invoke(messages)
    print(ai_msg1.content)
    messages.append(ai_msg1)
    messages.append(HumanMessage(content="谢谢"))
    for chunk in  model.stream(messages):
        print(chunk.content,end="",flush=True)

chat1()