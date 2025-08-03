import openai
from app.config import settings
from app.database.db import get_db
from app.database.models import User_Response
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
import json
from app.api_router.user_router import get_current_user


openai.api_key = settings.API_KEY


def call_gpt(prompt: str):
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        top_p=0.5,
        frequency_penalty=0.7,
        presence_penalty=0.0
    )
    return response.choices[0].message.content


def sorting_data(user_response: User_Response):
    if not user_response:
        raise HTTPException(status_code=404, detail="User not found") 
    context = {
        "student_profile": {
            "name": user_response.student_name,
            "grade": user_response.grade_level,
            "gender": user_response.gender,
            "ip_address": user_response.ip_address},
        "personality_traits": {
            "openness": user_response.openness,
            "conscientiousness": user_response.conscientiousness,
            "agreeableness": user_response.agreeableness,
            "neuroticism": user_response.neuroticism,
            "mbti_result": user_response.mbti_result
        }, 
        "academic_interests": {
            "favorite_high_school_subjects": user_response.favorite_high_school_subjects,
            "weight_high_school_subjects": user_response.weight_high_school_subjects,
            "subject_strengths_high_school": user_response.subject_strengths_high_school,
            "subject_strengths_weight": user_response.subject_strengths_weight,
            "awards": {
                "award_winning_competitions": user_response.award_winning_competitions,
                "award_details": user_response.award_details,
                "awards_weight": user_response.awards_weight,
                "other_academic_achievements": user_response.other_academic_achievements,
                "achievements_weight": user_response.achievements_weight}
        },
        "major_interests": {   
            # Engineering
            "engineering_school": user_response.engineering_school,
            "electrical_engineering": user_response.electrical_engineering,
            "mechanical_engineering": user_response.mechanical_engineering,
            "data_science": user_response.data_science,
            "civil_and_environment_engineering": user_response.civil_and_environment_engineering,
            "aerospace_engineering": user_response.aerospace_engineering,
            "biomedical_engineering": user_response.biomedical_engineering,
            "chemical_engineering": user_response.chemical_engineering,
            "industry_engineering": user_response.industry_engineering,

            # Science
            "math": user_response.math,
            "physics": user_response.physics,
            "chemistry": user_response.chemistry,
            "material_science": user_response.material_science,
            "biology": user_response.biology,
            "astronomy": user_response.astronomy,
            "earth_science": user_response.earth_science,

            # Social Sciences & Humanities
            "social_science_economy": user_response.social_science_economy,
            "finance": user_response.finance,
            "sociology": user_response.sociology,
            "political_science": user_response.political_science,
            "organization_management": user_response.organization_management,
            "psychology": user_response.psychology,
            "linguistics": user_response.linguistics,
            "literature": user_response.literature,
            "art": user_response.art,
            "music": user_response.music,
            "anthropology": user_response.anthropology,
            "archaeology": user_response.archaeology,
            "philosophy": user_response.philosophy,
            "history": user_response.history,
            "gender_study": user_response.gender_study,
            "culture_study": user_response.culture_study
}, 
        "career_and_future_aspirations": {
            "has_college_major_choice": user_response.has_college_major_choice,
            "chosen_major": user_response.chosen_major,
            "future_career_preference": user_response.future_career_preference,
            "existing_future_career_preferences": user_response.existing_future_career_preferences,
            "future_career_preference_weight": user_response.future_career_preference_weight,
            "post_graduation_plan": user_response.post_graduation_plan,
            "post_graduation_plan_weight": user_response.post_graduation_plan_weight,
            "expected_annual_income": user_response.expected_annual_income,
            "income_weight": user_response.income_weight,
             },
        "socioeconomic_and_financial_factors": {
            
            "parents_resources": user_response.parents_resources,
            "elaborate_parents_resources": user_response.elaborate_parents_resources,
            "resources_weight": user_response.resources_weight,
            "financial_difficulties": user_response.financial_difficulties,
            "expected_annual_tuition": user_response.expected_annual_tuition, 
            "preferred_study_countries": user_response.preferred_study_countries,
            "country_weight": user_response.country_weight,
            "other_considerations": user_response.other_considerations
        }, 
        "extracurriculars_and_hobbies": {
            "favorite_extracurricular_activities": user_response.favorite_extracurricular_activities,
            "extracurricular_activities_weight": user_response.extracurricular_activities_weight,
            "interested_subject_areas": user_response.interested_subject_areas,
            "hobbies": user_response.hobbies,
            "hobbies_weight": user_response.hobbies_weight,
            "elaborate_other": user_response.elaborate_other    
        },
        }
        
    return context


