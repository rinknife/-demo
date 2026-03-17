"""
抖音商城模拟数据 - 商品库、店铺信息、价格历史
完全模拟真实电商数据结构，供AI购物智能体调用
"""

# 商品数据库（模拟抖音商城商品池）
PRODUCT_DB = {
    # ==================== 手机类 ====================
    "iphone15_001": {
        "product_id": "iphone15_001",
        "name": "Apple iPhone 15 128GB 黑色",
        "category": "手机",
        "sub_category": "智能手机",
        "brand": "Apple",
        "price": 5999,
        "original_price": 6999,
        "discount": "满5999减200",
        "shop_id": "shop_apple_001",
        "is_official": True,
        "sales_volume": "10万+",
        "rating": 4.8,
        "specs": {
            "processor": "A16仿生芯片",
            "screen": "6.1英寸 OLED",
            "camera": "4800万主摄",
            "battery": "3349mAh",
            "weight": "171g",
            "os": "iOS 17"
        },
        "tags": ["官方正品", "全国联保", "12期免息"],
        "good_reviews": ["拍照清晰", "系统流畅", "手感好"],
        "bad_reviews": ["续航一般", "信号不稳定", "充电慢"],
        "price_history": {
            "30d_min": 5399,
            "30d_avg": 5699,
            "30d_max": 6199,
            "lowest_ever": 5299
        },
        "stock": 589,
        "delivery": "次日达"
    },
    
    "xiaomi14_002": {
        "product_id": "xiaomi14_002",
        "name": "小米14 16+512GB 白色",
        "category": "手机",
        "sub_category": "智能手机",
        "brand": "小米",
        "price": 4599,
        "original_price": 4999,
        "discount": "领券减100",
        "shop_id": "shop_xiaomi_001",
        "is_official": True,
        "sales_volume": "5万+",
        "rating": 4.7,
        "specs": {
            "processor": "骁龙8 Gen3",
            "screen": "6.36英寸 1.5K",
            "camera": "徕卡三摄 5000万",
            "battery": "4610mAh",
            "weight": "188g",
            "os": "HyperOS"
        },
        "tags": ["徕卡联名", "90W快充", "IP68"],
        "good_reviews": ["拍照好看", "充电快", "手感小屏"],
        "bad_reviews": ["MIUI广告多", "发热略明显", "电池不耐用"],
        "price_history": {
            "30d_min": 4199,
            "30d_avg": 4399,
            "30d_max": 4699,
            "lowest_ever": 3999
        },
        "stock": 324,
        "delivery": "明日达"
    },
    
    "huawei60_003": {
        "product_id": "huawei60_003",
        "name": "华为 Mate 60 Pro 12+512GB 雅川青",
        "category": "手机",
        "sub_category": "智能手机",
        "brand": "华为",
        "price": 6999,
        "original_price": 7999,
        "discount": "赠碎屏险",
        "shop_id": "shop_huawei_001",
        "is_official": True,
        "sales_volume": "8万+",
        "rating": 4.9,
        "specs": {
            "processor": "麒麟9000S",
            "screen": "6.82英寸 OLED",
            "camera": "XMAGE影像 5000万",
            "battery": "5000mAh",
            "weight": "225g",
            "os": "HarmonyOS 4"
        },
        "tags": ["卫星通话", "昆仑玻璃", "鸿蒙系统"],
        "good_reviews": ["信号强", "系统流畅", "拍照真实"],
        "bad_reviews": ["重", "发热", "价格高"],
        "price_history": {
            "30d_min": 6799,
            "30d_avg": 6999,
            "30d_max": 7299,
            "lowest_ever": 6699
        },
        "stock": 127,
        "delivery": "预订7天"
    },
    
    # ==================== 耳机类 ====================
    "airpods_pro_004": {
        "product_id": "airpods_pro_004",
        "name": "Apple AirPods Pro 2 主动降噪耳机",
        "category": "耳机",
        "sub_category": "真无线降噪",
        "brand": "Apple",
        "price": 1899,
        "original_price": 1999,
        "discount": "无",
        "shop_id": "shop_apple_002",
        "is_official": True,
        "sales_volume": "20万+",
        "rating": 4.9,
        "specs": {
            "type": "入耳式",
            "noise_cancelling": "主动降噪",
            "battery_life": "6小时+30小时充电盒",
            "chip": "H2芯片",
            "waterproof": "IPX4"
        },
        "tags": ["主动降噪", "空间音频", "查找功能"],
        "good_reviews": ["降噪强", "连接稳", "生态好"],
        "bad_reviews": ["贵", "容易掉", "电池衰减快"],
        "price_history": {
            "30d_min": 1799,
            "30d_avg": 1899,
            "30d_max": 1999,
            "lowest_ever": 1699
        },
        "stock": 1023,
        "delivery": "次日达"
    },
    
    "sony_xm5_005": {
        "product_id": "sony_xm5_005",
        "name": "Sony WH-1000XM5 头戴降噪耳机",
        "category": "耳机",
        "sub_category": "头戴降噪",
        "brand": "Sony",
        "price": 2299,
        "original_price": 2899,
        "discount": "满2000减200",
        "shop_id": "shop_sony_001",
        "is_official": True,
        "sales_volume": "3万+",
        "rating": 4.8,
        "specs": {
            "type": "头戴式",
            "noise_cancelling": "旗舰降噪",
            "battery_life": "30小时",
            "driver": "30mm振膜",
            "codec": "LDAC"
        },
        "tags": ["降噪天花板", "佩戴舒适", "30小时续航"],
        "good_reviews": ["降噪无敌", "音质好", "戴着舒服"],
        "bad_reviews": ["夏天热", "收纳盒大", "贵"],
        "price_history": {
            "30d_min": 2099,
            "30d_avg": 2299,
            "30d_max": 2499,
            "lowest_ever": 1999
        },
        "stock": 256,
        "delivery": "明日达"
    },
    
    # ==================== 电脑类 ====================
    "macbook_air_006": {
        "product_id": "macbook_air_006",
        "name": "Apple MacBook Air 13英寸 M2芯片 16+512GB",
        "category": "电脑",
        "sub_category": "轻薄本",
        "brand": "Apple",
        "price": 11499,
        "original_price": 12499,
        "discount": "教育优惠",
        "shop_id": "shop_apple_003",
        "is_official": True,
        "sales_volume": "1万+",
        "rating": 4.9,
        "specs": {
            "processor": "M2 8核",
            "memory": "16GB",
            "storage": "512GB",
            "screen": "13.6英寸 Liquid",
            "battery": "18小时",
            "weight": "1.24kg"
        },
        "tags": ["超长续航", "无风扇", "视网膜屏"],
        "good_reviews": ["轻薄", "续航强", "屏幕好"],
        "bad_reviews": ["接口少", "贵", "散热一般"],
        "price_history": {
            "30d_min": 10999,
            "30d_avg": 11499,
            "30d_max": 11999,
            "lowest_ever": 10499
        },
        "stock": 89,
        "delivery": "次日达"
    },
    
    # ==================== 平板类 ====================
    "ipad_air_007": {
        "product_id": "ipad_air_007",
        "name": "Apple iPad Air 6 11英寸 M2芯片 256GB",
        "category": "平板",
        "sub_category": "平板电脑",
        "brand": "Apple",
        "price": 4799,
        "original_price": 5299,
        "discount": "送保护壳",
        "shop_id": "shop_apple_004",
        "is_official": True,
        "sales_volume": "2万+",
        "rating": 4.8,
        "specs": {
            "processor": "M2芯片",
            "screen": "11英寸 Liquid",
            "storage": "256GB",
            "support": "Apple Pencil",
            "weight": "462g"
        },
        "tags": ["M2芯片", "全面屏", "兼容妙控键盘"],
        "good_reviews": ["性能强", "屏幕好", "便携"],
        "bad_reviews": ["60Hz刷新率", "贵", "配件贵"],
        "price_history": {
            "30d_min": 4599,
            "30d_avg": 4799,
            "30d_max": 4999,
            "lowest_ever": 4499
        },
        "stock": 156,
        "delivery": "明日达"
    }
}


