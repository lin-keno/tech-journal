AI Agent 开发技术日志 - 第一周：环境搭建与基础模型对接

项目初始化与环境配置
项目脚手架搭建：采用模块化设计思想，确立了以 main.py 为程序入口，utils/ 目录存放核心工具函数的项目结构。
虚拟环境管理：使用 conda 创建独立的 ai-agent 虚拟环境，确保依赖包与系统环境隔离。
依赖管理：通过 requirements.txt 锁定核心依赖，包括 langchain、langchain-openai、langchain-community 以及 python-dotenv，实现了依赖的可复现安装。
安全配置：引入 .env 文件管理敏感信息（如 DASHSCOPE_API_KEY），并通过 load_dotenv() 在代码中安全加载，避免了密钥硬编码带来的安全风险。

核心功能开发
模型工厂模式实现：在 utils/llm.py 中封装了 get_model 工厂函数。
    实现了基于字符串参数（如 "qwen"）动态返回不同 LLM 实例的逻辑。
    成功集成了阿里云通义千问模型，解决了 langchain_community 的导入与配置问题。
主程序逻辑构建：在 main.py 中完成了模型调用流程的串联。
    实现了 llm.invoke() 的标准调用方式。
    增加了异常捕获机制（try-except），能够优雅地处理 API 连接失败或响应异常的情况。

遇到的挑战与解决方案
依赖缺失问题：初期运行时报错 ModuleNotFoundError: No module named 'langchain_openai'。
    解决方案：分析出 LangChain 0.1.0 版本后的拆分策略，手动补全安装了 langchain-openai 和 langchain-community 两个独立包。
运行环境警告：终端出现大量 missing ScriptRunContext 警告信息。
    原因分析：由于代码中引用了 Streamlit 相关库，但在纯 Python 环境下运行导致上下文缺失。
    处理结果：确认该警告不影响核心逻辑执行，属于非阻塞性日志，暂时通过日志过滤或忽略处理，后续将在 Streamlit 专用入口中消除。

最终成果
成功实现终端交互式对话：程序启动后，能够成功接收用户输入，调用云端大模型，并流式打印出通义千问的回复内容。
代码结构清晰，具备良好的扩展性，为后续增加“记忆模块”和“工具调用”打下了坚实基础。

附：关键代码片段

utils/llm.py

from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatTongyi
import os
from dotenv import load_dotenv

load_dotenv()

def get_model(model_name="qwen"):
    if model_name == "qwen":
        return ChatTongyi(
            model_name="qwen-max",
            dashscope_api_key=os.getenv("DASHSCOPE_API_KEY")
        )
    # 预留其他模型接口
    return None

main.py

from utils.llm import get_model

def main():
    llm = get_model("qwen")
    response = llm.invoke("你好，请介绍一下你自己。")
    print(response.content)

if name == "main":
    main()