def built_prompts(context: dict):
    if not context:
        raise HTTPException(status_code=404, detail="Context not found")
    
    student_profile = context["student_profile"]
    personality_traits = context["personality_traits"]
    academic_interests = context["academic_interests"]
    major_interests = context["major_interests"]
    career_and_future_aspirations = context["career_and_future_aspirations"]
    socioeconomic_and_financial_factors = context["socioeconomic_and_financial_factors"]
    extracurriculars_and_hobbies = context["extracurriculars_and_hobbies"]

    personal_promt = f"""You are a wise and supportive elder. Based on a questionnaire submitted by the student named '''{student_profile["name"]}''', write a short, encouraging, and thoughtful letter.
Instructions:
- Use the **format of a personal letter**.
- Write in **second-person perspective** ("you").
- Do not exceed **500 words**.
- End the letter with: "Sincerely, MerAi".
The tone should be warm, respectful, and slightly philosophical — like a mentor guiding a young learner. Reflect on the student’s personality, academic interests, and future aspirations using the data below. Highlight their strengths, motivation, and potential.

Basic Info:
{json.dumps(student_profile, ensure_ascii=False, indent=4)}

Personality Traits:
{json.dumps(personality_traits, ensure_ascii=False, indent=4)}

Major Interests:
{json.dumps(major_interests, ensure_ascii=False, indent=4)}

Career Aspirations:
{json.dumps(career_and_future_aspirations, ensure_ascii=False, indent=4)}  
"""

    subject_interests_prompt = f"""
You are an experienced academic advisor and university counselor. Based on the academic background and their interests in various majors, write a thoughtful and inspiring narrative to help the student reflect on their educational path.
Speak directly to the student using the second person ("you"). Use a warm and supportive tone. Begin by acknowledging their academic strengths and interests, then explore how those align with potential college majors. The message should offer encouragement, insight, and personalized advice. Stay under 500 words.

Student's Academic Profile:
{json.dumps(academic_interests, ensure_ascii=False, indent=4)}

Student's Major Interests:
{json.dumps(major_interests, ensure_ascii=False, indent=4)}

Close your message with a sentence encouraging the student to keep exploring and growing.
"""

    socioeconomic_prompt = f"""
You are a university admissions and financial aid advisor.
Based on the student’s socioeconomic profile below, provide a thoughtful analysis (maximum 400 words) that helps guide them toward realistic and well-supported choices for studying abroad.
Speak directly to the student using the second person ("you").

The student has shared the following:
- Available resources from parents and family
- Detailed comments on family financial background
- Their personal assessment of financial difficulty
- Estimated annual tuition expectations
- Preferred countries for studying
- The importance (weight) they place on country selection
- Any other considerations they mentioned

Using this data:
1. Recommend 2–3 countries that best fit the student’s financial situation, support system, and preferences.
2. Briefly explain what kind of universities or programs in those countries might suit them (public vs private, scholarship availability, etc.).
3. Offer reassurance or guidance on balancing financial practicality with educational ambition.

Student’s Socioeconomic & Financial Profile:
{json.dumps(socioeconomic_and_financial_factors, ensure_ascii=False, indent=4)}

End your message with an encouraging tone, empowering the student to pursue their dreams with clarity and resourcefulness.
"""

    extracurriculars_prompt = f"""
You are a career advisor specializing in helping high school students connect their extracurricular activities and hobbies with future career paths.
A student has provided the following information about their favorite extracurricular activities, areas of interest, and personal hobbies. Your task is to write an encouraging, forward-looking message (under 400 words) that reflects on how these activities reveal the student’s strengths, preferences, and possible career inclinations.
Use second-person perspective ("you") and provide a few career directions or majors that align naturally with their interests. Be creative but realistic, and support your suggestions with reasoning based on the student’s actual responses.

Student’s Extracurricular and Hobby Profile:
{json.dumps(extracurriculars_and_hobbies, ensure_ascii=False, indent=4)}

End the message by encouraging the student to keep exploring their passions, as those often illuminate the best paths.
"""

    final_summary = f"""
You are a professional global education consultant with expertise in student profiling, university admissions, and scholarship advising.
Speak directly to the student using the second person ("you").
Based on all the following information about a student, provide a comprehensive final advisory summary (max 600 words). Your task is to help the student:

1. **Choose 3 best-fit universities** to apply to — based on MBTI, academic background, financial constraints, and preferred countries.
2. **Advise potential scholarship programs or financial aid options** in those countries.
3. **Recommend 3 additional universities** that the student may not have considered but are good alternatives.
4. **Identify areas of weakness** (academic or personal) and suggest online or offline **courses to improve those skills**.
5. Based on their overall personality, traits, interests, and achievements — **suggest 2 or 3 potential occupations or career paths** that align with their abilities and goals.

Be specific and encouraging. Avoid generic advice. Tailor all insights to the student's actual context, strengths, preferences, and constraints.".

Here is the student's information:
- Student Profile: {json.dumps(context['student_profile'], ensure_ascii=False)}
- Personality Traits & MBTI: {json.dumps(context['personality_traits'], ensure_ascii=False)}
- Academic Interests & Achievements: {json.dumps(context['academic_interests'], ensure_ascii=False)}
- Major Preferences: {json.dumps(context['major_interests'], ensure_ascii=False)}
- Financial and Socioeconomic Info: {json.dumps(context['socioeconomic_and_financial_factors'], ensure_ascii=False)}
- Extracurriculars & Hobbies: {json.dumps(context['extracurriculars_and_hobbies'], ensure_ascii=False)}

End the response with a warm, empowering message to the student, showing confidence in their future and motivating them to act on your guidance.  
Sign the message with: "Good Luck!".
"""

    gpt_prompts = {
        "personal_letter": personal_promt,
        "academic_reflection": subject_interests_prompt,
        "financial_guidance": socioeconomic_prompt,
        "career_from_hobbies": extracurriculars_prompt,
        "final_summary": final_summary
        }
    
    result = {
        key: call_gpt(prompt)
        for key, prompt in gpt_prompts.items()
        }
        
    return result

