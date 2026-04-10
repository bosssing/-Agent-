from typing import List, Dict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from utils.config import get_settings


class InterviewQuestionGenerator:
    def __init__(self, llm=None):
        settings = get_settings()
        self.llm = llm or ChatOpenAI(
            model=settings.openai_model,
            base_url=settings.openai_api_base,
            api_key=settings.openai_api_key,
            temperature=0.7
        )
        
    def generate_questions(
        self, 
        job_type: str, 
        difficulty: str = "medium", 
        question_count: int = 10
    ) -> List[Dict]:
        prompt = ChatPromptTemplate.from_messages([
            ("system", """你是一位专业的面试题生成专家。请根据指定的岗位类型生成面试题。

请以JSON格式返回，格式如下：
{{
    "questions": [
        {{
            "id": 1,
            "type": "技术题/行为题/专业题",
            "question": "问题内容",
            "difficulty": "easy/medium/hard",
            "suggested_answer": "参考答案要点",
            "evaluation_points": ["考察点1", "考察点2"]
        }}
    ]
}}"""),
            ("user", "岗位类型：{job_type}\n难度：{difficulty}\n题目数量：{question_count}")
        ])
        
        chain = prompt | self.llm | JsonOutputParser()
        
        try:
            result = chain.invoke({
                "job_type": job_type,
                "difficulty": difficulty,
                "question_count": question_count
            })
            return result.get("questions", [])
        except Exception as e:
            return self._get_default_questions(job_type, question_count)
    
    def _get_default_questions(self, job_type: str, count: int) -> List[Dict]:
        default_questions = [
            {
                "id": 1,
                "type": "自我介绍",
                "question": "请简单介绍一下你自己",
                "difficulty": "easy",
                "suggested_answer": "包括教育背景、实习经历、项目经验、技能特长等",
                "evaluation_points": ["表达能力", "逻辑思维", "自我认知"]
            },
            {
                "id": 2,
                "type": "行为题",
                "question": "请描述一次你在团队中遇到冲突的经历，以及你是如何解决的",
                "difficulty": "medium",
                "suggested_answer": "使用STAR法则描述，重点说明你的处理方式和结果",
                "evaluation_points": ["沟通能力", "问题解决能力", "团队协作"]
            },
            {
                "id": 3,
                "type": "专业题",
                "question": f"请谈谈你对{job_type}这个岗位的理解",
                "difficulty": "medium",
                "suggested_answer": "岗位职责、技能要求、发展前景等",
                "evaluation_points": ["岗位认知", "职业规划"]
            }
        ]
        return default_questions[:count]