# ==================== 店铺信息表 ====================
SHOP_DB = {
    "shop_apple_001": {
        "shop_id": "shop_apple_001",
        "shop_name": "Apple京东自营旗舰店",
        "platform": "京东",
        "fans": "1000万+",
        "score": 4.9,
        "open_years": 8,
        "customer_service": "7x24h",
        "return_policy": "7天无理由",
        "warranty": "全国联保1年"
    },
    "shop_apple_002": {
        "shop_id": "shop_apple_002",
        "shop_name": "Apple京东自营旗舰店",
        "platform": "京东",
        "fans": "1000万+",
        "score": 4.9,
        "open_years": 8,
        "customer_service": "7x24h",
        "return_policy": "7天无理由",
        "warranty": "全国联保1年"
    },
    "shop_apple_003": {
        "shop_id": "shop_apple_003",
        "shop_name": "Apple京东自营旗舰店",
        "platform": "京东",
        "fans": "1000万+",
        "score": 4.9,
        "open_years": 8,
        "customer_service": "7x24h",
        "return_policy": "7天无理由",
        "warranty": "全国联保1年"
    },
    "shop_apple_004": {
        "shop_id": "shop_apple_004",
        "shop_name": "Apple京东自营旗舰店",
        "platform": "京东",
        "fans": "1000万+",
        "score": 4.9,
        "open_years": 8,
        "customer_service": "7x24h",
        "return_policy": "7天无理由",
        "warranty": "全国联保1年"
    },
    "shop_xiaomi_001": {
        "shop_id": "shop_xiaomi_001",
        "shop_name": "小米京东自营旗舰店",
        "platform": "京东",
        "fans": "500万+",
        "score": 4.8,
        "open_years": 6,
        "customer_service": "7x24h",
        "return_policy": "7天无理由",
        "warranty": "全国联保1年"
    },
    "shop_huawei_001": {
        "shop_id": "shop_huawei_001",
        "shop_name": "华为京东自营旗舰店",
        "platform": "京东",
        "fans": "800万+",
        "score": 4.9,
        "open_years": 7,
        "customer_service": "7x24h",
        "return_policy": "7天无理由",
        "warranty": "全国联保1年"
    },
    "shop_sony_001": {
        "shop_id": "shop_sony_001",
        "shop_name": "Sony官方旗舰店",
        "platform": "抖音小店",
        "fans": "200万+",
        "score": 4.7,
        "open_years": 3,
        "customer_service": "9:00-21:00",
        "return_policy": "7天无理由",
        "warranty": "店铺保修1年"
    }
}


