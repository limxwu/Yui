import io

from docling.datamodel.base_models import DocumentStream
from fastapi import APIRouter, UploadFile, HTTPException

from memory.persistent_memory import persistent_memory
from utils.logger import logger

memory_router = APIRouter()


@memory_router.post('/document')
async def upload_document(file: UploadFile):
    """
    上传文档并添加到知识库
    
    Args:
        file: 上传的文件（支持 PDF、DOCX 等格式）
        
    Returns:
        dict: 包含处理结果的字典
    """
    try:
        # 记录开始上传
        logger.info(f"开始上传文档: {file.filename}, 文件大小: {len(await file.read())} bytes")
        
        # 1. 读取文件内容
        await file.seek(0)  # 重置文件指针到开头
        file_content = await file.read()
        logger.debug(f"文件 '{file.filename}' 读取完成，大小: {len(file_content)} bytes")
        
        # 2. 将字节包装成内存流 (io.BytesIO)
        buf = io.BytesIO(file_content)
        
        # 3. 构造 Docling 所需的流对象
        source = DocumentStream(name=file.filename, stream=buf)
        logger.info(f"正在处理文档: {file.filename}")
        
        # 4. 添加到持久化记忆
        await persistent_memory.add_document(source)
        logger.info(f"文档 '{file.filename}' 已成功添加到知识库")
        
        return {
            "success": True,
            "message": f"文档 '{file.filename}' 已成功上传并处理",
            "filename": file.filename
        }
    except Exception as e:
        logger.error(f"文档处理失败 [{file.filename}]: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"文档处理失败: {str(e)}"
        )
