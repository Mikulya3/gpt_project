from fastapi import FastAPI, status, Depends, HTTPException
from app.database.models import Base
from app.database.db import engine
from fastapi.middleware.cors import CORSMiddleware
from app.api_router.user_router import user_router
from app.api_router.user_response_router import response_router 
from app.api_router.pdf_router import pdf_router
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from prometheus_fastapi_instrumentator import Instrumentator





app = FastAPI(title='GPT4')
Base.metadata.create_all(bind=engine)
app.include_router(user_router)
app.include_router(response_router)
app.include_router(pdf_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", status_code=status.HTTP_200_OK)
def read_root():
    return {"message": "OK"}


Instrumentator().instrument(app).expose(app)



# Route to render the HTML
# @app.get("/report", response_class=HTMLResponse)
# def get_report(request: Request):
#     return templates.TemplateResponse("template.html", {
#         "request": request,
#         "name": "Meerim",
#         "personal_letter": "Your personal letter goes here...",
#         "academic_reflection": "Some reflections...",
#         "financial_guidance": "Advice about money...",
#         "career_from_hobbies": "How your hobbies can shape your career...",
#         "final_summary": "Summary of your future"
#     })

# import os
# from fastapi.responses import FileResponse
# from app.services.pdf_generator import generate_pdf 
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# @app.get("/generate-pdf")
# def generate_pdf_endpoint():
#     logo_path = os.path.join(BASE_DIR, "static", "logo1.jpg")
#     test_data = {
#         "student_profile": {"name": "Meerim"},
#         "personal_letter": "Hi, I'm Meerim. I love clean code and security.",
#         "academic_reflection": "My academic strength is in logical problem-solving.",
#         "financial_guidance": "Consider scholarships and budget planning.",
#         "career_from_hobbies": "Your interest in structure suits backend & security.",
#         "final_summary": "You are ready for roles in backend or DevSecOps.",
#         "logo_path": logo_path, 
#         "for_pdf": False
#     }
    
#     output_path = "app/generated_reports/test_report.pdf"
#     generate_pdf(test_data, output_path)

#     return FileResponse(
#         output_path,
#         media_type="application/pdf",
#         filename="MerAI_Report.pdf"
#     )