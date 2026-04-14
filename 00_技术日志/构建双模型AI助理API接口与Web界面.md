**GitHub技术日志：2026-04-15 周三任务总结 —— 构建双模型AI助理API接口与Web界面**

**一、任务目标**
今日核心目标：

1. **构建支持OpenAI与通义千问的双核AI助理API接口**，实现模型动态切换功能。
2. **开发Web界面**，通过下拉菜单允许用户实时选择模型，兼顾灵活性与成本效益。
3. **整合免费额度策略**，确保通义千问API的合理使用，同时保留OpenAI接口的兼容性。

**二、关键技术组件**

1. **API框架与Web界面**：
    - 使用**Streamlit**快速搭建交互式Web界面，集成侧边栏模型选择组件。
    - 支持双模型切换的下拉菜单，动态调整API调用逻辑。
2. **模型集成**：
    - **OpenAI**：通过`OpenAI`库调用`gpt-4o`模型，处理流式响应。
    - **通义千问**：使用`dashscope`库，调用`qwen-turbo`模型并适配流式输出。
3. **密钥管理与环境配置**：
    - 通过`.env`文件存储双模型API密钥，使用`dotenv`库加载环境变量。
    - 密钥不存在时自动禁用对应模型选项，避免报错。
4. **流式响应优化**：
    - 统一两个模型的流式输出处理逻辑，实时展示生成内容。
    - 添加进度指示符（"▌"）提升用户体验。
5. **错误处理与容错机制**：
    - 捕获API调用异常，通过`st.error`显示错误信息。
    - 无密钥时阻止程序运行，提示用户检查配置。

**三、任务完成情况**

1. **双模型集成与切换**：
    - 完成模型选择下拉菜单，根据用户选择动态切换API调用逻辑。
    - 验证OpenAI（若密钥有效）与通义千问均能正确返回流式对话结果。
2. **Web界面开发**：
    - 使用Streamlit构建交互式聊天界面，支持历史消息记录。
    - 侧边栏集成模型选择、当前模型提示及密钥检查逻辑。
3. **密钥与额度管理**：
    - 自动检测密钥有效性，仅显示可用模型选项（例如：OpenAI密钥失效时隐藏该选项）。
    - 通义千问集成免费额度监控逻辑（参考昨日任务，代码中预留接口）。
4. **测试与验证**：
    - 模拟密钥缺失场景，验证程序报错提示正确性。
    - 切换模型后对话功能正常，流式输出无延迟问题。
5. **代码优化**：
    - 统一错误处理流程，确保异常时保存对话历史。
    - 封装模型调用函数，提升代码复用性（如`call_openai()`与`call_dashscope()`）。

**四、关键代码片段**

```
# app.py 核心逻辑（节选）

# 加载密钥并初始化客户端
openai_key = os.getenv("OPENAI_API_KEY")
dashscope_key = os.getenv("DASHSCOPE_API_KEY")
client_openai = OpenAI(api_key=openai_key) if openai_key else None
dashscope.api_key = dashscope_key if dashscope_key else None

# 生成模型选项
model_options = []
if client_openai:
    model_options.append("OpenAI (GPT-4o)")
if dashscope_key:
    model_options.append("通义千问 (Qwen-Turbo)")
selected_model = st.sidebar.selectbox("选择模型", model_options)

# 根据选择调用API
if selected_model == "OpenAI (GPT-4o)":
    stream = client_openai.chat.completions.create(
        model="gpt-4o",
        messages=st.session_state.messages,
        stream=True
    )
    for chunk in stream:
        # 处理流式输出...
elif selected_model == "通义千问 (Qwen-Turbo)":
    response = Generation.call(
        model='qwen-turbo',
        messages=st.session_state.messages,
        incremental_output=True,  # 流式输出
        stream=True
    )
    for chunk in response:
        if chunk.status_code == 200:
            # 处理流式输出...
        else:
            st.error(f"通义千问错误: {chunk.message}")
```

**五、关键功能截图**
（附：Web界面示意图，展示模型选择下拉菜单与实时对话效果）

**六、明日计划（周四）**

1. **集成Advanced RAG系统**：
    - 实现基于向量数据库的检索增强生成（RAG），提升回答准确性。
    - 支持文件上传与知识库关联，结合通义千问或OpenAI完成上下文对话。
2. **优化双模型切换逻辑**：
    - 添加模型性能监控指标（延迟、准确率），辅助用户决策。
    - 探索自动切换策略（如通义千问额度不足时降级至OpenAI免费层）。

**七、总结与价值**

- **灵活性与成本平衡**：通过双模型架构，用户可灵活切换高性价比方案（通义千问）与高性能模型（OpenAI）。
- **生产级兼容性**：完整集成密钥检测、错误容错机制，确保服务稳定性。
- **可扩展基础**：模块化设计便于未来集成更多模型（如腾讯混元、华为盘古）。

**技术标签**：#双模型切换 #OpenAI #通义千问 #Streamlit #流式响应 #API集成
**作者**：[你的GitHub用户名]
**日期**：2026-04-15
**仓库链接**：[GitHub仓库地址]
**备注**：完整代码、界面截图及RAG系统设计文档详见仓库。

---

**亮点说明**：

1. **双核驱动架构**：同时支持OpenAI与通义千问，兼顾性能与成本。
2. **动态切换界面**：通过Streamlit实现实时模型选择，提升用户体验。
3. **完整容错机制**：密钥缺失时自动禁用选项，避免运行报错。
4. **流式输出优化**：统一双模型流式处理逻辑，确保对话实时性。

**任务验证**：已通过多场景测试，符合周三任务目标，可无缝衔接周四RAG系统集成。

