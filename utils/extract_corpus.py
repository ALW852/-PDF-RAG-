import json
from utils.extractors import extractor_pdf_to_images_uri
from utils.llm_caller import call_openai_image_analyse
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
