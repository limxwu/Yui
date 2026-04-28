from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from core.docling_transformer import YuiDoclingTransformer

# 创建 PDF 转换器
pdf_transformer = YuiDoclingTransformer()

# 转换 PDF为markdown格式
md_text = pdf_transformer.transform2md(".doc/safe1_report.docx")

# 创建文本分块器，默认分块大小为 100，分块重叠为 20
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

md_text_splitter_chunks = text_splitter.split_text(md_text)

print(f"doc length:{len(md_text_splitter_chunks)}")

# 创建 Chroma 向量数据库
embed = OllamaEmbeddings(model="qwen3-embedding:0.6b")
chroma = Chroma(embedding_function=embed, persist_directory='./chroma_db', collection_name='yui_knowledge')

# 向数据库中添加数据 todo 元数据，固定字段=>搜索过滤 模型生成=>搜索增强
chroma.add_documents([Document(text) for text in md_text_splitter_chunks])

# 查询数据库
result = chroma.similarity_search_with_score("交叉验证的实验目的是什么")
print(result)
