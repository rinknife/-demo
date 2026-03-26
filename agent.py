import json
from openai import OpenAI
import config
import prompts
import functions
from utils import *

client = OpenAI(api_key=config.BAILIAN_API_KEY, base_url=config.BASE_URL)


#疑似未调用
def agent_loop(messages, max_steps=3):
    products_dict = {}
    for step in range(max_steps):
        response = client.chat.completions.create(
            model=config.MODEL_NAME,
            messages=messages,
            functions=functions.functions,
            function_call="auto",
            temperature=config.TEMPERATURE
        )
        msg = response.choices[0].message
        if msg.function_call:
            func_name = msg.function_call.name
            func_args = msg.function_call.arguments
            print(f"[Step {step+1}] 调用函数: {func_name}, 参数: {func_args}")
            result = functions.execute_function_call(func_name, func_args)
            try:
                data = json.loads(result)
                if isinstance(data, list):
                    temp = {}
                    for i, p in enumerate(data):
                        temp[f"result_{i}"] = p
                    products_dict = temp
                elif isinstance(data, dict):
                    products_dict = {"result": data}
            except:
                pass
            messages.append({
                "role": "assistant",
                "function_call": {"name": func_name, "arguments": func_args}
            })
            messages.append({
                "role": "function",
                "name": func_name,
                "content": result
            })
        else:
            return msg.content, products_dict
    return messages[-1].get("content", "抱歉，推理超时。"), products_dict

def agent_chat(user_message, chat_history, last_products=None):
    """
    购物助手核心函数，根据用户消息和历史对话生成回复，并返回推荐的商品列表。
    """
    # 1. 构建历史文本（用于提示词）并提取上一轮的商品（如果有）
    history_text, stored_products = build_conversation_history(chat_history)
    if last_products is None:
        last_products = stored_products

    # 2. 复用场景：如果用户表达犹豫（如“不知道选哪个”）且上一轮有商品，则直接复用这些商品
    if should_reuse_last_products(user_message, last_products):
        products_dict = last_products
        product_summary = build_product_summary(products_dict)
        system_prompt = prompts.SYSTEM_PROMPT.format(
            history=history_text,
            product_summary=product_summary,
            user_message=user_message
        )
        final_response = client.chat.completions.create(
            model=config.MODEL_NAME,
            messages=[{"role": "user", "content": system_prompt}],
            temperature=config.TEMPERATURE
        )
        return {
            "reply": final_response.choices[0].message.content,
            "products": products_dict
        }

    # 3. 规则优先：用正则提取用户意图
    intent = extract_user_intent(user_message)
    print(f"[Intent] {intent}")

    # 4. 从上一轮商品中继承品类和品牌（如果当前消息中未提供）
    if "category" not in intent and last_products:
        for p in last_products.values():
            if "category" in p:
                intent["category"] = p["category"]
                print(f"[State] 继承品类: {intent['category']}")
                break
    if "brand" not in intent and last_products:
        for p in last_products.values():
            if "brand" in p:
                intent["brand"] = p["brand"]
                print(f"[State] 继承品牌: {intent['brand']}")
                break

    # 5. 处理价格反馈（例如“太贵”）
    price_feedback_keywords = ["贵", "太贵", "超出预算", "买不起", "便宜点"]
    if any(kw in user_message for kw in price_feedback_keywords) and last_products:
        # 获取上一轮推荐商品的最低价格
        min_price = min(p["price"] for p in last_products.values())
        # 新价格上限 = 最低价的90%（不低于100）
        new_price = max(int(min_price * 0.9), 100)
        # 更新意图中的价格
        intent["price"] = new_price
        intent["price_loose"] = True
        intent["action"] = "recommend"
        print(f"[Price Feedback] 调整价格上限为 {new_price}")

    # 6. 处理对比意图
    if intent["action"] == "compare" and "compare" in intent:
        ids = []
        for name in intent["compare"]:
            pid = map_product_name_to_id(name)
            if pid:
                ids.append(pid)
        if len(ids) == 2:
            result = functions.execute_function_call("compare_products", json.dumps({"product_ids": ids}))
            return {"reply": result, "products": {}}
        else:
            return {"reply": "请提供两个明确的商品名称，例如“对比 iPhone 15 和小米14”。", "products": {}}

    # 7. 处理价格预警意图（值不值得买）
    if intent["action"] == "price_alert" and "price_alert" in intent:
        pid = map_product_name_to_id(intent["price_alert"])
        if pid:
            result = functions.execute_function_call("get_price_alert", json.dumps({"product_id": pid}))
            return {"reply": result, "products": {}}
        else:
            return {"reply": "请提供具体的商品名称，例如“小米14值不值得买”。", "products": {}}

    # 8. 处理推荐意图（价格/品牌/品类组合条件）
    if intent["action"] == "recommend":
        products_data = None

        # 8.1 价格筛选
        if "price" in intent:
            result = functions.execute_function_call("filter_by_price", json.dumps({"max_price": intent["price"]}))
            products_data = json.loads(result)
            if not products_data and intent.get("price_loose"):
                # 放宽10%
                result = functions.execute_function_call("filter_by_price", json.dumps({"max_price": intent["price"] * 1.1}))
                products_data = json.loads(result)

        # 8.2 品牌筛选
        if "brand" in intent and products_data is not None:
            products_data = [p for p in products_data if p["brand"] == intent["brand"]]
        elif "brand" in intent:
            result = functions.execute_function_call("get_products_by_brand", json.dumps({"brand": intent["brand"]}))
            products_data = json.loads(result)

        # 8.3 品类筛选
        if "category" in intent and products_data is not None:
            products_data = [p for p in products_data if p["category"] == intent["category"]]
        elif "category" in intent:
            result = functions.execute_function_call("get_products_by_category", json.dumps({"category": intent["category"]}))
            products_data = json.loads(result)

        # 8.4 如果最终没有商品，返回友好提示
        if not products_data:
            if "price" in intent:
                return {
                    "reply": f"抱歉，在 {intent.get('price', '')} 元以内没有找到符合条件的商品。您可以提高预算或尝试其他品牌。",
                    "products": {}
                }
            else:
                return {
                    "reply": "抱歉，没有找到符合您条件的商品。您可以告诉我更具体的需求（如预算、品牌等）。",
                    "products": {}
                }

        # 8.5 打分排序，取前5个
        ranked = score_products(products_data, intent)
        products_dict = {f"rank_{i}": p for i, p in enumerate(ranked[:5])}
        product_summary = build_product_summary(products_dict)

        # 8.6 调用模型生成推荐理由
        system_prompt = prompts.SYSTEM_PROMPT.format(
            history=history_text,
            product_summary=product_summary,
            user_message=user_message
        )
        final_response = client.chat.completions.create(
            model=config.MODEL_NAME,
            messages=[{"role": "user", "content": system_prompt}],
            temperature=config.TEMPERATURE
        )
        return {
            "reply": final_response.choices[0].message.content,
            "products": products_dict
        }

    # 9. 如果以上所有规则都没有匹配，则退化为模型决策
    messages = [
        {"role": "user", "content": prompts.FUNCTION_DECISION_PROMPT.format(
            history=history_text,
            user_message=user_message
        )}
    ]
    try:
        final_reply, products_dict = agent_loop(messages)
        return {"reply": final_reply, "products": products_dict}
    except Exception as e:
        print(f"Agent loop error: {e}")
        return {"reply": "抱歉，处理过程中出现错误。", "products": {}}