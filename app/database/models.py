from app.database.db import Base    
from sqlalchemy import Column, Integer, Text,Boolean, String, ForeignKey, Float, DateTime 
from sqlalchemy.orm import relationship
from datetime import datetime


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True)
    email = Column(String(50), unique=True)
    password = Column(String, nullable=True)
    is_staff = Column(Boolean, default=False)
    
    user_response = relationship('User_Response', back_populates='owner')

    def __repr__(self):
        return f"<User {self.username}>"



class User_Response(Base):
    __tablename__ = 'user_responses'

    owner_id = Column(Integer, ForeignKey("users.id"), primary_key=True)  
    submission_time = Column(DateTime, default=datetime.now, nullable=False) 
    ip_address = Column(String, nullable=True)
    student_name = Column(String)
    grade_level = Column(String)
    gender = Column(String)
    openness = Column(String, index=True, comment="Openness: You are willing to try new things")
    conscientiousness = Column(String, index=True, comment="Conscientiousness: You desire to be cautious and diligent")
    agreeableness = Column(String, index=True, comment="Agreeableness: You are good at interacting with people")
    neuroticism = Column(String, index=True, comment="Neuroticism: You tend to experience negative emotions")
    mbti_result = Column(String, index=True, comment="Please select your MBTI (Myers-Briggs Type Indicator) result")
    has_college_major_choice = Column(Boolean, index=True, comment="Do you have a clear choice of college major?")
    chosen_major = Column(String, index=True, comment="lease specify your chosen major")
    favorite_high_school_subjects = Column(String, index=True, comment="Favorite high school subjects (could be more than one, seperated by comma)")
    weight_high_school_subjects = Column(Integer, index=True, comment="How much do you care about your favorite subjects in high school when choosing a major? Weight")
    favorite_extracurricular_activities = Column(String, index=True, comment="Favorite extracurricular activities")
    extracurricular_activities_weight = Column(Float, index=True, comment="How much do you care about your favorite extracurricular activities in high school when choosing a major? Weight")
    future_career_preference = Column(String, index=True, comment="Is there any future career preference (career goal)")
    existing_future_career_preferences = Column(String, index=True, comment="Please indicate existing future career preferences")
    future_career_preference_weight = Column(Float, index=True, comment="How much do you care about your future career when choosing a major? Weight")
    interested_subject_areas = Column(String, index=True, comment="Your most interested subject areas (multiple choice)")
    hobbies = Column(String, index=True, comment="Hobbies（could be more than one, seperated by comma)")
    hobbies_weight = Column(Float, index=True, comment="How much do you care about your hobbies when choosing a major? Weight")
    subject_strengths_high_school = Column(String, index=True, comment="Subject strengths in High school (multiple choice)")
    elaborate_other = Column(String, index=True, comment="Please describe other")
    subject_strengths_weight = Column(Float, index=True, comment="The degree of concern for high school strong subjects in major selection. Weight")
    award_winning_competitions = Column(Boolean, index=True, comment="Is there any award-winning competitions")
    award_details = Column(String, index=True, comment="Please state the discipline and name of the award")
    awards_weight = Column(Float, index=True, comment="How much do people care about awards they have received when choosing a major? Weight")
    other_academic_achievements = Column(String, index=True, comment="Other academic achievements (published papers, certificates, etc.)")
    achievements_weight = Column(Float, index=True, comment="The degree of importance attached to other achievements in choosing a major, Weight")
    parents_resources = Column(String, index=True, comment="Resources that parents can provide")
    elaborate_parents_resources = Column(String, index=True, comment='Please Elaborate "Other"')
    resources_weight = Column(Float, index=True, comment="The degree of concern about the resources that parents can provide when choosing a major.Weight")
    post_graduation_plan = Column(String, index=True, comment="Plan after undergraduate graduation")
    post_graduation_plan_weight = Column(Float, index=True, comment="How much do students care about their post-graduation career path when choosing their undergraduate major? Weight")
    expected_annual_income = Column(Float, index=True, comment="Expected annual income range (USD)")
    income_weight = Column(Float, index=True, comment="How much do people care about expected annual income when choosing a major? Weight")
    career_prospects_preference = Column(Boolean, index=True, comment="Is there a preference for career prospects")
    career_prospects_details = Column(String, index=True, comment="Please indicate existing preferences for career prospects")
    career_prospects_weight = Column(Float, index=True, comment="The degree of concern about future career prospects when choosing a major, Weight")
    financial_difficulties = Column(Boolean, index=True, comment="Are there any financial difficulties")
    expected_annual_tuition = Column(Float, index=True, comment="Expected annual tuition and living expenses range (USD)")
    preferred_study_countries = Column(String, index=True, comment="List the countries you wish to study for your undergraduate degree（could be more than one, seperated by comma")
    country_weight = Column(Float, index=True, comment="How much do students care about the country where the university is located when choosing a major? Weight")
    other_considerations = Column(String, index=True, comment="Please list any other considerations or requirements (optional)")
    engineering_school = Column(Integer, index=True, comment="Please choose your preferences of the following majors in Engineering School—Computer Science 计算机科学")
    electrical_engineering = Column(Integer, index=True, comment="Electrical Engineering")
    mechanical_engineering = Column(Integer, index=True, comment="Mechanical Engineering")
    data_science = Column(Integer, index=True, comment="Data Science and Data Engineering")
    civil_and_enviroment_engineering = Column(Integer, index=True, comment="Civil and Environmental Engineering")
    aerospace_engineering = Column(Integer, index=True, comment="Aerospace Engineering")
    biomedical_engineering = Column(Integer, index=True, comment="Biomedical Engineering")
    chemical_engineering = Column(Integer, index=True, comment="Chemical Engineering")
    industry_engineering = Column(Integer, index=True, comment="Industrial Engineering")
    math = Column(Integer, index=True, comment="Please choose your preferences of the following majors in Science School—Math 数学")
    physics = Column(Integer, index=True, comment="Physics")
    chemistry = Column(Integer, index=True, comment="Chemistry")
    material_science = Column(Integer, index=True, comment="Material Science")
    biology = Column(Integer, index=True, comment="Biology")
    astronomy = Column(Integer, index=True, comment="Astronomy")
    earth_science = Column(Integer, index=True, comment="Earth Science")
    social_science_economy = Column(Integer, index=True, comment="Social Science Economy")
    finance = Column(Integer, index=True, comment="Finance")
    sociology = Column(Integer, index=True, comment="Sociology")
    political_science = Column(Integer, index=True, comment="Political Science")
    organization_management = Column(Integer, index=True, comment="Organization management")
    psychology = Column(Integer, index=True, comment="Psychology")
    linguistics = Column(Integer, index=True, comment="Linguistics")
    literature = Column(Integer, index=True, comment="Literature")
    art = Column(Integer, index=True, comment="Art")
    music = Column(Integer, index=True, comment="Music")
    anthropology = Column(Integer, index=True, comment="Anthropology")
    archaeology = Column(Integer, index=True, comment="Archaeology")
    philosophy = Column(Integer, index=True, comment="Philosophy")
    history = Column(Integer, index=True, comment="History")
    gender_study = Column(Integer, index=True, comment="Gender study")
    culture_study = Column(Integer, index=True, comment="Culture study")
    choosing_major = Column(String, index=True, comment="The most likely reasons for students not having a major preference or having difficulty choosing a major are")
    total_score = Column(Integer, index=True, comment="Total score")
    owner = relationship('User', back_populates='user_response') 



