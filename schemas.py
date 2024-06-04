from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import yaml 

def load_config():
    with open('config.yaml', 'r') as file:
        config = load_config(file)
        return config
        
config = load_config()
jwt_secret_key=config['jwt_secret_key']


class User(UserBase):
    id: int
    user_response: List['UserResponse'] = []

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    email: str
    auth_jwt_key: str = jwt_secret_key

class UserCreate(UserBase):
    password: str
    is_staff: Optional[bool] = False

class UserLogin(UserBase):
    password: str



class User_Response(User_ResponseBase):
    id:int
    user_id:int

    class Config:
        orm_mode = True

class UserResponseBase(BaseModel):
    submission_time: Optional[datetime]
    ip_address: Optional[str]
    student_name: Optional[str]
    grade_level: Optional[str]
    gender: Optional[str]
    openness: Optional[str]
    conscientiousness: Optional[str]
    agreeableness: Optional[str]
    neuroticism: Optional[str]
    mbti_result: Optional[str]
    has_college_major_choice: Optional[bool]
    chosen_major: Optional[str]
    favorite_high_school_subjects: Optional[str]
    weight_high_school_subjects: Optional[int]
    favorite_extracurricular_activities: Optional[str]
    extracurricular_activity_weight: Optional[int]
    favorite_career_choices: Optional[str]
    career_weight: Optional[int]
    favorite_subjects: Optional[str]
    subject_weight: Optional[int]
    additional_comments: Optional[str]
    economics: Optional[int]
    sociology: Optional[int]
    political_science: Optional[int]
    organization_management: Optional[int]
    psychology: Optional[int]
    linguistics: Optional[int]
    literature: Optional[int]
    art: Optional[int]
    music: Optional[int]
    anthropology: Optional[int]
    archaeology: Optional[int]
    philosophy: Optional[int]
    history: Optional[int]
    gender_study: Optional[int]
    culture_study: Optional[int]
    choosing_major: Optional[str]
    total_score: Optional[int]