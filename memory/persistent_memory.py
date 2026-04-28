from typing import Union

from core.docling_transformer import docling_transformer
from docling_core.types.io import DocumentStream
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from pathlib import Path
from langchain_core.documents import Document


class PersistentMemory:
    """
    基于 Chroma 的持久化记忆
    """

    def __init__(self, persist_directory: str = "./chroma_db", collection_name: str = "yui_knowledge"):
        self.embed = OllamaEmbeddings(model="qwen3-embedding:0.6b")
        self.chroma = Chroma(persist_directory=persist_directory,
                             collection_name=collection_name,
                             embedding_function=self.embed)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        self.docling_transformer = docling_transformer

    async def add_document(self, source: Union[str, Path, DocumentStream]):
        """
        添加文档
        :param source: 文档源
        :return:
        """
        md_text = self.docling_transformer.transform2md(source)
        md_text_splitter_chunks = self.text_splitter.split_text(md_text)
        self.chroma.add_documents([Document(text) for text in md_text_splitter_chunks])

    def similarity_search_with_score(self, query: str):
        """
        相似度搜索
        :param query: 查询语句
        :return:
        """
        return self.chroma.similarity_search_with_score(query)


persistent_memory = PersistentMemory()
