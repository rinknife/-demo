import json
from shop_data import (
    get_products_by_category,
    filter_by_price,
    get_products_by_brand,
    get_shop_info,
    compare_products,
    get_price_alert
)

# 定义 Skills（函数调用元数据）
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

def execute_function_call(function_name, arguments):
    args = json.loads(arguments)

    if function_name == "get_products_by_category":
        result = get_products_by_category(args["category"])
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
        # compare_products 现在返回文本，直接返回字符串
        return result

    elif function_name == "get_price_alert":
        result = get_price_alert(args["product_id"], args.get("target_price", 0))
        # 直接返回文本
        return result

    else:
        return json.dumps({"error": "未知函数"})