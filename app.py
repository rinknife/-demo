import os
import json
from dotenv import load_dotenv
import gradio as gr
from openai import OpenAI
from shop_data import *

# ====================== 环境 & API ======================
load_dotenv()
client = OpenAI(
    api_key=os.getenv("BAILIAN_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
# ====================== 定义 Skills（函数调用） ======================
functions = [
    {
        "name": "get_products_by_category",
        "description": "根据商品类别获取商品列表，比如手机、耳机、电脑、平板",
        "parameters": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "enum": ["手机", "耳机", "电脑", "平板"],
                    "description": "商品类别"
                }
            },
            "required": ["category"]
        }
    },
    {
        "name": "filter_by_price",
        "description": "根据预算上限筛选商品",
        "parameters": {
            "type": "object",
            "properties": {
                "max_price": {"type": "number", "description": "预算上限"}
            },
            "required": ["max_price"]
        }
    },
    {
        "name": "get_products_by_brand",
        "description": "根据品牌筛选商品",
        "parameters": {
            "type": "object",
            "properties": {
                "brand": {
                    "type": "string",
                    "enum": ["Apple", "小米", "华为", "Sony"],
                    "description": "品牌名称"
                }
            },
            "required": ["brand"]
        }
    },
    {
        "name": "get_shop_info",
        "description": "获取店铺详细信息，包括评分、是否官方等",
        "parameters": {
            "type": "object",
            "properties": {
                "shop_id": {"type": "string", "description": "店铺ID"}
            },
            "required": ["shop_id"]
        }
    },
    {
        "name": "compare_products",
        "description": "对比多个商品的参数",
        "parameters": {
            "type": "object",
            "properties": {
                "product_ids": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "商品ID列表"
                }
            },
            "required": ["product_ids"]
        }
    },
    {
        "name": "get_price_alert",
        "description": "分析商品价格是否值得购买",
        "parameters": {
            "type": "object",
            "properties": {
                "product_id": {"type": "string", "description": "商品ID"},
                "target_price": {"type": "number", "description": "用户的心理价位"}
            },
            "required": ["product_id"]
        }
    }
]

# ====================== 执行函数调用 ======================
def execute_function_call(function_name, arguments):
    """执行大模型请求调用的函数"""
    args = json.loads(arguments)
    
    if function_name == "get_products_by_category":
        result = get_products_by_category(args["category"])
        # 转换为列表格式方便大模型阅读
        products = list(result.values())
        return json.dumps(products, ensure_ascii=False, indent=2)
    
    elif function_name == "filter_by_price":
        result = filter_by_price(args["max_price"])
        products = list(result.values())
        return json.dumps(products, ensure_ascii=False, indent=2)
    
    elif function_name == "get_products_by_brand":
        result = get_products_by_brand(args["brand"])
        products = list(result.values())
        return json.dumps(products, ensure_ascii=False, indent=2)
    
    elif function_name == "get_shop_info":
        result = get_shop_info(args["shop_id"])
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    elif function_name == "compare_products":
        result = compare_products(args["product_ids"])
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    elif function_name == "get_price_alert":
        result = get_price_alert(args["product_id"], args.get("target_price", 0))
        return json.dumps({"message": result}, ensure_ascii=False, indent=2)
    
    else:
        return json.dumps({"error": "未知函数"})

# ====================== 构建商品摘要（你漏掉的函数） ======================
def build_product_summary(products_dict=None):
    """构建商品摘要，如果传入了products_dict就用传入的，否则用全部商品"""
    if products_dict is None:
        products_dict = PRODUCT_DB
    
    product_summary = ""
    for pid, p in products_dict.items():
        product_summary += f"- {p['name']} | {p['price']}元 | 品牌:{p['brand']} | 库存:{p['stock']} | 店铺:{p['shop_id']}\n"
    return product_summary



