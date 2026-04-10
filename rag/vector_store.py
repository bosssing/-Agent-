from typing import List, Dict, Optional
from langchain_core.documents import Document
import numpy as np


class SentenceBERTEmbeddings:
    def __init__(self):
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
            self.available = True
        except ImportError:
            self.model = None
            self.available = False
            print("警告: sentence-transformers 未安装，将使用简单的词频统计作为备用方案")
    
    def embed_query(self, text: str) -> List[float]:
        if self.available and self.model:
            return self.model.encode(text).tolist()
        return self._simple_embed(text)
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        if self.available and self.model:
            return self.model.encode(texts).tolist()
        return [self._simple_embed(text) for text in texts]
    
    def _simple_embed(self, text: str) -> List[float]:
        words = text.lower().split()
        vocab = sorted(set(words))
        vec = [0.0] * 100
        for i, word in enumerate(words[:100]):
            vec[i] = hash(word) % 1000 / 1000.0
        return vec


class VectorStore:
    def __init__(self):
        self.embeddings = SentenceBERTEmbeddings()
        self.documents: List[Document] = []
        self._init_sample_data()

    def _init_sample_data(self):
        sample_docs = [
            Document(
                page_content="校招流程一般包括：网申、笔试、一面、二面、HR面、Offer发放。每个公司的具体流程可能有所不同，但大致是这样的顺序。",
                metadata={"category": "校招流程", "source": "校招指南"}
            ),
            Document(
                page_content="简历制作的关键要点：1. 简洁明了，一页纸最佳；2. 突出实习和项目经验；3. 使用数据量化成果；4. 针对性优化，根据不同岗位调整简历内容。",
                metadata={"category": "简历技巧", "source": "简历指南"}
            ),
            Document(
                page_content="常见的面试类型包括：技术面、行为面、群面、压力面、HR面等。不同的面试类型考察重点不同，需要针对性准备。",
                metadata={"category": "面试技巧", "source": "面试指南"}
            ),
            Document(
                page_content="STAR法则是描述经历的有效方法：Situation（情境）、Task（任务）、Action（行动）、Result（结果）。按照这个结构组织回答，会更加清晰有条理。",
                metadata={"category": "面试技巧", "source": "面试指南"}
            ),
            Document(
                page_content="谈薪资的技巧：1. 提前了解行业薪资水平；2. 不要主动先开口；3. 给出合理区间；4. 综合考虑福利和发展空间。",
                metadata={"category": "薪资谈判", "source": "求职指南"}
            ),
            Document(
                page_content="Offer评估需要考虑：薪资福利、公司平台、岗位匹配度、成长空间、工作地点、工作强度、企业文化等多个维度。",
                metadata={"category": "Offer选择", "source": "求职指南"}
            ),
            Document(
                page_content="互联网行业主要岗位包括：后端开发、前端开发、算法、产品经理、运营、测试、运维、数据分析等。不同岗位的技能要求和发展路径各不相同。",
                metadata={"category": "岗位介绍", "source": "行业指南"}
            ),
            Document(
                page_content="计算机专业学生的核心技能：数据结构与算法、编程语言（Java/Python/C++）、计算机网络、操作系统、数据库、系统设计等。",
                metadata={"category": "技能要求", "source": "技术指南"}
            )
        ]
        self.documents = sample_docs

    def add_documents(self, documents: List[Document]):
        self.documents.extend(documents)

    def similarity_search(self, query: str, k: int = 3) -> List[Document]:
        query_embedding = self.embeddings.embed_query(query)
        doc_embeddings = [
            self.embeddings.embed_query(doc.page_content)
            for doc in self.documents
        ]
        
        scores = []
        for i, doc_emb in enumerate(doc_embeddings):
            similarity = self._cosine_similarity(query_embedding, doc_emb)
            scores.append((similarity, self.documents[i]))
        
        scores.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in scores[:k]]

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = sum(a * a for a in vec1) ** 0.5
        norm2 = sum(b * b for b in vec2) ** 0.5
        if norm1 == 0 or norm2 == 0:
            return 0
        return dot_product / (norm1 * norm2)

    def as_retriever(self):
        class SimpleRetriever:
            def __init__(self, vector_store):
                self.vector_store = vector_store
            
            def get_relevant_documents(self, query: str) -> List[Document]:
                return self.vector_store.similarity_search(query)
        
        return SimpleRetriever(self)
