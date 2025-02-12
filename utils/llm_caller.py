import openai
import os
def call_openai_response(prompt, model_name):
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    client =openai.Client(
        api_key = api_key,
        base_url = base_url
    )
    response = client.chat.completions.create(
        model = model_name,
        temperature = 0.7,
        messages = [{"role":"user", "content":prompt}]
    )
    return(response.choices[0].message.content)

def call_openai_image_analyse(base64_url):
    system_prompt = '''
    你是一位专门研究人工智能领域（如AI Agent、大语言模型、自然语言处理等领域）的专家讲师。你擅长解释有关人工智能的知识、包括但不限于架构设计、工作原理、以及实现方法。

    你将收到一张关于人工智能的PDF页面或幻灯片图像。你的目标是作为专家讲师,**详尽且通俗易懂地**讲解其中的内容。

    你的讲解应该：

    1.**提供详尽、系统的讲解**，涵盖图像中知识的 **数学背景、理论知识、关键技术** 及 **优化技巧**,如果图像中没有提及这些内容，请不要**提及或进行推断**。如果图像中有示例，你应当**完全、详细地复述并讲解这些示例**。

    2. 如果有图表或表格，请**详尽地讲解图表或表格的内容**,**不要给出宽泛、含糊的讲解**,**使得即使你的学生是初学者，他们也可以轻松学习图像中的内容**。

    3. 不要包括引用内容格式的术语
    不要提及内容类型 - 专注于内容本身
    例如:如果图像上有图表/图表和文字,请同时讨论两者,而不要提及一个是图表,另一个是文字。

    4. 如果图像包含架构图或流程图：
       - 详细解释每个组件的功能和作用
       - 说明组件之间的交互关系
       - 分析数据和控制流的传递过程

    请记住：
    - **你的学生看不到图像，需要详尽的描述**
    - **避免使用过于专业的术语，注重通俗易懂的解释**
    - **不要提及页码或元素在图像上的位置**
    - **不要提及内容的格式，专注于内容本身**
    - **不要提及图像的来源或作者**
    - **将你的讲解限制在750词以内**


    ------

    如果有可识别的标题，请识别标题，如果没有可识别的标题，请总结一个简短的标题，并按以下格式进行讲解：

    {标题}

    {你的讲解}
    '''
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    client =openai.Client(
        api_key = api_key,
        base_url = base_url
    )
    response = client.chat.completions.create(
        model = "gpt-4-vision-preview",
        temperature = 0.7,
        messages = [
            {
                "role":"system", 
                "content": system_prompt
            },
            {
                "role":"user", 
                "content":[
                    {
                    "type":"text",
                    "text":"以下是你要分析的图片。"
                    },
                    {
                    "type":"image_url", 
                    "image_url": {
                        "url": base64_url  # 符合 API 规范
                                }
                    }
                ]
            }
            ],
            max_tokens= 1000,
            top_p= 0.9
    )
    return(response.choices[0].message.content)
