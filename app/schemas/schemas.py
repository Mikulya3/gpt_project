from pydantic import BaseModel, EmailStr, field_validator, Field, ConfigDict
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
   

class ResetPassword(BaseModel):
    token: str
    new_password: str
    confirm_password: str
    
    class Config:
        orm_mode = True 


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    is_staff: Optional[bool] = None


class UserResponseBase(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        extra="forbid"
    )
    student_name: str = Field(..., description="Your full name")  
    grade_level: str = Field(..., description="Example: freshman, sophomore, junior, senior") 
    gender: str 
    openness: str = Field(..., description="Openness: You are willing to try new things")
    conscientiousness: str = Field(..., description="Conscientiousness: You desire to be cautious and diligent")    
    agreeableness: str = Field(..., description="Agreeableness: You are good at interacting with people")
    neuroticism: str = Field(..., description="Neuroticism: You tend to experience negative emotions")
    mbti_result: int = Field(..., description="Please select your MBTI (Myers-Briggs Type Indicator) result")
    has_college_major_choice: bool = Field(..., description="Do you have a clear choice of college major?")
    chosen_major: str = Field(..., description="Please specify your chosen major")
    favorite_high_school_subjects: str = Field(..., description="Favorite high school subjects (could be more than one, separated by comma)")
    weight_high_school_subjects: int = Field(..., description="How much do you care about your favorite subjects in high school when choosing a major? Weight from 0 to 10")
    favorite_extracurricular_activities: str = Field(..., description="Favorite extracurricular activities")
    extracurricular_activities_weight: float = Field(..., description="How much do you care about your favorite extracurricular activities in high school when choosing a major? Weight from 0 to 10")
    future_career_preference: str = Field(..., description="What is your dream job or career path?")
    existing_future_career_preferences: str = Field(..., description="Do you have a future career in mind? If yes, which one?")
    future_career_preference_weight: float = Field(..., description="How much do you care about your future career when choosing a major? Weight from 0 to 10")
    interested_subject_areas: str = Field(..., description="Your most interested subject areas (multiple choice)")
    hobbies: str = Field(..., description="Hobbies (could be more than one, separated by comma)")
    hobbies_weight: float = Field(..., description="How much do you care about your hobbies when choosing a major? Weight from 0 to 10")
    subject_strengths_high_school: str = Field(..., description="Which school subjects are your strongest or favorite? (Choose all that apply)")
    elaborate_other: str = Field(..., description="Please describe other favorite subjects")
    subject_strengths_weight: float = Field(..., description="The degree of concern for high school strong subjects in major selection. Weight from 0 to 10")
    award_winning_competitions: bool = Field(..., description="Is there any award-winning competitions?")
    award_details: str = Field(..., description="Please state the discipline and name of the award")
    awards_weight: float = Field(..., description="How much do people care about awards they have received when choosing a major? Weight from 0 to 10")
    other_academic_achievements: str = Field(..., description="Other academic achievements (published papers, certificates, etc.)")
    achievements_weight: float = Field(..., description="The degree of importance attached to other achievements in choosing a major. Weight from 0 to 10")
    parents_resources: str = Field(..., description="Resources that parents can provide")
    elaborate_parents_resources: str = Field(..., description='Please Elaborate "internet, english courses, buy laptop and etc"')
    resources_weight: float = Field(..., description="The degree of concern about the resources that parents can provide when choosing a major. Weight from 0 to 10")
    post_graduation_plan: str = Field(..., description="Plan after undergraduate graduation")
    post_graduation_plan_weight: float = Field(..., description="How much do students care about their post-graduation career path when choosing their undergraduate major? Weight from 0 to 10")
    expected_annual_income: float = Field(..., description="Expected annual income range (USD)")
    income_weight: float = Field(..., description="How much do people care about expected annual income when choosing a major? Weight from 0 to 10")
    career_prospects_preference: bool = Field(..., description="Do you care about career prospects when choosing a major?")
    career_prospects_details: str = Field(..., description="Please describe your career prospects details")
    career_prospects_weight: float = Field(..., description="How much do you care about career prospects when choosing a major? Weight from 0 to 10")
    financial_difficulties: bool = Field(..., description="Are there any financial difficulties?")
    expected_annual_tuition: float = Field(..., description="Expected annual tuition fee (USD)")
    preferred_study_countries: str = Field(..., description="List the countries you wish to study for your undergraduate degree (could be more than one, separated by comma)")
    country_weight: float = Field(..., description="How much do you care about the country you study in when choosing a major? Weight from 0 to 10")
    other_considerations: str = Field(..., description="Other considerations when choosing a major")

    # Engineering
    engineering_school: int = Field(..., description="Interest in engineering school (0-10)")
    electrical_engineering: int = Field(..., description="Interest in electrical engineering (0-10)")
    mechanical_engineering: int = Field(..., description="Interest in mechanical engineering (0-10)")
    data_science: int = Field(..., description="Interest in data science (0-10)")
    civil_and_environment_engineering: int = Field(..., description="Interest in civil and environmental engineering (0-10)")
    aerospace_engineering: int = Field(..., description="Interest in aerospace engineering (0-10)")
    biomedical_engineering: int = Field(..., description="Interest in biomedical engineering (0-10)")
    chemical_engineering: int = Field(..., description="Interest in chemical engineering (0-10)")
    industry_engineering: int = Field(..., description="Interest in industrial engineering (0-10)")

    # Science
    math: int = Field(..., description="Interest in math (0-10)")
    physics: int = Field(..., description="Interest in physics (0-10)")
    chemistry: int = Field(..., description="Interest in chemistry (0-10)")
    material_science: int = Field(..., description="Interest in material science (0-10)")
    biology: int = Field(..., description="Interest in biology (0-10)")
    astronomy: int = Field(..., description="Interest in astronomy (0-10)")
    earth_science: int = Field(..., description="Interest in earth science (0-10)")

    # Social sciences & humanities
    social_science_economy: int = Field(..., description="Interest in social science economy (0-10)")
    finance: int = Field(..., description="Interest in finance (0-10)")
    sociology: int = Field(..., description="Interest in sociology (0-10)")
    political_science: int = Field(..., description="Interest in political science (0-10)")
    organization_management: int = Field(..., description="Interest in organization management (0-10)")
    psychology: int = Field(..., description="Interest in psychology (0-10)")
    linguistics: int = Field(..., description="Interest in linguistics (0-10)")
    literature: int = Field(..., description="Interest in literature (0-10)")
    art: int = Field(..., description="Interest in art (0-10)")
    music: int = Field(..., description="Interest in music (0-10)")
    anthropology: int = Field(..., description="Interest in anthropology (0-10)")
    archaeology: int = Field(..., description="Interest in archaeology (0-10)")
    philosophy: int = Field(..., description="Interest in philosophy (0-10)")
    history: int = Field(..., description="Interest in history (0-10)")
    gender_study: int = Field(..., description="Interest in gender study (0-10)")
    culture_study: int = Field(..., description="Interest in culture study (0-10)")
    choosing_major: str = Field(..., description="The most likely reasons for students not having a major preference or having difficulty choosing a major are")

    submission_time: Optional[datetime] = None
    ip_address: Optional[str] = None
    owner_id: Optional[int] = None


