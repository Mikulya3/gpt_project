import uuid
from app.celery_app import celery_app
from app.services.pdf_generator import generate_pdf
import os

@celery_app.task(name="app.tasks.pdf.generate_pdf_task")
def generate_pdf_task(data: dict):
    reports_dir = "/app/generated_reports"
    os.makedirs(reports_dir, exist_ok=True)

    filename = f"{data['student_profile']['name'].replace(' ', '_')}_{uuid.uuid4().hex[:6]}.pdf"
    output_path = os.path.join(reports_dir, filename)

    generate_pdf(data, output_path)

    return {
        "pdf_url": f"/reports/{filename}"   
    }