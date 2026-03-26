from shop_data import PRODUCT_DB
import re

# 商品名称到ID的映射表（可扩展）
PRODUCT_NAME_TO_ID = {
    "iPhone 15": "iphone15_001",
    "小米14": "xiaomi14_002",
    "华为Mate 60": "huawei60_003",
    "华为 Pura70": "huawei_pura70_012",
    "荣耀 Magic6": "honor_magic6_013",
    "荣耀X50": "honor_x50_024",
    "红米K70": "redmi_k70_011",
    "一加12": "oneplus_12_017",
    "OPPO Find X7": "oppo_find_x7_014",
    "vivo X100": "vivo_x100_015",
    "三星S24": "samsung_s24_016",
}

def build_product_summary(products_dict=None):
    if products_dict is None:
        products_dict = PRODUCT_DB
    summary = ""
    for pid, p in products_dict.items():
        summary += f"- {p['name']} | {p['price']}元 | 品牌:{p['brand']} | 库存:{p['stock']} | 店铺:{p['shop_id']}\n"
    return summary

def build_conversation_history(chat_history, max_turns=6):
    history_text = ""
    last_products = None
    if chat_history:
        history_text = "【历史对话】\n"
        recent = chat_history[-max_turns:] if len(chat_history) > max_turns else chat_history
        for turn in recent:
            if turn["role"] == "user":
                history_text += f"用户：{turn['content']}\n"
            else:
                history_text += f"AI：{turn['content']}\n"
                if "products" in turn:
                    last_products = turn["products"]
    return history_text, last_products

def should_reuse_last_products(user_message, last_products):
    if not last_products:
        return False
    hesitation_words = ["不知道", "哪个", "犹豫", "纠结", "怎么选", "帮我选", "推荐哪个", "选哪个"]
    return any(word in user_message for word in hesitation_words)


