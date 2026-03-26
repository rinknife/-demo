import json
import config
from agent import agent_chat
from openai import OpenAI
import random
# 初始化裁判模型客户端（使用同一个 API）
judge_client = OpenAI(api_key=config.BAILIAN_API_KEY, base_url=config.BASE_URL)

# 裁判提示词模板
JUDGE_PROMPT = """
你是一个严格的评测专家。请判断以下购物助手的回复是否满足用户的需求。

【用户问题】
{user_input}

【购物助手回复】
{agent_reply}

【评测要求】
1. 回复是否准确理解了用户的需求？（例如：价格、品牌、类别等）
2. 推荐的商品是否合理匹配用户的条件？
3. 如果用户要求对比，回复是否给出了有意义的对比分析？
4. 回答是否清晰、有帮助？

请输出 JSON 格式，包含两个字段：
- "passed": true 或 false
- "reason": 简短的判断理由（中文）

只输出 JSON，不要输出其他内容。
"""

def judge_with_llm(user_input, agent_reply):
    """调用大模型评判回复质量"""
    prompt = JUDGE_PROMPT.format(user_input=user_input, agent_reply=agent_reply)
    try:
        response = judge_client.chat.completions.create(
            model=config.MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1  # 低温度，保证评判稳定
        )
        result = response.choices[0].message.content.strip()
        # 尝试解析 JSON
        try:
            data = json.loads(result)
            return data.get("passed", False), data.get("reason", "无理由")
        except json.JSONDecodeError:
            # 如果模型没输出合法 JSON，简单处理
            if "true" in result.lower():
                return True, "模型判定通过"
            else:
                return False, "模型判定不通过"
    except Exception as e:
        print(f"裁判调用失败: {e}")
        return False, "裁判出错"

# 预定义测试模板（覆盖多种场景）
test_templates = [
    # 价格约束
    ("推荐一款{price}元以内的{category}", {"price": [500, 1000, 1500, 2000, 3000, 5000], "category": ["手机", "耳机", "电脑", "平板"]}),
    ("{budget}元能买到什么{category}", {"budget": [500, 1000, 1500, 2000, 3000], "category": ["手机", "耳机"]}),
    ("我想买{category}，预算{price}左右", {"price": [800, 1200, 1800, 2500, 4000], "category": ["手机", "平板"]}),
    # 品牌约束
    ("{brand}的{category}怎么样", {"brand": ["华为", "小米", "Apple", "荣耀", "OPPO"], "category": ["手机", "耳机"]}),
    ("推荐一款{brand}手机", {"brand": ["华为", "小米", "Apple", "荣耀"]}),
    # 品类约束
    ("最近想买个{category}", {"category": ["手机", "耳机", "电脑", "平板"]}),
    ("{category}推荐", {"category": ["手机", "耳机", "电脑", "平板"]}),
    # 对比
    ("对比{product1}和{product2}", {"product1": ["iPhone 15", "小米14", "华为Mate 60"], "product2": ["小米14", "华为Pura70", "荣耀Magic6"]}),
    ("{product1}和{product2}哪个好", {"product1": ["iPhone 15", "小米14", "华为Mate 60"], "product2": ["小米14", "华为Pura70", "荣耀Magic6"]}),
    # 价格+品牌组合
    ("{brand}手机{price}元以内的", {"brand": ["华为", "小米", "Apple"], "price": [2000, 3000, 4000, 5000]}),
    ("预算{price}左右，想要{brand}的{category}", {"price": [1500, 2500, 3500], "brand": ["华为", "小米"], "category": ["手机", "平板"]}),
    # 模糊意图
    ("想买个手机，不知道哪个好", {}),
    ("帮我选一个", {}),
    ("哪个更划算", {}),
    # 价格预警
    ("{product}值不值得买", {"product": ["iPhone 15", "小米14", "华为Mate 60"]}),
    ("{product}现在价格合适吗", {"product": ["iPhone 15", "小米14", "华为Mate 60"]}),
]

def generate_test_cases(n=100):
    """根据模板随机生成 n 个测试用例"""
    test_cases = []
    while len(test_cases) < n:
        template, params_dict = random.choice(test_templates)
        # 随机填充参数
        filled = template
        for key, values in params_dict.items():
            if values:
                filled = filled.replace(f"{{{key}}}", str(random.choice(values)))
        # 避免重复
        if filled not in [case["input"] for case in test_cases]:
            test_cases.append({"input": filled, "description": "自动生成"})
    return test_cases

def evaluate(test_cases):
    results = []
    failed_reasons = []  # 收集失败的原因文本
    for case in test_cases:
        user_input = case["input"]
        print(f"\n正在评测: {user_input}")
        try:
            agent_response = agent_chat(user_input, chat_history=[])
            reply = agent_response["reply"]
            passed, reason = judge_with_llm(user_input, reply)
            results.append({
                "input": user_input,
                "passed": passed,
                "reason": reason,
                "reply_preview": reply[:200] + ("..." if len(reply) > 200 else "")
            })
            if not passed:
                failed_reasons.append(reason)
        except Exception as e:
            results.append({
                "input": user_input,
                "passed": False,
                "reason": f"Agent执行异常: {str(e)}",
                "reply_preview": ""
            })
            failed_reasons.append("Agent执行异常")
    return results, failed_reasons
if __name__ == "__main__":
    # 生成100个测试用例
    test_cases = generate_test_cases(100)
    print(f"生成了 {len(test_cases)} 个测试用例")
    
    results, failed_reasons = evaluate(test_cases)
    
    # 输出统计报告
    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    print(f"\n通过率: {passed}/{total} ({passed/total*100:.1f}%)")
    
    # 对失败原因进行聚类
    from collections import Counter
    reason_counts = Counter(failed_reasons)
    print("\n失败原因统计:")
    for reason, count in reason_counts.most_common():
        print(f"  {reason}: {count} 次")
    
    # 可选：输出部分失败案例详情
    print("\n失败案例预览（前5个）:")
    fail_samples = [r for r in results if not r["passed"]][:5]
    for i, r in enumerate(fail_samples):
        print(f"{i+1}. 输入: {r['input']}")
        print(f"   失败原因: {r['reason']}")
        print(f"   回复预览: {r['reply_preview']}\n")