# ==================== 用户历史记录（模拟） ====================
USER_HISTORY = {
    "user_123": {
        "user_id": "user_123",
        "view_history": ["iphone15_001", "xiaomi14_002", "huawei60_003"],
        "purchase_history": ["airpods_pro_004"],
        "preferences": {
            "preferred_brands": ["Apple", "小米"],
            "budget_range": [3000, 7000],
            "payment_method": "微信支付"
        },
        "search_history": ["手机 5000左右", "降噪耳机", "MacBook"]
    }
}


# ==================== 辅助函数 ====================

def get_product_by_id(product_id):
    """根据ID获取商品详情"""
    return PRODUCT_DB.get(product_id)

def get_products_by_category(category):
    """根据分类获取商品列表"""
    return {pid: p for pid, p in PRODUCT_DB.items() if p["category"] == category}

def get_products_by_brand(brand):
    """根据品牌获取商品列表"""
    return {pid: p for pid, p in PRODUCT_DB.items() if p["brand"] == brand}

def filter_by_price(max_price):
    """按价格筛选"""
    return {pid: p for pid, p in PRODUCT_DB.items() if p["price"] <= max_price}

def filter_by_price_range(min_price, max_price):
    """按价格区间筛选"""
    return {pid: p for pid, p in PRODUCT_DB.items() if min_price <= p["price"] <= max_price}

def get_shop_info(shop_id):
    """获取店铺信息"""
    return SHOP_DB.get(shop_id)

def compare_products(product_ids):
    """对比多个商品（返回对比表格数据）"""
    products = [PRODUCT_DB[pid] for pid in product_ids if pid in PRODUCT_DB]
    return products

def get_price_alert(product_id, target_price):
    """价格提醒（模拟）"""
    product = PRODUCT_DB.get(product_id)
    if not product:
        return None
    current = product["price"]
    lowest = product["price_history"]["lowest_ever"]
    if target_price >= current:
        return f"当前价格{current}元，已达到你的目标价{target_price}元，可直接购买"
    elif target_price < lowest:
        return f"目标价{target_price}元低于历史最低{lowest}元，可能较难达到"
    else:
        return f"当前价格{current}元，历史最低{lowest}元，建议设置降价提醒"