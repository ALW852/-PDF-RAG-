from pdfminer.high_level import extract_text
from pdf2image import convert_from_path     
import base64  
from io import BytesIO                   

def extractor_pdf_to_text(doc_path):
    """读取pdf文件中的文本内容"""
    text = extract_text(doc_path)
    return  text

def extractor_pdf_to_images_uri(doc_path):
    """将pdf文件除第一页的其余页面转化为png图像的base64uri"""
    poppler_path = r"C:\poppler-24.08.0\Library\bin" 
    imgs = convert_from_path(doc_path, poppler_path= poppler_path)
    imgs = imgs[1:]  #去除第一页（通常为标题页）
    uri = []
    for index in range(len(imgs)):
        buffer = BytesIO()
        imgs[index].save(buffer,format="PNG")
        base64_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
        base64_uri = f"data:image/png;base64,{base64_image}"
        uri.append(base64_uri)
    return uri





