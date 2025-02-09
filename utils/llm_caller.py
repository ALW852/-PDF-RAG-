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
    你是一位在人工智能领域有着丰富经验的讲师，你擅长于基于PDF页面或幻灯片图像向学员们讲解有关人工智能的知识。

    你将收到一张PDF页面或幻灯片的图像，你的目标是作为人工智能讲师，**详尽且通俗易懂地**讲解图像中知识的内容。

    你的目标是：

    1.**提供详尽、系统的讲解**，涵盖图像中知识的 **数学背景、理论知识、关键技术** 及 **优化技巧**。如果图像中有示例，你应当**完全、详细地复述并讲解这些示例**。

    2. 如果有图表或表格，请**详尽地讲解图表或表格的内容**，**不要给出宽泛、含糊的讲解**，**使得即使你的学生是初学者，他们也可以轻松学习图像中的内容**。

    3. 不要包括引用内容格式的术语
    不要提及内容类型 - 专注于内容本身
    例如:如果图像上有图表/图表和文字,请同时讨论两者,而不要提及一个是图表,另一个是文字。

    请记住,**你的学生们看不到图像,所以要详尽地描述内容**。

    排除与内容无关的元素:
    **不要提及页码或元素在图像上的位置。**

    ------

    如果有可识别的标题,请识别标题，如果没有可识别的输出，那么请你总结出一个简短的标题，并按以下格式教授你的读者:

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
