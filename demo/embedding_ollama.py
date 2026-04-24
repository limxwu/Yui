from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings

# ollama pull qwen3-embedding:0.6b
embed = OllamaEmbeddings(model="qwen3-embedding:0.6b")

input_text = "The meaning of life is 42"
vector = embed.embed_query(input_text)
print(vector[:3])

from langchain_chroma import Chroma

chroma = Chroma(embedding_function=embed)

docs = [
    Document(
        "有了农民组织以后，第一个行动，就是从政治上把地主阶层特别是土豪劣绅的威风打下去，即是从农村的社会地位上把地主权力打下去，把农民权力长上来。这是一场极其严重、紧要的斗争。这场斗争是第二个时期即革命时期的中心斗争。"),
    Document("一个人如果想要输出，必须依赖积累，这本来就是常识。"),
    Document("15年前，我刚刚向社会推出自己的“断舍离”概念时，在举办讲座期间遇到了很多焦虑的听众。"),
    Document("Chroma 可以在任何需要的地方运行，支持从本地实验到大规模生产工作负载的所有场景。"),
    Document(
        "我国科学家在嫦娥五号月球样品中发现两种月球新矿物，均获国际矿物学协会新矿物命名及分类委员会批准，分别命名为镁嫦娥石与铈嫦娥石。")
]
chroma.add_documents(docs)

result = chroma.similarity_search_with_score("航空航天")
## 分数代表的相关性，或者说是到目标的维度距离（chroma默认设置l2为平方欧几里得距离），数字越小越相关
print(result)
