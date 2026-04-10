from typing import Dict, Any, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from agents import (
    DemandAnalysisAgent,
    JobMatchingAgent,
    ResumeOptimizationAgent,
    InterviewSimulationAgent,
    KnowledgeBaseAgent
)
from rag import RAGEngine


class AgentState(TypedDict):
    user_input: str
    context: Dict[str, Any]
    current_agent: str
    result: str
    next_steps: list


class CampusRecruitmentWorkflow:
    def __init__(self):
        self.demand_analysis_agent = DemandAnalysisAgent()
        self.job_matching_agent = JobMatchingAgent()
        self.resume_optimization_agent = ResumeOptimizationAgent()
        self.interview_simulation_agent = InterviewSimulationAgent()
        self.knowledge_base_agent = KnowledgeBaseAgent()
        self.rag_engine = RAGEngine()
        
        self.workflow = self._build_workflow()
        self.app = self.workflow.compile()

    def _build_workflow(self) -> StateGraph:
        workflow = StateGraph(AgentState)
        
        workflow.add_node("demand_analysis", self._demand_analysis_node)
        workflow.add_node("job_matching", self._job_matching_node)
        workflow.add_node("resume_optimization", self._resume_optimization_node)
        workflow.add_node("interview_simulation", self._interview_simulation_node)
        workflow.add_node("knowledge_base", self._knowledge_base_node)
        
        workflow.set_entry_point("router")
        workflow.add_node("router", self._router_node)
        
        workflow.add_conditional_edges(
            "router",
            self._route,
            {
                "demand_analysis": "demand_analysis",
                "job_matching": "job_matching",
                "resume_optimization": "resume_optimization",
                "interview_simulation": "interview_simulation",
                "knowledge_base": "knowledge_base",
                "END": END
            }
        )
        
        workflow.add_edge("demand_analysis", END)
        workflow.add_edge("job_matching", END)
        workflow.add_edge("resume_optimization", END)
        workflow.add_edge("interview_simulation", END)
        workflow.add_edge("knowledge_base", END)
        
        return workflow

    def _router_node(self, state: AgentState) -> AgentState:
        return state

    def _route(self, state: AgentState) -> str:
        user_input = state["user_input"].lower()
        
        keywords = {
            "demand_analysis": ["职业规划", "需求分析", "背景分析", "求职意向", "发展方向", "我适合什么"],
            "job_matching": ["岗位匹配", "找工作", "推荐岗位", "匹配度", "投什么"],
            "resume_optimization": ["简历", "优化简历", "修改简历", "简历润色", "简历改进"],
            "interview_simulation": ["面试", "模拟面试", "面试准备", "面试题", "面试技巧"],
            "knowledge_base": ["问答", "咨询", "问题", "如何", "怎么", "什么是"]
        }
        
        for agent, kw_list in keywords.items():
            for kw in kw_list:
                if kw in user_input:
                    return agent
        
        return "knowledge_base"

    def _demand_analysis_node(self, state: AgentState) -> AgentState:
        result = self.demand_analysis_agent.process({
            "user_input": state["user_input"],
            "context": state["context"]
        })
        return {
            **state,
            "current_agent": "demand_analysis",
            "result": result["result"],
            "context": result["context"]
        }

    def _job_matching_node(self, state: AgentState) -> AgentState:
        result = self.job_matching_agent.process({
            "user_profile": state.get("context", {}).get("demand_analysis", state["user_input"]),
            "job_info": state.get("context", {}).get("job_info", "互联网公司校招岗位"),
            "context": state["context"]
        })
        return {
            **state,
            "current_agent": "job_matching",
            "result": result["result"],
            "context": result["context"]
        }

    def _resume_optimization_node(self, state: AgentState) -> AgentState:
        result = self.resume_optimization_agent.process({
            "resume_content": state.get("context", {}).get("resume_content", state["user_input"]),
            "target_job": state.get("context", {}).get("target_job", "软件开发工程师"),
            "context": state["context"]
        })
        return {
            **state,
            "current_agent": "resume_optimization",
            "result": result["result"],
            "context": result["context"]
        }

    def _interview_simulation_node(self, state: AgentState) -> AgentState:
        result = self.interview_simulation_agent.process({
            "user_profile": state.get("context", {}).get("demand_analysis", state["user_input"]),
            "target_job": state.get("context", {}).get("target_job", "软件开发工程师"),
            "interview_type": state.get("context", {}).get("interview_type", "综合面试"),
            "context": state["context"]
        })
        return {
            **state,
            "current_agent": "interview_simulation",
            "result": result["result"],
            "context": result["context"]
        }

    def _knowledge_base_node(self, state: AgentState) -> AgentState:
        knowledge_context = self.rag_engine.get_knowledge_context(state["user_input"])
        result = self.knowledge_base_agent.process({
            "question": state["user_input"],
            "knowledge_context": knowledge_context,
            "context": state["context"]
        })
        return {
            **state,
            "current_agent": "knowledge_base",
            "result": result["result"],
            "context": result["context"]
        }

    def run(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        initial_state: AgentState = {
            "user_input": user_input,
            "context": context or {},
            "current_agent": "",
            "result": "",
            "next_steps": []
        }
        
        result = self.app.invoke(initial_state)
        return {
            "success": True,
            "agent": result["current_agent"],
            "result": result["result"],
            "context": result["context"]
        }
