import json
from utils.extractors import extractor_pdf_to_images_uri
from utils.llm_caller import call_openai_image_analyse
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

def extract_corpus(file_list):
    """创建一个列表来存储所有文件的信息
    将所有pdf文件的页面用LLM进行分析，并将描述结构化地存储进json文件中，形成未来以供使用的知识库。"""
    documents_info = []
    # 遍历文件列表
    for file_name in file_list:
        if file_name.endswith('.pdf'):
            doc_path = f"Raw_KB/{file_name}"
            print(f"正在处理文件: {file_name}")
            
            # 获取文件的所有页面URI
            uris = extractor_pdf_to_images_uri(doc_path)
            
            # 创建文件信息字典
            doc_info = {
                "file_name": file_name,
                "pages": []
            }
            
            # 对每个页面进行分析
            for page_num, uri in enumerate(uris):
                try:
                    description = call_openai_image_analyse(uri)
                    page_info = {
                        "page_number": page_num + 1,
                        "description": description
                    }
                    doc_info["pages"].append(page_info)
                    print(f"- 已完成第 {page_num + 1} 页的分析")
                except Exception as e:
                    print(f"- 处理第 {page_num + 1} 页时出错: {str(e)}")
            
            # 将文件信息添加到总列表中
            documents_info.append(doc_info)
            print(f"完成文件 {file_name} 的处理\n")
    # 保存为JSON文件
    output_path = "pdf_descriptions.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(documents_info, f, ensure_ascii=False, indent=2)
    # 打印处理结果统计
    print("\n处理完成！")
    print(f"共处理了 {len(documents_info)} 个文件")
    for doc in documents_info:
        print(f"{doc['file_name']}: {len(doc['pages'])} 页")


def Split_into_chunks(documents_info):
    """
    将文档描述分割成chunks
    documents_info: 包含文件和页面信息的列表
    返回: 包含chunks的列表，每个chunk包含ID和内容
    """
    text_splitter = RecursiveCharacterTextSplitter(
        # 分割设置
        chunk_size=300,
        chunk_overlap=50,
        separators=["\n\n", "\n", "。", "！", "？", ".", "!", "?", " ", ""],  # 优先在这些位置分割
        length_function=len,
        is_separator_regex=False
    )
    all_chunks = []
    
    for doc in documents_info:
        file_name = doc["file_name"]
        
        for page in doc["pages"]:
            page_num = page["page_number"]
            description = page["description"]
            
            # 分割文本
            chunks = text_splitter.split_text(description)
            
            # 为每个chunk创建记录
            for chunk_num, chunk_text in enumerate(chunks, 1):
                # 清理chunk文本（去除多余的空白字符）
                chunk_text = ' '.join(chunk_text.split())
                    
                chunk_info = {
                    "chunk_id": f"{file_name}_page{page_num}_chunk{chunk_num}",
                    "file_name": doc["file_name"],
                    "page_number": page_num,
                    "chunk_number": chunk_num,
                    "content": chunk_text
                }
                all_chunks.append(chunk_info)
    
    return all_chunks

def process_and_save_chunks():
    """
    加载PDF描述，分割成chunks并保存
    """
    # 加载PDF描述
    with open("pdf_descriptions.json", "r", encoding="utf-8") as f:
        documents_info = json.load(f)
    
    # 分割成chunks
    chunks = Split_into_chunks(documents_info)
    
    # 保存chunks到新的JSON文件
    output_path = "knowledge_base/pdf_chunks.json"
    
    # 确保目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)
        
    print(f"\n处理完成！")
    print(f"共生成了 {len(chunks)} 个chunks")
    print(f"Chunks已保存到: {output_path}")
    
    # 显示一些示例
    print("\n示例chunks:")
    for chunk in chunks[:3]:  # 显示前3个chunks
        print(f"\nChunk ID: {chunk['chunk_id']}")
        print(f"Content preview: {chunk['content'][:100]}...")

# 使用示例：
# 假设已经有了documents_info（从JSON文件加载或之前的处理结果）
"""
# 加载JSON文件
with open("pdf_descriptions.json", "r", encoding="utf-8") as f:
    documents_info = json.load(f)

# 分割成chunks
chunks = Split_into_chunks(documents_info)

# 可以选择将chunks保存为新的JSON文件
with open("pdf_chunks.json", "w", encoding="utf-8") as f:
    json.dump(chunks, f, ensure_ascii=False, indent=2)
"""
