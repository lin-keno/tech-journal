import streamlit as st
from utils.llm import get_model

# --- 页面配置 ---
st.set_page_config(page_title="💬 极简 AI 助理", page_icon="🤖")
st.title("🤖 我的 AI 助理")

# --- 侧边栏设置 ---
with st.sidebar:
    st.header("⚙️ 设置")
    model_option = st.radio("选择模型:", ("Qwen", "OpenAI"))
    st.markdown("---")
    st.caption("💡 请确保 .env 文件中已配置相应的 API Key")

# --- 初始化模型 ---
@st.cache_resource
def load_model(model_name):
    try:
        return get_model(model_name=model_name)
    except Exception as e:
        st.error(f"模型加载失败: {e}")
        return None

# 映射选项到代码名称
model_map = {"Qwen": "qwen", "OpenAI": "openai"}
selected_model_key = model_map[model_option]

llm = load_model(selected_model_key)

# --- 聊天逻辑 ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "你好！我是你的 AI 助手，请问有什么可以帮你？"}
    ]

# 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 处理用户输入
if prompt := st.chat_input("请输入你的问题..."):
    if llm is None:
        st.stop()

    # 显示用户消息
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 获取并显示 AI 回复
    with st.chat_message("assistant"):
        with st.spinner("正在思考..."):
            try:
                response = llm.invoke(prompt)
                # 兼容不同模型的返回格式
                content = response.content if hasattr(response, 'content') else str(response)
                st.markdown(content)
                st.session_state.messages.append({"role": "assistant", "content": content})
            except Exception as e:
                st.error(f"发生错误: {e}")
