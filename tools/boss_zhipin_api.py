import requests
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv

load_dotenv()


class BossZhipinAPI:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("BOSS_ZHIPIN_API_KEY", "")
        self.base_url = "https://api.zhipin.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Authorization": f"Bearer {self.api_key}" if self.api_key else ""
        }

    def search_jobs(
        self, 
        keyword: str, 
        city: str = "", 
        page: int = 1, 
        page_size: int = 10
    ) -> List[Dict]:
        mock_jobs = [
            {
                "job_id": "1",
                "job_name": f"{keyword}开发工程师",
                "company_name": "阿里巴巴",
                "salary": "25k-40k",
                "city": city or "杭州",
                "experience": "应届生",
                "education": "本科",
                "description": "负责{keyword}相关产品的开发与维护，要求掌握Python/Java等编程语言，有良好的算法基础。",
                "tags": ["五险一金", "年终奖", "弹性工作"]
            },
            {
                "job_id": "2",
                "job_name": f"初级{keyword}工程师",
                "company_name": "腾讯",
                "salary": "20k-35k",
                "city": city or "深圳",
                "experience": "应届生",
                "education": "本科",
                "description": "参与{keyword}相关项目的开发，要求计算机相关专业，有实习经验优先。",
                "tags": ["股票期权", "免费班车", "员工食堂"]
            },
            {
                "job_id": "3",
                "job_name": f"{keyword}实习生",
                "company_name": "字节跳动",
                "salary": "300-500/天",
                "city": city or "北京",
                "experience": "在校生",
                "education": "本科及以上",
                "description": "参与{keyword}核心业务的开发，有留用机会，要求每周至少实习4天。",
                "tags": ["转正机会", "免费三餐", "下午茶"]
            }
        ]
        return mock_jobs

    def get_job_detail(self, job_id: str) -> Optional[Dict]:
        mock_detail = {
            "job_id": job_id,
            "job_name": "软件开发工程师",
            "company_name": "某知名互联网公司",
            "salary": "25k-40k",
            "city": "杭州",
            "experience": "应届生",
            "education": "本科",
            "description": "岗位职责：1. 负责产品功能的设计与开发；2. 参与技术方案的讨论与制定；3. 维护和优化现有系统。任职要求：1. 计算机相关专业本科及以上学历；2. 掌握至少一门编程语言；3. 有良好的数据结构和算法基础；4. 有实习经验优先。",
            "company_size": "10000人以上",
            "company_industry": "互联网",
            "publish_date": "2024-01-15"
        }
        return mock_detail

    def get_company_info(self, company_name: str) -> Optional[Dict]:
        mock_company = {
            "company_name": company_name,
            "company_size": "10000人以上",
            "company_industry": "互联网",
            "company_desc": f"{company_name}是一家知名的互联网公司，专注于科技创新和产品研发。",
            "benefits": ["五险一金", "年终奖", "股票期权", "弹性工作", "免费班车"]
        }
        return mock_company
