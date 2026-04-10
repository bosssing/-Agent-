from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from pathlib import Path
from core.workflow import CampusRecruitmentWorkflow
from tools import PDFParser, BossZhipinAPI, InterviewQuestionGenerator, OfferEvaluator
from rag import RAGEngine
import json

app = FastAPI(title="校招求职全流程多Agent协同智能助手", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")

workflow = CampusRecruitmentWorkflow()
pdf_parser = PDFParser()
boss_api = BossZhipinAPI()
interview_generator = InterviewQuestionGenerator()
offer_evaluator = OfferEvaluator()
rag_engine = RAGEngine()


class ChatRequest(BaseModel):
    user_input: str
    context: Optional[Dict[str, Any]] = None


class JobSearchRequest(BaseModel):
    keyword: str
    city: Optional[str] = ""
    page: Optional[int] = 1
    page_size: Optional[int] = 10


class InterviewQuestionRequest(BaseModel):
    job_type: str
    difficulty: Optional[str] = "medium"
    question_count: Optional[int] = 10


class OfferEvaluationRequest(BaseModel):
    offer_details: Dict[str, Any]
    user_profile: Optional[Dict[str, Any]] = None


class OfferCompareRequest(BaseModel):
    offers: List[Dict[str, Any]]


@app.get("/")
async def root():
    index_file = frontend_path / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {
        "message": "校招求职全流程多Agent协同智能助手",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/api/chat",
            "upload_resume": "/api/upload-resume",
            "search_jobs": "/api/search-jobs",
            "generate_interview_questions": "/api/generate-interview-questions",
            "evaluate_offer": "/api/evaluate-offer",
            "compare_offers": "/api/compare-offers",
            "rag_query": "/api/rag-query"
        }
    }


@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        result = workflow.run(request.user_input, request.context)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        if file.filename.endswith(".pdf"):
            result = pdf_parser.parse_pdf_with_structure(file_bytes=contents)
        else:
            text = contents.decode("utf-8")
            result = {"text": text, "pages": [], "tables": []}
        return {
            "success": True,
            "filename": file.filename,
            "content": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/search-jobs")
async def search_jobs(request: JobSearchRequest):
    try:
        jobs = boss_api.search_jobs(
            keyword=request.keyword,
            city=request.city,
            page=request.page,
            page_size=request.page_size
        )
        return {
            "success": True,
            "jobs": jobs
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/job-detail/{job_id}")
async def get_job_detail(job_id: str):
    try:
        job_detail = boss_api.get_job_detail(job_id)
        if not job_detail:
            raise HTTPException(status_code=404, detail="Job not found")
        return {
            "success": True,
            "job_detail": job_detail
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate-interview-questions")
async def generate_interview_questions(request: InterviewQuestionRequest):
    try:
        questions = interview_generator.generate_questions(
            job_type=request.job_type,
            difficulty=request.difficulty,
            question_count=request.question_count
        )
        return {
            "success": True,
            "questions": questions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/evaluate-offer")
async def evaluate_offer(request: OfferEvaluationRequest):
    try:
        evaluation = offer_evaluator.evaluate_offer(
            offer_details=request.offer_details,
            user_profile=request.user_profile
        )
        return {
            "success": True,
            "evaluation": evaluation
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/compare-offers")
async def compare_offers(request: OfferCompareRequest):
    try:
        comparison = offer_evaluator.compare_offers(offers=request.offers)
        return {
            "success": True,
            "comparison": comparison
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/rag-query")
async def rag_query(request: ChatRequest):
    try:
        result = rag_engine.query(request.user_input)
        return {
            "success": True,
            **result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
