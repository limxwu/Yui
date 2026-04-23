from langchain_deepseek import ChatDeepSeek
import getpass
import os
from base import constants

if not os.getenv("DEEPSEEK_API_KEY"):
    os.environ["DEEPSEEK_API_KEY"] = getpass.getpass("Enter your DeepSeek API key: ")

model = ChatDeepSeek(
    model="deepseek-chat"
)


def chat1():
    messages = [
        ("system", constants.ROLE_SYSTEM_DEFINE),
        ("human", "Yui,讲个爆笑的笑话，嘿嘿")
    ]
    response = model.invoke(messages)
    print(response.content)