# ====================== Agent 核心（保留你的提示词，但用函数获取数据） ======================
def agent_chat(user_message, chat_history):
    """
    Agent风格：大模型决定调用哪个函数获取数据，然后用你的提示词格式推荐
    """
    # 构建历史对话上下文
    history_context = ""
    if chat_history:
        history_context = "【历史对话】\n"
        recent = chat_history[-6:] if len(chat_history) > 6 else chat_history
        for turn in recent:
            if turn["role"] == "user":
                history_context += f"用户：{turn['content']}\n"
            else:
                history_context += f"AI：{turn['content']}\n"

    # 系统提示词（让大模型决定调用什么函数）
    function_decision_prompt = f"""
你是一个智能购物Agent。你的任务是理解用户需求，然后调用合适的函数获取商品数据。

{history_context}

用户说：{user_message}

请决定调用哪个函数来获取用户想要的商品信息。
"""
    
    # 第一轮：让大模型决定调用哪个函数
    try:
        response = client.chat.completions.create(
            model="qwen-turbo",
            messages=[{"role": "user", "content": function_decision_prompt}],
            functions=functions,
            function_call="auto",
            temperature=0.3
        )
        
        response_message = response.choices[0].message
        
        # 如果大模型想调用函数
        if response_message.function_call:
            function_name = response_message.function_call.name
            function_args = response_message.function_call.arguments
            
            # 执行函数，获取真实的商品数据
            function_response = execute_function_call(function_name, function_args)
            products_data = json.loads(function_response)
            
            # 把函数返回的商品数据转换成字典格式，用于构建商品摘要
            products_dict = {}
            if isinstance(products_data, list):
                for i, p in enumerate(products_data):
                    # 生成一个临时的product_id
                    temp_id = f"result_{i}"
                    products_dict[temp_id] = p
            else:
                products_dict = {"result": products_data}
            
            # 用获取到的真实数据构建商品摘要
            product_summary = build_product_summary(products_dict)
            
        else:
            # 如果大模型没调用函数，就用全部商品（保底）
            product_summary = build_product_summary()
    
    except Exception as e:
        # 如果出错，保底用全部商品
        print(f"Function calling error: {e}")
        product_summary = build_product_summary()
    
    # ====================== 完全保留你的提示词 ======================
    system_prompt = f"""
你是一个智能购物 Agent。
用户会随意输入购买需求。

【你的任务】
1. 理解用户意图（商品类别、品牌、价格区间、特殊需求等）
2. 参考历史对话理解上下文
3. 从下面商品列表中推荐最匹配的商品（最多5个），必须是同类商品，有几个推荐几个
4. 简洁说明推荐理由
5. 如果用户输入不明确，结合历史对话推测意图

{history_context}

【商品列表】
{product_summary}

【当前用户输入】
{user_message}
"""

    # 第二轮：用你的提示词生成最终推荐
    final_response = client.chat.completions.create(
        model="qwen-turbo",
        messages=[{"role": "user", "content": system_prompt}],
        temperature=0.3
    )

    return final_response.choices[0].message.content



# ====================== Gradio 交互 ======================
def respond(message, chat_history):
    if chat_history is None:
        chat_history = []

    bot_reply = agent_chat(message, chat_history)

    # 返回 messages 格式，Gradio 6.x 必须
    chat_history.append({"role": "user", "content": message})
    chat_history.append({"role": "assistant", "content": bot_reply})

    return "", chat_history

with gr.Blocks(title="AI购物Agent（百炼版）") as demo:
    gr.Markdown("# 🛍️ AI购物Agent（百炼版）")
    
    chatbot = gr.Chatbot(height=500)  # 默认 messages 模式
    msg = gr.Textbox(label="输入需求")
    btn = gr.Button("发送")
    clear = gr.Button("清空对话")

    # 绑定事件
    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    btn.click(respond, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: [], None, chatbot)

if __name__ == "__main__":
    demo.launch(server_port=7860)