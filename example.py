#!/usr/bin/env python3
"""
校招求职全流程多Agent协同智能助手 - 使用示例
"""
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("校招求职全流程多Agent协同智能助手 - 使用示例")
print("=" * 60)


def example_1_demand_analysis():
    print("\n【示例1】需求分析Agent")
    print("-" * 40)
    from core.workflow import CampusRecruitmentWorkflow
    
    workflow = CampusRecruitmentWorkflow()
    
    user_input = """
    你好，我是一名计算机科学与技术专业的大四学生，GPA 3.8/4.0，
    有过两段实习经历，分别是在一家创业公司做后端开发和在大厂做算法实习生。
    我现在比较迷茫，不知道毕业后应该选择做后端开发还是算法工程师，
    希望你能帮我分析一下。
    """
    
    result = workflow.run(user_input)
    print(f"处理Agent: {result['agent']}")
    print("\n分析结果:")
    print(result['result'])


def example_2_resume_optimization():
    print("\n\n【示例2】简历优化Agent")
    print("-" * 40)
    from core.workflow import CampusRecruitmentWorkflow
    
    workflow = CampusRecruitmentWorkflow()
    
    context = {
        "resume_content": """
        张三
        计算机科学与技术 本科
        实习经历：
        - 某公司 后端开发实习生 2023.06-2023.09
          做了一些后端开发工作
        - 某大厂 算法实习生 2023.03-2023.05
          参与了算法项目
        """,
        "target_job": "后端开发工程师"
    }
    
    result = workflow.run("请帮我优化简历", context)
    print(f"处理Agent: {result['agent']}")
    print("\n优化建议:")
    print(result['result'])


def example_3_interview_simulation():
    print("\n\n【示例3】面试模拟Agent")
    print("-" * 40)
    from core.workflow import CampusRecruitmentWorkflow
    
    workflow = CampusRecruitmentWorkflow()
    
    context = {
        "target_job": "Python后端开发工程师",
        "interview_type": "技术面试"
    }
    
    result = workflow.run("我明天有一个Python后端开发的面试，请帮我准备一下", context)
    print(f"处理Agent: {result['agent']}")
    print("\n面试准备:")
    print(result['result'])


def example_4_job_search():
    print("\n\n【示例4】岗位搜索工具")
    print("-" * 40)
    from tools import BossZhipinAPI
    
    boss_api = BossZhipinAPI()
    jobs = boss_api.search_jobs(keyword="Python开发", city="杭州", page_size=3)
    
    print(f"找到 {len(jobs)} 个岗位:")
    for job in jobs:
        print(f"\n- {job['company_name']} - {job['job_name']}")
        print(f"  薪资: {job['salary']} | 地点: {job['city']}")


def example_5_interview_questions():
    print("\n\n【示例5】面试题生成")
    print("-" * 40)
    from tools import InterviewQuestionGenerator
    
    generator = InterviewQuestionGenerator()
    questions = generator.generate_questions(
        job_type="Java开发工程师",
        difficulty="medium",
        question_count=3
    )
    
    print(f"生成了 {len(questions)} 道面试题:")
    for q in questions:
        print(f"\n[{q['type']}] {q['question']}")
        print(f"  难度: {q['difficulty']}")
        if q.get('suggested_answer'):
            print(f"  参考答案: {q['suggested_answer'][:50]}...")


def example_6_offer_evaluation():
    print("\n\n【示例6】Offer评估")
    print("-" * 40)
    from tools import OfferEvaluator
    
    evaluator = OfferEvaluator()
    
    offer = {
        "company_name": "阿里巴巴",
        "job_name": "Java开发工程师",
        "salary": "30k*16",
        "city": "杭州",
        "department": "淘宝技术部",
        "benefits": ["五险一金", "股票", "年终奖", "免费班车"]
    }
    
    result = evaluator.evaluate_offer(offer_details=offer)
    print(f"综合评分: {result['overall_score']}/100")
    print(f"推荐指数: {result['recommendation']}")
    print("\n各维度评分:")
    for dimension, data in result['dimensions'].items():
        print(f"  - {dimension}: {data['score']}/100 - {data['comment']}")


def example_7_rag_query():
    print("\n\n【示例7】RAG知识库问答")
    print("-" * 40)
    from rag import RAGEngine
    
    rag = RAGEngine()
    
    question = "如何制作一份好的简历？"
    result = rag.query(question)
    
    print(f"问题: {question}")
    print("\n回答:")
    print(result['answer'])
    print("\n参考来源:")
    for i, source in enumerate(result['sources'], 1):
        print(f"  [{i}] {source['content'][:80]}...")


if __name__ == "__main__":
    try:
        example_1_demand_analysis()
        example_2_resume_optimization()
        example_3_interview_simulation()
        example_4_job_search()
        example_5_interview_questions()
        example_6_offer_evaluation()
        example_7_rag_query()
        
        print("\n" + "=" * 60)
        print("所有示例运行完成！")
        print("=" * 60)
    except Exception as e:
        print(f"\n运行示例时出错: {str(e)}")
        import traceback
        traceback.print_exc()
