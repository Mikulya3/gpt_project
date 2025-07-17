from app.database.db import Base    
from sqlalchemy import Column, Integer, Text,Boolean, String, ForeignKey, Float, DateTime 
from sqlalchemy.orm import relationship
from datetime import datetime


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    is_staff = Column(Boolean, default=False)
    
    user_response = relationship('User_Response', back_populates='owner')

    def __repr__(self):
        return f"<User {self.username}>"


class User_Response(Base):
    __tablename__ = "user_responses"

    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String, index=True)
    grade_level = Column(String, index=True)
    gender = Column(String, index=True)
    openness = Column(String, index=True)
    conscientiousness = Column(String, index=True)
    agreeableness = Column(String, index=True)
    neuroticism = Column(String, index=True)
    mbti_result = Column(Integer, index=True)
    has_college_major_choice = Column(Boolean, index=True)
    chosen_major = Column(String, index=True)
    favorite_high_school_subjects = Column(String, index=True)
    weight_high_school_subjects = Column(Integer, index=True)
    favorite_extracurricular_activities = Column(String, index=True)
    extracurricular_activities_weight = Column(Float, index=True)
    future_career_preference = Column(String, index=True)
    existing_future_career_preferences = Column(String, index=True)
    future_career_preference_weight = Column(Float, index=True)
    interested_subject_areas = Column(String, index=True)
    hobbies = Column(String, index=True)
    hobbies_weight = Column(Float, index=True)
    subject_strengths_high_school = Column(String, index=True)
    elaborate_other = Column(String, index=True)
    subject_strengths_weight = Column(Float, index=True)
    award_winning_competitions = Column(Boolean, index=True)
    award_details = Column(String, index=True)
    awards_weight = Column(Float, index=True)
    other_academic_achievements = Column(String, index=True)
    achievements_weight = Column(Float, index=True)
    parents_resources = Column(String, index=True)
    elaborate_parents_resources = Column(String, index=True)
    resources_weight = Column(Float, index=True)
    post_graduation_plan = Column(String, index=True)
    post_graduation_plan_weight = Column(Float, index=True)
    expected_annual_income = Column(Float, index=True)
    income_weight = Column(Float, index=True)
    career_prospects_preference = Column(Boolean, index=True)
    career_prospects_details = Column(String, index=True)
    career_prospects_weight = Column(Float, index=True)
    financial_difficulties = Column(Boolean, index=True)
    expected_annual_tuition = Column(Float, index=True)
    preferred_study_countries = Column(String, index=True)
    country_weight = Column(Integer, index=True)
    other_considerations = Column(String, index=True)

    engineering_school = Column(Integer, index=True)
    electrical_engineering = Column(Integer, index=True)
    mechanical_engineering = Column(Integer, index=True)
    data_science = Column(Integer, index=True)
    civil_and_environment_engineering = Column(Integer, index=True)
    aerospace_engineering = Column(Integer, index=True)
    biomedical_engineering = Column(Integer, index=True)
    chemical_engineering = Column(Integer, index=True)
    industry_engineering = Column(Integer, index=True)

    math = Column(Integer, index=True)
    physics = Column(Integer, index=True)
    chemistry = Column(Integer, index=True)
    material_science = Column(Integer, index=True)
    biology = Column(Integer, index=True)
    astronomy = Column(Integer, index=True)
    earth_science = Column(Integer, index=True)

    social_science_economy = Column(Integer, index=True)
    finance = Column(Integer, index=True)
    sociology = Column(Integer, index=True)
    political_science = Column(Integer, index=True)
    organization_management = Column(Integer, index=True)
    psychology = Column(Integer, index=True)
    linguistics = Column(Integer, index=True)
    literature = Column(Integer, index=True)
    art = Column(Integer, index=True)
    music = Column(Integer, index=True)
    anthropology = Column(Integer, index=True)
    archaeology = Column(Integer, index=True)
    philosophy = Column(Integer, index=True)
    history = Column(Integer, index=True)
    gender_study = Column(Integer, index=True)
    culture_study = Column(Integer, index=True)

    choosing_major = Column(String, index=True)

    ip_address = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="user_response")




