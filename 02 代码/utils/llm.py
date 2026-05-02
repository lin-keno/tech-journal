import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatTongyi

load_dotenv()

def get_model(model_name="qwen"):
    """
    工厂函数：根据名称返回初始化好的模型对象
    """
    if model_name == "qwen":
        api_key = os.getenv("DASHSCOPE_API_KEY")
        if not api_key:
            raise ValueError("缺少 DASHSCOPE_API_KEY，请检查 .env 文件")
        
        return ChatTongyi(
            model_name="qwen-plus",
            dashscope_api_key=api_key,
            temperature=0.5
        )
    
    elif model_name == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("缺少 OPENAI_API_KEY，请检查 .env 文件")
            
        return ChatOpenAI(
            model_name="gpt-3.5-turbo",
            api_key=api_key,
            temperature=0.5
        )
    
    else:
        raise ValueError(f"不支持的模型: {model_name}")
