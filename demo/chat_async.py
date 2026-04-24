"""
异步对话演示
展示如何使用 asyncio 进行异步 LLM 调用
"""
import asyncio
from typing import List

from core.llm import get_model, aget_model_response
from core.constants import YUI_SYSTEM_PROMPT
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage


async def async_chat_demo():
    """异步对话演示"""
    print("=" * 60)
    print("异步对话演示")
    print("=" * 60)
    
    # 获取模型实例
    model = get_model()
    
    # 准备消息
    system_msg = SystemMessage(content=YUI_SYSTEM_PROMPT)
    human_msg1 = HumanMessage(content="Yui，你好！请介绍一下自己。")
    
    messages: List[BaseMessage] = [system_msg, human_msg1]
    
    print("\n用户: Yui，你好！请介绍一下自己。")
    print("AI: ", end="", flush=True)
    
    # 异步调用
    response = await aget_model_response(model, messages)
    print(response.content)
    
    # 继续对话
    messages.append(HumanMessage(content="你能帮我做什么？"))
    print("\n用户: 你能帮我做什么？")
    print("AI: ", end="", flush=True)
    
    response = await aget_model_response(model, messages)
    print(response.content)
    
    print("\n" + "=" * 60)
    print("对话结束")
    print("=" * 60)


async def concurrent_chat_demo():
    """并发对话演示 - 同时发起多个请求"""
    print("\n" + "=" * 60)
    print("并发对话演示")
    print("=" * 60)
    
    model = get_model()
    
    # 定义多个问题
    questions = [
        "讲一个简短的笑话",
        "今天天气怎么样？（模拟）",
        "推荐一本好书",
    ]
    
    print("\n同时发起 3 个请求...\n")
    
    # 并发执行多个任务
    tasks = []
    for i, question in enumerate(questions, 1):
        messages = [
            SystemMessage(content=YUI_SYSTEM_PROMPT),
            HumanMessage(content=question)
        ]
        task = aget_model_response(model, messages)
        tasks.append((i, question, task))
    
    # 等待所有任务完成
    results = await asyncio.gather(*[task for _, _, task in tasks])
    
    # 打印结果
    for (i, question, _), response in zip(tasks, results):
        print(f"\n问题 {i}: {question}")
        print(f"回答: {response.content[:100]}...")  # 只显示前100字符
    
    print("\n" + "=" * 60)
    print("并发请求完成")
    print("=" * 60)


if __name__ == "__main__":
    # 运行异步对话演示
    asyncio.run(async_chat_demo())
    
    # 运行并发演示
    asyncio.run(concurrent_chat_demo())