class UserResponseCreate(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        extra="forbid"
    )

    student_name: str = Field(..., description="Your full name")
    grade_level: str = Field(..., description="Example: freshman, sophomore, junior, senior")
    gender: str
    openness: str = Field(..., description="Openness: You are willing to try new things")
    conscientiousness: str = Field(..., description="Conscientiousness: You desire to be cautious and diligent")
    agreeableness: str = Field(..., description="Agreeableness: You are good at interacting with people")
    neuroticism: str = Field(..., description="Neuroticism: You tend to experience negative emotions")
    mbti_result: int = Field(..., description="Please select your MBTI (Myers-Briggs Type Indicator) result")
    has_college_major_choice: bool = Field(..., description="Do you have a clear choice of college major?")
    chosen_major: str = Field(..., description="Please specify your chosen major")
    favorite_high_school_subjects: str = Field(..., description="Favorite high school subjects (could be more than one, separated by comma)")
    weight_high_school_subjects: int = Field(..., description="How much do you care about your favorite subjects in high school when choosing a major? Weight from 0 to 10")
    favorite_extracurricular_activities: str = Field(..., description="List the activities you do outside of class that you enjoy most. This could be sports, music, clubs, volunteering, or any hobbies you actively participate in.")
    extracurricular_activities_weight: float = Field(..., description="How much do you care about your favorite extracurricular activities in high school when choosing a major? Weight from 0 to 10")
    future_career_preference: str = Field(..., description="What is your dream job or career path?")
    existing_future_career_preferences: str = Field(..., description="Do you have a future career in mind? If yes, which one?")
    future_career_preference_weight: float = Field(..., description="How much do you care about your future career when choosing a major? Weight from 0 to 10")
    interested_subject_areas: str = Field(..., description="Your most interested subject areas (multiple choice)")
    hobbies: str = Field(..., description="Hobbies (could be more than one, separated by comma)")
    hobbies_weight: float = Field(..., description="How much do you care about your hobbies when choosing a major? Weight from 0 to 10")
    subject_strengths_high_school: str = Field(..., description="Which school subjects are your strongest or favorite? (Choose all that apply)")
    elaborate_other: str = Field(..., description="Please describe other favorite subjects")
    subject_strengths_weight: float = Field(..., description="The degree of concern for high school strong subjects in major selection. Weight from 0 to 10")
    award_winning_competitions: bool = Field(..., description="Is there any award-winning competitions?")
    award_details: str = Field(..., description="Please state the discipline and name of the award")
    awards_weight: float = Field(..., description="How much do people care about awards they have received when choosing a major? Weight from 0 to 10")
    other_academic_achievements: str = Field(..., description="Other academic achievements (published papers, certificates, etc.)")
    achievements_weight: float = Field(..., description="The degree of importance attached to other achievements in choosing a major. Weight from 0 to 10")
    parents_resources: str = Field(..., description="Resources that parents can provide")
    elaborate_parents_resources: str = Field(..., description="Please Elaborate \"internet, english courses, buy laptop and etc\"")
    resources_weight: float = Field(..., description="The degree of concern about the resources that parents can provide when choosing a major. Weight from 0 to 10")
    post_graduation_plan: str = Field(..., description="Plan after undergraduate graduation")
    post_graduation_plan_weight: float = Field(..., description="How much do students care about their post-graduation career path when choosing their undergraduate major? Weight from 0 to 10")
    expected_annual_income: float = Field(..., description="Expected annual income range (USD)")
    income_weight: float = Field(..., description="How much do people care about expected annual income when choosing a major? Weight from 0 to 10")
    career_prospects_preference: bool = Field(..., description="Do you care about career prospects when choosing a major?")
    career_prospects_details: str = Field(..., description="Please describe your career prospects details")
    career_prospects_weight: float = Field(..., description="How much do you care about career prospects when choosing a major? Weight from 0 to 10")
    financial_difficulties: bool = Field(..., description="Are there any financial difficulties?")
    expected_annual_tuition: float = Field(..., description="Expected annual tuition fee (USD)")
    preferred_study_countries: str = Field(..., description="List the countries you wish to study for your undergraduate degree (could be more than one, separated by comma)")
    country_weight: int = Field(..., description="How much do you care about the country you study in when choosing a major? Weight from 0 to 10")
    other_considerations: str = Field(..., description="Other considerations when choosing a major")

    # Engineering
    engineering_school: int = Field(..., description="Interest in engineering school (0-10)")
    electrical_engineering: int = Field(..., description="Interest in electrical engineering (0-10)")
    mechanical_engineering: int = Field(..., description="Interest in mechanical engineering (0-10)")
    data_science: int = Field(..., description="Interest in data science (0-10)")
    civil_and_environment_engineering: int = Field(..., description="Interest in civil and environmental engineering (0-10)")
    aerospace_engineering: int = Field(..., description="Interest in aerospace engineering (0-10)")
    biomedical_engineering: int = Field(..., description="Interest in biomedical engineering (0-10)")
    chemical_engineering: int = Field(..., description="Interest in chemical engineering (0-10)")
    industry_engineering: int = Field(..., description="Interest in industrial engineering (0-10)")

    # Science
    math: int = Field(..., description="Interest in math (0-10)")
    physics: int = Field(..., description="Interest in physics (0-10)")
    chemistry: int = Field(..., description="Interest in chemistry (0-10)")
    material_science: int = Field(..., description="Interest in material science (0-10)")
    biology: int = Field(..., description="Interest in biology (0-10)")
    astronomy: int = Field(..., description="Interest in astronomy (0-10)")
    earth_science: int = Field(..., description="Interest in earth science (0-10)")

    # Social sciences & humanities
    social_science_economy: int = Field(..., description="Interest in social science economy (0-10)")
    finance: int = Field(..., description="Interest in finance (0-10)")
    sociology: int = Field(..., description="Interest in sociology (0-10)")
    political_science: int = Field(..., description="Interest in political science (0-10)")
    organization_management: int = Field(..., description="Interest in organization management (0-10)")
    psychology: int = Field(..., description="Interest in psychology (0-10)")
    linguistics: int = Field(..., description="Interest in linguistics (0-10)")
    literature: int = Field(..., description="Interest in literature (0-10)")
    art: int = Field(..., description="Interest in art (0-10)")
    music: int = Field(..., description="Interest in music (0-10)")
    anthropology: int = Field(..., description="Interest in anthropology (0-10)")
    archaeology: int = Field(..., description="Interest in archaeology (0-10)")
    philosophy: int = Field(..., description="Interest in philosophy (0-10)")
    history: int = Field(..., description="Interest in history (0-10)")
    gender_study: int = Field(..., description="Interest in gender study (0-10)")
    culture_study: int = Field(..., description="Interest in culture study (0-10)")
    choosing_major: str = Field(..., description="The most likely reasons for students not having a major preference or having difficulty choosing a major are")