##关键部分
def extract_user_intent(user_message):
    """
    返回结构化意图字典，包含:
    - price: int (价格上限)
    - brand: str (品牌)
    - category: str (品类)
    - compare: list (对比的商品名称)
    - price_alert: str (价格预警的商品名称)
    - action: str (recommend, compare, price_alert, unknown)
    """
    intent = {"action": "unknown"}

    # ========== 1. 价格提取 ==========
    # 问题：正则只能匹配 "数字+元+可选(以内/左右/预算)"，但用户可能说“1500元以下”、“不超过2000元”、“预算1500”等，未覆盖
    # 另外，“左右”只检测用户消息中是否出现“左右”二字，但若用户说“1500左右”，确实能匹配到，但若说“1500元上下”则漏掉
    price_pattern = r'(\d+)\s*元(?:\s*以内|左右|预算)?'
    price_match = re.search(price_pattern, user_message)
    if price_match:
        intent["price"] = int(price_match.group(1))
        # 问题：仅检测“左右”二字，若用户说“大约1500”、“1500上下”则不识别为宽松
        if "左右" in user_message:
            intent["price_loose"] = True

    # ========== 2. 品牌提取 ==========
    # 问题：品牌列表硬编码，缺少别名（如“苹果”映射到“Apple”已处理，但“iPhone”未映射为Apple）
    # 此外，品牌可能出现在商品名称中，如“华为Mate 60”，这里只会匹配到“华为”，但若用户说“Mate 60”则漏掉品牌
    brands = ["Apple", "苹果", "小米", "华为", "荣耀", "OPPO", "vivo", "三星", "Sony"]
    for b in brands:
        if b in user_message:
            intent["brand"] = "Apple" if b == "苹果" else b
            break   # 只取第一个匹配的品牌，若用户同时提到多个品牌则只记录一个

    # ========== 3. 品类提取 ==========
    # 问题：品类列表有限，未覆盖“笔记本”（应映射到“电脑”）、“蓝牙耳机”（应映射到“耳机”）等
    categories = ["手机", "耳机", "电脑", "平板"]
    for c in categories:
        if c in user_message:
            intent["category"] = c
            break

    # ========== 4. 对比意图 ==========
    # 问题：正则要求“A和B”或“A与B”等形式，但用户可能说“A对比B”、“A和B对比”、“A vs B哪个好”等。
    # 正则中的 [\w\s]+? 会匹配包含空格的多个单词，但中文“和”前后可能没有空格，可能能匹配。
    # 但若用户说“对比iPhone 15和小米14”，正则中“对比”会先被消耗？实际上“对比”在 if 条件中已判断，但这里用“和|与|vs|对比”作为分隔符，可能会把“对比”当作分隔符，导致提取结果错误。
    # 例如“对比iPhone 15和小米14”，分隔符“对比”被匹配后，name1变成空，name2变成“iPhone 15和小米14”，显然错误。
    # 应该使用更精确的分隔符：在“对比”之后寻找“和”或“与”作为实际分隔符。
    if "对比" in user_message or "哪个好" in user_message or "比较" in user_message:
        # 尝试提取两个商品名
        match = re.search(r'([\w\s]+?)(?:和|与|vs|对比)([\w\s]+?)(?:哪个好|怎么样|$)', user_message)
        if match:
            name1 = match.group(1).strip()
            name2 = match.group(2).strip()
            # 清洗多余空格
            name1 = re.sub(r'\s+', ' ', name1)
            name2 = re.sub(r'\s+', ' ', name2)
            intent["compare"] = [name1, name2]
            intent["action"] = "compare"
        # 问题：若用户只说“哪个好”而没有给出两个商品，正则匹配不到，但仍可能进入这个if，导致action未设置

    # ========== 5. 价格预警（值不值得买） ==========
    # 问题：同样使用简单的正则提取商品名，可能提取范围过大，如“小米14现在价格合适吗”会提取出“小米14现在”，导致映射失败
    if "值不值得" in user_message or "值得买" in user_message or "价格合适吗" in user_message:
        # 提取商品名：匹配到关键词前的任意字符
        product_match = re.search(r'([\w\s]+?)(?:值不值得|值得买|价格合适)', user_message)
        if product_match:
            intent["price_alert"] = product_match.group(1).strip()
            intent["action"] = "price_alert"

    # ========== 6. 默认动作 ==========
    # 问题：若未匹配到对比/价格预警，但有价格/品牌/品类之一，则设为推荐。但用户可能同时有价格和品牌，仍设为推荐，这是合理的。
    # 但若用户输入“帮我选一个”，没有任何条件，action保持unknown，后续会走模型决策或引导提示。
    if intent["action"] == "unknown":
        if any(k in intent for k in ["price", "brand", "category"]):
            intent["action"] = "recommend"

    return intent

def extract_current_state(chat_history):
    """
    从历史对话中提取当前累积的状态（品类、品牌）
    返回一个字典，包含可能已明确的意图。
    """
    state = {}
    # 从最近的助手回复中提取商品信息（如果有）
    for turn in reversed(chat_history):
        if turn["role"] == "assistant" and "products" in turn and turn["products"]:
            # 取最近一次推荐的商品列表，从中提取品类和品牌
            for p in turn["products"].values():
                if "category" in p and "category" not in state:
                    state["category"] = p["category"]
                if "brand" in p and "brand" not in state:
                    state["brand"] = p["brand"]
                # 如果已经找到品类和品牌，可以提前结束
                if "category" in state and "brand" in state:
                    break
            break
    return state

def map_product_name_to_id(name):
    """将商品名称映射到ID，支持模糊匹配"""
    return PRODUCT_NAME_TO_ID.get(name.strip())

def score_products(products, user_intent):
    """
    products: 商品列表（字典列表）
    user_intent: 意图字典
    返回排序后的商品列表
    """
    scored = []
    for p in products:
        score = 0
        if user_intent.get("price"):
            if p["price"] <= user_intent["price"]:
                score += 3
            elif user_intent.get("price_loose") and p["price"] <= user_intent["price"] * 1.1:
                score += 1
        if user_intent.get("brand") and p["brand"] == user_intent["brand"]:
            score += 2
        if p.get("stock", 0) > 0:
            score += 1
        if p.get("rating", 0) >= 4.5:
            score += 1
        scored.append((p, score))
    scored.sort(key=lambda x: x[1], reverse=True)
    return [p for p, _ in scored]