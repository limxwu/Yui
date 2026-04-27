import re


def is_low_quality_text(text: str, threshold=0.2) -> bool:
    """
    判断文本是否为损坏的编码
    threshold: 乱码字符占总长度的比例
    """
    if not text.strip():
        return True

    # 匹配你遇到的 /Gxx 这种字形 ID 模式
    glyph_pattern = r"/G[0-9A-F]{2,4}"
    glyphs = re.findall(glyph_pattern, text)

    # 计算乱码字符约占总文本的比例
    quality_score = len("".join(glyphs)) / len(text)

    return quality_score > threshold


from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat


def smart_convert(file_path):
    # 阶段 1：快速文本提取（关闭 OCR）
    options_fast = PdfPipelineOptions()
    options_fast.do_ocr = False

    converter_fast = DocumentConverter(
        format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=options_fast)}
    )

    result = converter_fast.convert(file_path)
    sample_text = result.document.export_to_markdown()[:2000]  # 只检测前2000字提升效率

    # 阶段 2：质量判定
    if is_low_quality_text(sample_text):
        print(f"检测到编码损坏，正在切换到 OCR 模式解析: {file_path}")

        # 重新配置高精度 OCR 选项
        options_ocr = PdfPipelineOptions()
        options_ocr.do_ocr = True
        options_ocr.ocr_options.force_full_page_ocr = True
        options_ocr.ocr_options.lang = ["ch_sim", "en"]

        converter_ocr = DocumentConverter(
            format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=options_ocr)}
        )
        return converter_ocr.convert(file_path)

    return result


result = smart_convert("./.doc/hd7279a.pdf")
print(result.document.export_to_markdown())
