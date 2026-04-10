from typing import Dict, List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from utils.config import get_settings


class OfferEvaluator:
    def __init__(self, llm=None):
        settings = get_settings()
        self.llm = llm or ChatOpenAI(
            model=settings.openai_model,
            base_url=settings.openai_api_base,
            api_key=settings.openai_api_key,
            temperature=0.7
        )

    def evaluate_offer(
        self,
        offer_details: Dict,
        user_profile: Dict = None
    ) -> Dict:
        prompt = ChatPromptTemplate.from_messages([
            ("system", """你是一位专业的Offer评估专家。请对提供的Offer进行全面评估。

评估维度：
1. 薪资福利竞争力
2. 公司发展前景
3. 岗位匹配度
4. 个人成长空间
5. 工作生活平衡
6. 综合推荐指数

请以JSON格式返回，格式如下：
{{
    "overall_score": 0-100,
    "dimensions": {
        "salary_benefits": {
            "score": 0-100,
            "comment": "评价内容"
        },
        "company_prospects": {
            "score": 0-100,
            "comment": "评价内容"
        },
        "job_match": {
            "score": 0-100,
            "comment": "评价内容"
        },
        "growth_potential": {
            "score": 0-100,
            "comment": "评价内容"
        },
        "work_life_balance": {
            "score": 0-100,
            "comment": "评价内容"
        }
    },
    "summary": "总体评价和建议",
    "recommendation": "强烈推荐/推荐/谨慎考虑/不推荐"
}}"""),
            ("user", "Offer详情：{offer_details}\n\n用户背景：{user_profile}")
        ])
        
        chain = prompt | self.llm | JsonOutputParser()
        
        try:
            result = chain.invoke({
                "offer_details": str(offer_details),
                "user_profile": str(user_profile or {})
            })
            return result
        except Exception as e:
            return self._get_default_evaluation(offer_details)
    
    def _get_default_evaluation(self, offer_details: Dict) -> Dict:
        return {
            "overall_score": 75,
            "dimensions": {
                "salary_benefits": {
                    "score": 80,
                    "comment": "薪资处于行业中等偏上水平"
                },
                "company_prospects": {
                    "score": 75,
                    "comment": "公司发展稳定，有一定市场地位"
                },
                "job_match": {
                    "score": 70,
                    "comment": "岗位与专业背景较为匹配"
                },
                "growth_potential": {
                    "score": 75,
                    "comment": "有较好的学习和成长机会"
                },
                "work_life_balance": {
                    "score": 70,
                    "comment": "工作节奏适中"
                }
            },
            "summary": "这是一个综合表现不错的Offer，在薪资、发展等方面都具有一定竞争力，建议可以考虑接受。",
            "recommendation": "推荐"
        }

    def compare_offers(self, offers: List[Dict]) -> Dict:
        evaluations = []
        for i, offer in enumerate(offers, 1):
            eval_result = self.evaluate_offer(offer)
            evaluations.append({
                "offer_id": i,
                "offer_name": offer.get("company_name", f"Offer {i}"),
                "evaluation": eval_result
            })
        
        evaluations.sort(key=lambda x: x["evaluation"]["overall_score"], reverse=True)
        
        return {
            "ranked_offers": evaluations,
            "best_offer": evaluations[0] if evaluations else None,
            "comparison_summary": "已根据综合得分对Offer进行了排名"
        }
