from langchain_ollama import OllamaLLM
from base import constants

model = OllamaLLM(model='qwen3.5:4b')


def chat1():
    input_text = '请问今天天气怎么样？'

    response = model.invoke(input_text)

    print(response)


def chat2():
    messages = [
        (
            "system",
            constants.ROLE_SYSTEM_DEFINE,
        ),
        ("human", "讲个笑话把."),
    ]
    response = model.invoke(messages, options={'think': False})
    print(response)
