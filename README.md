# 校招求职全流程多Agent协同智能助手

基于LangGraph和LangChain构建的校招求职全流程多Agent协同智能助手系统，覆盖从职业规划、简历优化、笔试准备、面试辅导到Offer评估的完整求职周期。包含Vue前端界面和FastAPI后端服务。

## 环境要求
- Windows 11
- Python 3.11

## 项目架构

### 核心Agent
1. **需求分析Agent** - 分析学生背景和求职意向，提供职业规划建议
2. **岗位匹配Agent** - 根据学生背景匹配适合的校招岗位
3. **简历优化Agent** - 提供简历优化建议和修改方案
4. **面试模拟Agent** - 生成面试题和模拟面试练习
5. **知识库问答Agent** - 基于RAG回答校招相关问题

### 工具集
- **PDF解析器** - 解析简历PDF文件
- **BOSS直聘API** - 搜索岗位信息
- **面试题生成器** - 生成针对性面试题
- **Offer评估器** - 评估和对比多个Offer

### 前端界面
- **Vue 3** - 现代化的对话界面
- **Axios** - 与后端API通信
- 美观的UI设计，支持快捷操作

### 技术栈
- **LangGraph** - 多Agent协同工作流
- **LangChain** - LLM应用开发框架
- **FastAPI** - 后端API服务
- **DeepSeek V3** - 大语言模型（通过阿里云通义千问兼容接口）
- **Vue 3** - 前端框架
- **Milvus** - 向量数据库（可选，当前使用内存实现）

## 快速开始

### 1. 环境配置

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑.env文件，配置已预置DeepSeek V3模型信息
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 运行项目

#### 方式一：启动Web应用（推荐）

启动后端服务后，访问 http://localhost:8000 即可使用Vue前端界面：

```bash
python main.py
# 然后选择 1 启动API服务器
```

或直接运行：

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

- 前端界面：http://localhost:8000
- API文档：http://localhost:8000/docs

#### 方式二：交互式命令行

```bash
python main.py
# 然后选择 2 进入交互式模式
```

#### 方式三：运行示例代码

```bash
python example.py
```

## API接口

### 聊天接口
```
POST /api/chat
Content-Type: application/json

{
  "user_input": "我想做职业规划",
  "context": {}
}
```

### 上传简历
```
POST /api/upload-resume
Content-Type: multipart/form-data

file: resume.pdf
```

### 搜索岗位
```
POST /api/search-jobs
Content-Type: application/json

{
  "keyword": "Python开发",
  "city": "杭州",
  "page": 1,
  "page_size": 10
}
```

### 生成面试题
```
POST /api/generate-interview-questions
Content-Type: application/json

{
  "job_type": "Java开发工程师",
  "difficulty": "medium",
  "question_count": 10
}
```

### 评估Offer
```
POST /api/evaluate-offer
Content-Type: application/json

{
  "offer_details": {
    "company_name": "阿里巴巴",
    "salary": "30k*16"
  },
  "user_profile": {}
}
```

### 对比Offer
```
POST /api/compare-offers
Content-Type: application/json

{
  "offers": [
    {"company_name": "A公司", ...},
    {"company_name": "B公司", ...}
  ]
}
```

## 项目结构

```
ma-2/
├── agents/                 # Agent实现
│   ├── demand_analysis_agent.py
│   ├── job_matching_agent.py
│   ├── resume_optimization_agent.py
│   ├── interview_simulation_agent.py
│   └── knowledge_base_agent.py
├── tools/                  # 工具集
│   ├── pdf_parser.py
│   ├── boss_zhipin_api.py
│   ├── interview_question_generator.py
│   └── offer_evaluator.py
├── rag/                    # RAG系统
│   ├── vector_store.py
│   └── rag_engine.py
├── core/                   # 核心模块
│   ├── base_agent.py
│   └── workflow.py
├── api/                    # API接口
│   └── main.py
├── utils/                  # 工具函数
│   ├── config.py
│   └── helpers.py
├── frontend/               # Vue前端界面
│   └── index.html
├── main.py                 # 主入口
├── example.py              # 使用示例
├── requirements.txt        # 依赖
├── .env.example           # 环境变量模板
├── README.md               # 项目文档
└── skill.md               # 原始需求文档
```

## 使用示例

### 1. 职业规划咨询
```python
from core.workflow import CampusRecruitmentWorkflow

workflow = CampusRecruitmentWorkflow()
result = workflow.run("我是计算机专业学生，适合做什么岗位？")
print(result['result'])
```

### 2. 简历优化
```python
context = {
    "resume_content": "我的简历内容...",
    "target_job": "后端开发工程师"
}
result = workflow.run("帮我优化简历", context)
```

### 3. 面试准备
```python
context = {
    "target_job": "Python后端开发",
    "interview_type": "技术面试"
}
result = workflow.run("帮我准备面试", context)
```

### 4. Offer评估
```python
from tools import OfferEvaluator

evaluator = OfferEvaluator()
result = evaluator.evaluate_offer({
    "company_name": "某公司",
    "salary": "25k*14",
    "job_name": "开发工程师"
})
print(result['overall_score'])
```

## 注意事项

1. 本项目使用模拟数据作为示例，实际使用时需要：
   - 配置真实的OpenAI API密钥
   - 集成真实的招聘平台API
   - 配置Milvus向量数据库

2. 建议在生产环境中：
   - 添加用户认证和权限管理
   - 实现请求限流
   - 添加日志监控
   - 使用LangSmith进行调试和评估

## 许可证

MIT License
