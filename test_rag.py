#!/usr/bin/env python3
"""
测试RAG系统
"""
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from rag import VectorStore, RAGEngine

def test_vector_store():
    print("测试向量存储...")
    vector_store = VectorStore()
    
    print(f"加载了 {len(vector_store.documents)} 个文档")
    
    print("\n测试相似性搜索: '如何制作好简历'")
    docs = vector_store.similarity_search("如何制作好简历")
    
    for i, doc in enumerate(docs, 1):
        print(f"\n--- 结果 {i} ---")
        print(f"内容: {doc.page_content[:100]}...")
        print(f"元数据: {doc.metadata}")
    
    return True

def test_rag_engine():
    print("\n\n测试RAG引擎...")
    rag_engine = RAGEngine()
    
    question = "如何制作好简历"
    print(f"\n问题: {question}")
    
    result = rag_engine.query(question)
    
    print(f"\n回答: {result['answer']}")
    print(f"\n来源数量: {len(result['sources'])}")
    
    return True

if __name__ == "__main__":
    try:
        print("=" * 60)
        print("开始测试RAG系统")
        print("=" * 60)
        
        test_vector_store()
        test_rag_engine()
        
        print("\n" + "=" * 60)
        print("✅ 所有测试通过！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
