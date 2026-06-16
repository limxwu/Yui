from typing import List

from core.llm import get_model
from core.constants import YUI_SYSTEM_PROMPT
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage
import time


def chat1():
    """演示对话功能"""
    # 获取模型实例
    model = get_model()
    
    # system_msg = SystemMessage(content=YUI_SYSTEM_PROMPT)
    human_msg1 = HumanMessage(content="讲个笑话")
    messages: List[BaseMessage] = [
        # system_msg,
        human_msg1,
    ]
    start_time=time.time()
    ai_msg1 = model.invoke(messages)
    print(ai_msg1.content)
    print(f"cost:{time.time()-start_time}")
    # messages.append(ai_msg1)
    # messages.append(HumanMessage(content="谢谢"))
    # for chunk in  model.stream(messages):
    #     print(chunk.content,end="",flush=True)

if __name__=="__main__":
    from langchain_deepseek import ChatDeepSeek

    # print("begin")
    # chat1()
    # 直接初始化模型并关闭思考模式（DeepSeek 默认开启思考）
    model = ChatDeepSeek(
        model="deepseek-v4-flash",
        temperature=0.7,
        extra_body={"thinking": {"type": "disabled"}},
    )
    system_msg = SystemMessage(content="""
你是一个严格的字段匹配专家。你需要将用户输入的"待匹配字段"映射到以下标准字典中的某一个。这些字段用于审计，标准字段是审计公司设置的，待匹配字段是待审客户提供的。
尽量给每个标准字段做匹配，除非待匹配字段中根据语义明显匹配不上。
待匹配字段与标准字段是一对一的关系。

【输出格式规范】
请严格按照 JSON 格式输出，不要包含任何多余的解释：
[{"standardName": "标准字段名", "mappingName": "匹配到的字段名称"}]
只需要输出能够匹配上的，如果一个都匹配不上，输出空数组即可，例如：[]。
【标准字段】
单位,单据日期,经销商代码,经销商名称,客户代码,产品代码,批号,数量,单位,单据日期,经销商代码,经销商名称,客户代码,客户名称,产品代码,产品名称,批号,数量,规格,单位,经销商处-产品代码,经销商处-客户名称,备用属性1,备用属性2,备用属性3
""")
    human_msg1 = HumanMessage(content="""
【待匹配字段】
主单位,消费日期,下游客户ID,买方名称,买家编号,收货人,SKU编码,品名,流水号,核销数,尺寸,下游产品代码,下游收货人,扩展字段1,扩展字段2,扩展字段3,买方名称,品号,内部物料号
""")
    messages: List[BaseMessage] = [
        system_msg,
        human_msg1,
    ]
    start_time=time.time()
    ai_msg1 = model.invoke(messages)
    print(ai_msg1.content)
    print(f"cost:{time.time()-start_time}")