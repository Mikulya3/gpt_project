from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os


def generate_pdf(data, output_path):
    environment = Environment(loader=FileSystemLoader("app/templates"))
    report = environment.get_template("template.html")

    logo_path = os.path.abspath("app/static/images/logo1.jpg")

    html_content = report.render(
        name=data["student_profile"]["name"],
        personal_info=data["personal_letter"],
        academic_reflection=data["academic_reflection"],
        financial_guidance=data["financial_guidance"],
        career_from_hobbies=data["career_from_hobbies"],
        final_summary=data["final_summary"],
        logo_path=logo_path,
        for_pdf=True,
    )

    HTML(string=html_content).write_pdf(output_path)
    return output_path