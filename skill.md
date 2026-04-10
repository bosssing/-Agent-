校招求职全流程多 Agent 协同智能助手
环境：Windows 11, Python 3.11
架构设计：基于 LangGraph 设计多 Agent 协同工作流，拆解为需求分析、岗位匹配、简历优化、面试模拟、知
识库问答 5 个核心角色，设计 Agent 间通信机制，解决单 Agent 能力边界不足、复杂任务完成率低的问题。
Agent 开发与工具集成：基于 LangChain 与主流大模型 API，完成各 Agent 的 Prompt 工程、工具定义与逻辑开
发；实现对接BOSS直聘API并爬取岗位信息、简历优化、PDF 解析 等 多个自定义工具，实现岗位信息获取、面试题生成等核心能力。
知识库与 RAG 优化：基于Milvus 向量数据库实现语义检索大幅降低 Agent 回答幻觉。
工程化落地：基于 FastAPI 开发后端接口，支持流式输出、并发请求与用户权限管理，优化系统稳定性。
前端：基于vue框架实现，与后端接口进行通信，实现用户交互与系统功能。只需要使用简单的对话界面，用户输入文字，前端将用户输入传递给后端，后端将用户输入传递给 LangChain，LangChain 将用户输入传递给模型，模型返回文字结果，返回给前端。
大模型调用如下：
# 2. 初始化 DeepSeek 模型
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(
    model="deepseek-v3",  # 指定要使用的大模型名称
    base_url= "https://dashscope.aliyuncs.com/compatible-mode/v1",  # 指定大模型服务的接口地址（阿里云通义千问兼容OpenAI格式的接口）
    api_key="sk-74087c072d48405bad3cdbb5ae910fd1",  
    temperature=0.7  # 设置模型生成温度（取值0-2），0.7表示生成内容兼具创造性和稳定性（值越高创造性越强，越低越严谨）
)
