from pydantic import BaseModel, EmailStr,  field_validator
from datetime import datetime
import re
from typing import Optional


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    
    class Config:
        from_attributes = True
                
                
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_staff: bool

    class Config:
        from_attributes = True

       
class LoginUser(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True
        use_enum_values = True


class ForgotPassword(BaseModel):
    email: EmailStr


class ChangePassword(BaseModel):
    old_password: str
    new_password: str
    
    class Congig:
        orm_mode = True
        

class ResetPassword(BaseModel):
    new_password: str
    confirm_password: str
    
    class Config:
        orm_mode = True 


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class UserResponseBase(BaseModel):
    student_name: str
    grade_level: str
    gender: str
    openness: str
    conscientiousness: str
    agreeableness: str
    neuroticism: str
    mbti_result: str
    has_college_major_choice: bool
    chosen_major: str
    favorite_high_school_subjects: str
    weight_high_school_subjects: int
    favorite_extracurricular_activities: str
    extracurricular_activities_weight: float
    future_career_preference: str
    existing_future_career_preferences: str
    future_career_preference_weight: float
    interested_subject_areas: str
    hobbies: str
    hobbies_weight: float
    subject_strengths_high_school: str
    elaborate_other: str
    subject_strengths_weight: float
    award_winning_competitions: bool
    award_details: str
    awards_weight: float
    other_academic_achievements: str
    achievements_weight: float
    parents_resources: str
    elaborate_parents_resources: str
    resources_weight: float
    post_graduation_plan: str
    post_graduation_plan_weight: float
    expected_annual_income: float
    income_weight: float
    career_prospects_preference: bool
    career_prospects_details: str
    career_prospects_weight: float
    financial_difficulties: bool
    expected_annual_tuition: float
    preferred_study_countries: str
    country_weight: float
    other_considerations: str

    # Engineering
    engineering_school: int
    electrical_engineering: int
    mechanical_engineering: int
    data_science: int
    civil_and_enviroment_engineering: int
    aerospace_engineering: int
    biomedical_engineering: int
    chemical_engineering: int
    industry_engineering: int

    # Science
    math: int
    physics: int
    chemistry: int
    material_science: int
    biology: int
    astronomy: int
    earth_science: int

    # Social sciences & humanities
    social_science_economy: int
    finance: int
    sociology: int
    political_science: int
    organization_management: int
    psychology: int
    linguistics: int
    literature: int
    art: int
    music: int
    anthropology: int
    archaeology: int
    philosophy: int
    history: int
    gender_study: int
    culture_study: int

    choosing_major: str
    total_score: int

    submission_time: Optional[datetime] = None
    ip_address: Optional[str] = None
    owner_id: Optional[int] = None

    class Config:
        orm_mode = True


class UserResponseCreate(BaseModel):
    student_name: str
    grade_level: str
    gender: str
    openness: str
    conscientiousness: str
    agreeableness: str
    neuroticism: str
    mbti_result: str
    has_college_major_choice: bool
    chosen_major: str
    favorite_high_school_subjects: str
    weight_high_school_subjects: int
    favorite_extracurricular_activities: str
    extracurricular_activities_weight: float
    future_career_preference: str
    existing_future_career_preferences: str
    future_career_preference_weight: float
    interested_subject_areas: str
    hobbies: str
    hobbies_weight: float
    subject_strengths_high_school: str
    elaborate_other: str
    subject_strengths_weight: float
    award_winning_competitions: bool
    award_details: str
    awards_weight: float
    other_academic_achievements: str
    achievements_weight: float
    parents_resources: str
    elaborate_parents_resources: str
    resources_weight: float
    post_graduation_plan: str
    post_graduation_plan_weight: float
    expected_annual_income: float
    income_weight: float
    career_prospects_preference: bool
    career_prospects_details: str
    career_prospects_weight: float
    financial_difficulties: bool
    expected_annual_tuition: float
    preferred_study_countries: str
    country_weight: float
    other_considerations: str

    # Engineering
    engineering_school: int
    electrical_engineering: int
    mechanical_engineering: int
    data_science: int
    civil_and_enviroment_engineering: int
    aerospace_engineering: int
    biomedical_engineering: int
    chemical_engineering: int
    industry_engineering: int

    # Science
    math: int
    physics: int
    chemistry: int
    material_science: int
    biology: int
    astronomy: int
    earth_science: int

    # Social Sciences & Humanities
    social_science_economy: int
    finance: int
    sociology: int
    political_science: int
    organization_management: int
    psychology: int
    linguistics: int
    literature: int
    art: int
    music: int
    anthropology: int
    archaeology: int
    philosophy: int
    history: int
    gender_study: int
    culture_study: int

    choosing_major: str

    class Config:
        orm_mode = True
        from_attributes = True
