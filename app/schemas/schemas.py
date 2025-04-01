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
    submission_time: Optional[datetime] = None
    ip_address: Optional[str] = None  
    owner_id: Optional[int] = None          
    
    class Config:
        orm_mode = True


