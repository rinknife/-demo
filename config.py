import os
from dotenv import load_dotenv

load_dotenv()

# API 配置
BAILIAN_API_KEY = os.getenv("BAILIAN_API_KEY")
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"



# 模型参数   新增
MODEL_NAME = "qwen3.5-35b-a3b"
TEMPERATURE = 0.3
MAX_TOKENS = 2048