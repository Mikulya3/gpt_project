from app.database import Base, engine
from sqlalchemy import Column, Integer, Text,Boolean, String, ForeignKey, Float, DateTime 
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True)
    email = Column(String(50), unique=True)
    password = Column(Text, nullable=True)
    is_staff = Column(Boolean, default=False)
    
    user_response = relationship('User_Response', back_populates='owner')

    def __repr__(self):
        return f"<User {self.username}>"


class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, index=True)
    user_id = Column(Integer)


class User_Response(Base):
    __tablename__ = 'user_response'

    owner_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    submission_time = Column(DateTime)
    ip_address = Column(String)
    student_name = Column(String)
    grade_level = Column(String)
    gender = Column(String)
    openness = Column(String, index=True, default="Openness: You are willing to try new things")
    conscientiousness = Column(String, index=True, default="Conscientiousness: You desire to be cautious and diligent")
    agreeableness = Column(String, index=True, default="Agreeableness: You are good at interacting with people")
    neuroticism = Column(String, index=True, default="Neuroticism: You tend to experience negative emotions")
    mbti_result = Column(String, index=True, default="请选择您的MBTI （迈尔斯-布里格斯性格分类法）结果")
    has_college_major_choice = Column(Boolean, index=True, default="是否已经对大学专业有明确的选择? Do you have a clear choice of college major?")
    chosen_major = Column(String, index=True, default="请说明您选择的专业Please specify your chosen major")
    favorite_high_school_subjects = Column(String, index=True, default="高中最喜欢的科目(可填写多个，用逗号分隔)Favorite high school subjects (could be more than one, seperated by comma)")
    weight_high_school_subjects = Column(Integer, index=True, default="专业选择中对于高中喜欢的学科的在意程度 Weight")
    favorite_extracurricular_activities = Column(String, index=True, default="喜欢的课外活动（按项目列出，用逗号分隔）Favorite extracurricular activities")
    extracurricular_activities_weight = Column(Float, index=True, default="专业选择中对于高中喜欢的课外活动的在意程度 Weight")
    future_career_preference = Column(String, index=True, default="是否有未来职业偏好（职业目标）Is there any future career preference (career goal)")
    existing_future_career_preferences = Column(String, index=True, default="请说明现有未来职业偏好Please indicate existing future career preferences")
    future_career_preference_weight = Column(Float, index=True, default="专业选择中对于未来职业的在意程度 Weight")
    interested_subject_areas = Column(String, index=True, default="偏好的学科范围(可多选)Your most interested subject areas (multiple choice)")
    hobbies = Column(String, index=True, default="爱好（可以填写多个，用逗号分隔）Hobbies（could be more than one, seperated by comma)")
    hobbies_weight = Column(Float, index=True, default="专业选择中对于爱好的在意程度 Weight")
    subject_strengths_high_school = Column(String, index=True, default="高中优势学科（可多选）Subject strengths in High school (multiple choice)")
    elaborate_other = Column(String, index=True, default="请说明其他")
    subject_strengths_weight = Column(Float, index=True, default="专业选择中对于高中强势学科的在意程度 Weight")
    award_winning_competitions = Column(Boolean, index=True, default="是否有获奖比赛 Is there any award-winning competitions")
    award_details = Column(String, index=True, default="请说明获奖的学科和奖项名称Please state the discipline and name of the award")
    awards_weight = Column(Float, index=True, default="专业选择中对于已获得奖项的在意程度 Weight")
    other_academic_achievements = Column(String, index=True, default="其他学术成就（发表论文、证书等）Other academic achievements (published papers, certificates, etc.)")
    achievements_weight = Column(Float, index=True, default="专业选择中对于其他成就的在意程度 Weight")
    parents_resources = Column(String, index=True, default="父母可以提供的资源Resources that parents can provide")
    elaborate_parents_resources = Column(String, index=True, default='请说明其他 Please Elaborate "Other"')
    resources_weight = Column(Float, index=True, default="专业选择中对于父母可提供的资源的在意程度 Weight")
    post_graduation_plan = Column(String, index=True, default="本科毕业去向Plan after undergraduate graduation")
    post_graduation_plan_weight = Column(Float, index=True, default="本科专业选择中对于本科后毕业去向的在意程度 Weight")
    expected_annual_income = Column(Float, index=True, default="预期年收入(美元)Expected annual income range (USD)")
    income_weight = Column(Float, index=True, default="专业选择中对于预期年收入的在意程度 Weight")
    career_prospects_preference = Column(Boolean,index=True, default="是否有对职业前景的偏好Is there a preference for career prospects")
    career_prospects_details = Column(String, index=True, default="请说明现有职业前景偏好Please indicate existing preferences for career prospects")
    career_prospects_weight = Column(Float, index=True, default="专业选择中对于未来职业前景偏好的在意程度 Weight")
    financial_difficulties = Column(Boolean, index=True, default="是否有济困难 Are there any financial difficulties")
    expected_annual_tuition = Column(Float, index=True, default="预期年度学费和生活费范围(美元)Expected annual tuition and living expenses range (USD)")
    preferred_study_countries = Column(String, index=True, default="列出你希望的本科学习的国家（可以填写多个，用逗号分隔）List the countries you wish to study for your undergraduate degree（could be more than one, seperated by comma")
    country_weight = Column(Float, index=True, default="专业选择中对于大学所在国家的在意程度 Weight")
    other_considerations = Column(String, index=True, default="请列出其他考虑或要求（可选）Please list any other considerations or requirements (optional)")
    engineering_school = Column(Integer, index=True, default="请在工程学院的以下专业中选择你的偏好Please choose your preferences of the following majors in Engineering School—Computer Science 计算机科学")
    electrical_engineering = Column(Integer, index=True, default="Electrical Engineering 电子工程")
    mechanical_engineering = Column(Integer, index=True, default="Mechanical Engineering 机械工程")
    data_science = Column(Integer, index=True, default="Data Science and Data Engineering 数据科学与工程")
    civil_and_enviroment_engineering = Column(Integer, index=True, default="Civil and Environmental Engineering 土木与环境工程")
    aerospace_engineering = Column(Integer,index=True, default="Aerospace Engineering 航空航天工程")
    biomedical_engineering = Column(Integer, index=True, default="Biomedical Engineering 生物医学工程")
    chemical_engineering = Column(Integer, index=True, default="Chemical Engineering 化学工程")
    industry_engineering = Column(Integer, index=True, default="Industrial Engineering 工业工程")
    math = Column(Integer, index=True, default="请在理学院的以下专业中选择您喜欢的专业Please choose your preferences of the following majors in Science School—Math 数学")
    physics = Column(Integer, index=True, default="Physics 物理")
    chemistry = Column(Integer, index=True, default="Chemistry 化学")
    material_science = Column(Integer, index=True, default="Material Science 材料科学")
    biology = Column(Integer, index=True, default="Biology 生物")
    astronomy = Column(Integer, index=True, default="Astronomy 天文学")
    earth_science = Column(Integer, index=True, default="Earth Science 地球科学")
    social_science_economy = Column(Integer, index=True, default="Social Science—Economy 经济学")
    finance = Column(Integer, index=True, default="Finance 金融")
    sociology = Column(Integer, index=True, default="Sociology 社会学")
    political_science = Column(Integer, index=True, default="Political Science 政治科学")
    organization_management = Column(Integer, index=True, default="Organization management 组织管理")
    psychology = Column(Integer, index=True, default="Psychology 心理学")
    linguistics = Column(Integer, index=True, default="Linguistics 语言学")
    literature = Column(Integer, index=True, default="Literature 文学")
    art = Column(Integer, index=True, default="Art 艺术")
    music = Column(Integer, index=True, default="Music 音乐")
    anthropology = Column(Integer, index=True, default="Anthropology 人类学")
    archaeology = Column(Integer, index=True, default="Archaeology 考古学")
    philosophy = Column(Integer, index=True, default="Philosophy 哲学")
    history = Column(Integer, index=True, default="History 历史")
    gender_study = Column(Integer, index=True, default="Gender study 性别研究")
    culture_study = Column(Integer, index=True, default="Culture study 文化研究")
    choosing_major = Column(String, index=True, default="学生没有专业偏好或难以选择专业的最可能原因是The most likely reasons for students not having a major preference or having difficulty choosing a major are")
    total_score = Column(Integer, index=True, default="总分")
    
    owner = relationship('User', back_populates='user_response')


# Create database tables if they dont exist
User.metadata.create_all(bind=engine)


