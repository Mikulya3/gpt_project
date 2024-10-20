from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    username:str
    email:str
    password:str
    
    class Config:
        orm_mode=True
    
    
    
class LoginUser(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True
        use_enum_values = True

class UserResponseBase(BaseModel):
    student_name: str
    grade_level: str
    gender: str
    openness: str
    conscientiousness: str
    agreeableness: str
    neuroticism: str
    mbti_result: int
    has_college_major_choice: bool
    chosen_major: str
    favorite_high_school_subjects: str
    weight_high_school_subjects: int
    favorite_extracurricular_activities: str
    extracurricular_activity_weight: int
    favorite_career_choices: str
    career_weight: int
    favorite_subjects: str
    subject_weight: int
    additional_comments: str
    economics: int
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

class UserResponseCreate(UserResponseBase):
    submission_time:datetime
    ip_address: str
    
class UserResponse(UserResponseBase):
    owner_id: int
    submission_time:datetime
    ip_address: str
    
    class Config:
        orm_mode=True