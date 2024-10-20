import pandas as pd
import os
from shutil import copyfile
from datetime import datetime
import subprocess
import requests 
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib as mpl
from matplotlib.patches import Patch
import os,sys
from matplotlib.font_manager import FontProperties
font_path = 'SNsanafonGyou.ttf'
# font_prop = FontProperties(fname=font_path)
from wordcloud import WordCloud, STOPWORDS
import jieba
import random





def process_csv_and_generate_content(file_path_xlxs, name):
# This function reads an Excel file, filters the data to find a row matching the provided name,
    # and extracts various pieces of information from specific columns.

    
    try:
        df = pd.read_excel(file_path_xlxs)
        name_column = '学生拼音/英文姓名（例：Eric Zhang 或者 Runxin Zhang）Student Name (First Name + Last Name)'
        data = df[df[name_column] == name].astype(str)

        if data.empty:
            return None, "person not found", None, None, None, None, None, None
        words = data.iloc[:, 6:79].astype(str)
        basic_info = data.iloc[:, 6:10].astype(str)
        major_preferences = data.iloc[:, 14:37].astype(str)
        college_preferences = data.iloc[:, 37:49].astype(str)
        potential_major_exploration = data.iloc[:, 49:79].astype(str)
        column_AU = data.iloc[:, 46].astype(str)
        return words, data, name, basic_info, major_preferences, college_preferences, potential_major_exploration, column_AU
    except ValueError as e:
        print(f"Error reading the Excel file: {e}")
        return None, None, None, None, None, None, None, None

def word_cloud(words, file_path, font_path, name):
    # Creating png file for the title list, where we are focusing on the name in the middle of the picture
    stopwords = set(STOPWORDS)
    custom_words = ["非常同意", "同意", "适度", '强烈反对', '跳过', '是', '否', 'Yes', ' No', 'neutral', 'maybe','Agree', '非常同意 Strongly Agree', 'disagree','强烈反对 Strongly disagree']
    stopwords.update(word.lower() for word in custom_words)
    stopwords.discard(name.lower()) 
    text = ' '.join(words.astype(str).values.flatten())
    text += (' ' + name) * 1000  
    wc = WordCloud(
        background_color='white',
        width=9000,
        height=6500,
        stopwords=stopwords,
        font_path=font_path,
        prefer_horizontal=1.0,
        collocations=False
    ).generate(text)

    plt.figure(figsize=(9, 6.5), dpi=300)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(file_path)
    plt.close()
    print(f"Word cloud image '{name}' created and saved to {file_path}")
    return file_path

# working over the spider chart creation. charts perform major direction of the student using information which chat gpt filtered from the whole database
def parse_generated_content(generated_visualization_score1,generated_visualization_score2):
    lines = generated_visualization_score1.strip().split('\n')+generated_visualization_score2.strip().split("\n")
    scores_dict = {}
    for line in lines:
        if "：" in line:
            category, scores_str = line.split("：", 1)
            category = category.split("（")[0]
            scores = []
            for score in scores_str.split(','):
                score_clean = score.strip("）").strip()
                if score_clean:
                    try:
                        scores.append(int(score_clean))
                    except ValueError:
                        print(f"Non-integer score encountered: '{score}'")
                        scores.append(0)
                else:
                    scores.append(0)
            if category in scores_dict and scores_dict[category]:
                scores_dict[category].extend(scores)
            else:
                scores_dict[category] = scores
    return scores_dict
    print(scores_dict) 

    # Save the plot to a file
    file_name = os.path.join("/home/hello/VScode", filename)
    plt.savefig(file_name)
    plt.close()
    print(f"Saved: {file_name}")


        
def generate_gpt(data, name, basic_info, major_preferences, college_preferences, potential_major_exploration, column_AU):
# here generating response using chat gpt APIkey 
    
    firstpage_summary = f""" 你的角色是一位长者。根据学生'''{name}'''提供的问卷(被3个引号括起），重新书写出一段故事性的总结，请使用信件的格式，请使用第二人称，落款为ChatIvy，不要超过500字。请与以下例子中的风格保持一致:“同学你好，在本次测试中，我看到了一位。。。;你是智慧博学的研究员，你有着永不枯竭的好奇心，强大的逻辑和异于常人的洞察力，求知欲更是驱使你站到了探索未知的第一线。理性的你注重逻辑分析，擅长抽象思考，时刻准备找出真理”: '''{name},{basic_info}, {major_preferences}, {college_preferences}''' """
    major_prompt_one = f""" 你是一位拥有多年教育经验的顶级留学咨询师，你尤其擅长了解学生的特点并进行基于基础数据的推荐。接下来你的任务是帮助我根据一份高中生的问卷为这位高中生推荐出最适合他的专业，你需要给出详细的理由并在每个中用理由到问卷里的细节信息，你同时需要给出足够的推理过程。在问卷中，学生会对每一个问题或因素进行权重的判断，不同的权重代表了这个因素在专业选择中得重要性(0表示一点都不重要，5表示非常重要)，请结合这些权重的数字给出最终推荐。你的具体任务分为两步。第一步是根据标为原始信息的信息为这位学生推荐10个最适合他的专业并给出理由。第二步是根据标为补充信息的信息从未这位学生推荐的10个最适合他的专业中筛选出3个专业并给出理由和这些专业与他的匹配度。最终结果我希望拥有一个含有10个推荐专业和理由，3个最适合专业和理由文档，每个理由都不能少于300字。当你准备好了，我就把这位学生的信息发给你。generate on the chinese language"""
    major_prompt_two = f""" 请根据以下问卷信息为用户进行第一步10个专业的推荐，在推荐的过程中请注重学生给出对于每个因素的权重。每个推荐理由不能少于300字. 每个推荐专业之间请用空行隔开，并形成序号列表'''{name},{basic_info},{major_preferences}''' """
    major_prompt_three = f"""请根据以下补充信息（被3个引号括起）继续从上述10个专业中进行第二步的3个最匹配专业的筛选。请给出推荐这三个专业的更详细的理由，理由需要要足够多的细节，证据和推理过程。理由都不能少于300字。请同时给出专业匹配度（0为最不匹配，100为最匹配）。请把三个专业分为三个自然段给出理由，匹配度需要在专业名称后面的括号内，每个自然段之间请加入空行'''{college_preferences}'''""" 

    gpt_input = f"{firstpage_summary}"
    chat_completion = openai.chat.completions.create(
    model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": gpt_input}],
        temperature=0.2,
        top_p=0.5,
        frequency_penalty=0.7,
        presence_penalty=0.0 
    )
    generated_summary=chat_completion.choices[0].message.content
    print("done1")

    gpt_input = f"{major_prompt_one},{major_prompt_two},{data}"
    # print(gpt_input)
    chat_completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": gpt_input}],
        temperature=0.2,
        top_p=0.5,
        frequency_penalty=0.7,
        presence_penalty=0.0 
    )
    generated_major_prompt_two = chat_completion.choices[0].message.content
    print("done2")

    gpt_input = f"{major_prompt_three}"
    chat_completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": gpt_input}],
        temperature=0.2,
        top_p=0.5,
        frequency_penalty=0.7,
        presence_penalty=0.0 
    )
    generated_major_prompt_three = chat_completion.choices[0].message.content
    print("done3")

    major_prompt_four =f"""请列出上个回答中推荐的三个专业的中文名称: use this information'''{generated_major_prompt_three}''' , 三个专业的分数之间加入空行 """
    
    gpt_input = f"{major_prompt_four}"
    chat_completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": gpt_input}],
        temperature=0.2,
        top_p=0.5,
        frequency_penalty=0.7,
        presence_penalty=0.0 
    )
    major_list = chat_completion.choices[0].message.content
    print('done4')


    
    potential_major = f"""1. 学习难度：一些专业可能涉及很高的学习难度，例如需要深入理解复杂的理论和概念，或者需要掌握一系列复杂的技术和技能。
        2. 实践机会：一些专业可能没有足够的实践机会，导致学生可能在理论和实践应用之间缺乏联系。
        3. 职业前景：一些专业可能缺乏明确或广泛的职业前景，导致学生可能在毕业后难以找到相关工作。
        4. 竞争压力：一些专业可能存在很高的竞争压力，例如一些热门的专业可能会有大量的学生竞争有限的就业机会。
        5. 专业要求：一些专业可能有严格的课程要求或学分要求，导致学生在满足这些要求的同时，可能无法有足够的时间和机会去探索自己的兴趣和潜力。
        6. 工作压力：一些专业可能会导致高压力的工作，例如医学、法律或金融等领域的工作常常需要在高压下工作，并需要长时间的工作。
        7. 对经济环境或政策的依赖：一些专业可能会受到经济环境或政策变化的影响，这可能会影响到这个专业的就业市场和工资水平。例如，金融或能源相关的专业就可能会受到全球经济或能源政策的影响。
        8. 快速变化的行业环境：一些专业可能会面临快速变化的行业环境，例如科技或媒体相关的专业，学生需要能够持续学习和更新自己的知识和技能。
        你现在模仿的是大学中的顾问
        请根据上述8个维度分别给出以下三个专业的缺点：'''{major_list}'''。每个维度都需要列出，如果在这个维度上没有明显缺点，请直接说明。
        请尽量详细和细节化并给出足够的证据和例子。每一点均不要少于3句话。请尝试在描述中加入个人感受，以更感性化的风格写出缺点。请在每一点的理由后均加入详细的例子，并将理由加长并变得更细节。请将每个专业的8个纬度用空行分开，将专业名称单独一行作为标题，每个专业的八个维度都变为从1-8的序号列表。"""

    # potential major
    gpt_input = f"{potential_major}"
    chat_completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": gpt_input}],
        temperature=0.2,
        top_p=0.5,
        frequency_penalty=0.7,
        presence_penalty=0.0 
    )
    generated_potential_major = chat_completion.choices[0].message.content
    print("done5")



    Correspondence_college_recommendations = f"""学生希望未来到'''{column_AU}'''各个国家读大学本科，可能专业为 '''{major_list}'''；请你为用户推荐这几个国家中每个国家里三个专业分别的具有代表性的两所大学并给出详细的推荐理由，每个推荐理由不少于300字。请将3个专业以序号列表形式呈现，再给出每个专业中用户希望去的国家推荐的两所大学。每个国家每个专业的两所大学推荐以列表形式呈现。"""
    Correspondence_Courses = f"""假设你给该用户推荐的最适合的三个专业分别是'''{major_list}'''，请分别列出该专业在本科阶段的7个基础课程以及3个进阶课程名称（中英文双语）上面的中英文双语请以如此格式展示：专业名 (major name)；课程名(class name)。"""
    Major_development_history = f"""请列出以下三个专业过去50年历史中的每个专业5个最重要的转折点及其时间与影响：'''{major_list}'''。每个转折点及其影响的描述不能少于200字。请在每个转折点与下一个转折点中加入空行。请在每个专业月下一个专业之间加入空行。"""
    Cutting_edge_field = f"""请列出以下三个专业每个专业学术界的3个最前沿领域和工业界的3个最前沿领域：'''{major_list}'''。请详细描述每个领域，每个领域的描述均不能少于200字。请在每个领域与领域中加入空行。请在每个专业月下一个专业之间加入空行。"""

    # Visualization_p1 = f"""
    #     1. 知识掌握程度（Knowledge Mastery）：这个维度可以通过测试或者评估来测量学生对于该学科的核心概念和技能的理解程度。这可能包括学生的课堂表现、作业、项目、测试和考试成绩。
    #     2. 热爱程度（Interest Level）：这个维度可以通过调查或者问卷来测量学生对于该学科的兴趣。这可能包括学生选择学习这个学科的频率、在这个学科上投入的时间、以及在这个学科上的自我激励程度。
    #     3. 实践应用能力（Practical Application）：这个维度可以通过评估学生对于该学科的实际应用能力。这可能包括学生在实验、项目或者实习中的表现，以及他们如何将学到的知识应用到实际问题中。
    #     4. 创新能力（Innovative Capability）：这个维度可以通过观察学生在该学科中的创新表现来测量。这可能包括他们是否能提出新的观点、解决问题的新方法、或者创作新的作品。
    #     5. 对未来的投入意愿（Future Commitment）：这个维度可以通过询问学生他们对于在这个学科上投入更多时间和精力的意愿来测量。这可能包括他们对于未来在这个领域内工作或者进一步学习的计划。
    #     请根据以下问卷结果对该学生的各个学科分别对相应的五个维度进行打分（0-5分），并以如下格式返回：'学科名称：分数,分数,分数,分数,分数'。每个学科的分数之间请加入空行，并确保使用中文学科名称。 use this related information。'''{potential_major_exploration}''' 请直接给出分数，不需要任何分析。参考格式为5,5,5,5,5；4,5,4,4,5；5,4,5,5,4；3,3,4,3,4。请在每个专业的分数之间加入空行 """
    # Visualization_p2 = f"""请根据以下问卷结果对该学生的三个最推荐专业'''{major_list}'''分别对相应的五个维度进行打分（0-5分）：'''{basic_info},{major_preferences},{college_preferences} '''。请直接给出分数，不需要任何分析。参考格式为5,5,5,5,5；4,5,4,4,5；5,4,5,5,4；3,3,4,3,4。请在每个专业的分数之间加入空行 """
    Visualization_p3 = f"""请参考以下括号内段落的格式与内容和该用户的问卷信息，为用户的推荐专业'''{major_list}'''以及它们所对应的五大维度‘知识掌握程度’，‘热爱程度’，‘实践实用能力‘，‘创新能力‘，‘对未来的投入意愿‘，写一个深度分析分析并给出一段话的总结。
    (运动医学： 
    - 知识掌握程度：Eva在高中阶段对生物科学有着较高的兴趣和优势，这将有助于她在运动医学领域掌握相关的生物学知识。此外，她在自然科学学科范围中的强势学科为生物，这意味着她在生物学方面可能已经有一定的知识基础。因此，Eva在运动医学领域的知识掌握程度可能较高，得分为4。 
    - 热爱程度：Eva在未来职业偏好中明确表示了从事与运动医学相关的领域，这表明她对该专业有较高的热爱程度。此外，她在喜欢的课外活动中包括排球，这也与运动医学的相关性相符。因此，Eva在运动医学领域的热爱程度可能较高，得分为5。 
    - 实践应用能力：运动医学强调对运动损伤和康复的实际应用，Eva在未来职业偏好中表明希望从事与运动康复相关的工作，这表明她对实践应用能力有较高的需求和意愿。此外，她在排球、戏剧和篮球等活动中可能培养了一定的运动康复实践能力。因此，Eva在运动医学领域的实践应用能力可能较高，得分为4。 
    - 创新能力：运动医学领域需要不断探索新的治疗方法和康复技术，而Eva在高中阶段的文学爱好可能有助于培养她的创新能力。尽管创新能力在运动医学中并非最为重要的特征，但她可能在研究和实践中展现一定的创新潜力。因此，Eva在运动医学领域的创新能力可能较高，得分为3。 
    - 对未来的投入意愿：Eva在未来职业偏好中明确表示了对从事与运动医学和运动康复相关的领域有兴趣，这表明她对该领域有较高的投入意愿。她的家庭还提供经济支持，这可能为她在学习和实践中提供一定的资源和机会。因此，Eva在运动医学领域的对未来的投入意愿可能较高，得分为4。  
    综合考虑，根据Eva在不同学科的兴趣和五大维度的评估，推荐专业包括运动医学、康复科学和生物科学。在这些领域，Eva表现出较高的兴趣和匹配程度。她在生物学方面有较好的知识掌握程度和热爱程度，对于实践应用能力和未来投入意愿也表现出较高的需求和意愿。对于创新能力，Eva在这些学科中可能需要进一步培养和锻炼。建议Eva在选择专业时综合考虑自己的兴趣和综合能力，对未来职业规划有明确的认识，以做出最适合自己的决策。）"""

    Highschool_activities = f"""你现在的角色是一名资深的大学顾问。 请根据以下括号内段落的风格内容格式，为该高中生规划大学申请的活动。他的目标专业分别为：'''{major_list}'''。 活动规划框架为： 一周以内的活动(参观，讲座），一个月以内的活动（夏校，读书，小型研究，coursera课程），一年以内的活动（科研，实习，志愿者），以及背景提升的规划（主打科研和open-ended project-based learning，现实免费资源和付费资源） 
    请给出有创造性,独特性的活动规划。每一个活动的细节与信息不能少于300字。请讲一周内的活动，一个月内的活动，一年内的活动，背景提升的规划4部分内容用空行隔开，并将一周内的活动，一个月内的活动，一年内的活动，背景提升的规划变为标题。请在每个专业月下一个专业之间加入空行。
    (1. 运动科学(Kinesiology)：
    一周以内：在一周之内，你可以组织一次校内运动科学小型研讨会。邀请校内的体育爱 好者、健身教练和相关专业的学生参加。你可以邀请一位运动科学领域的教授或专家进 行讲座，探讨热门话题如运动与健康的关系，新兴的运动训练方法等。通过这个独特的 活动，你将展示自己的组织能力、领导力，并为同学们带来有价值的学习机会。
    一个月以内：在一个月内，你可以参与一个在线社交平台上的科学普及活动。你可以制 作短视频或撰写博文，介绍一些有趣的科学实验或运动原理。这样的活动将帮助你将运 动科学知识传播给更广大的受众，同时锻炼你的科学沟通能力。你还可以邀请其他研究 生或教授合作，共同打造一个有趣而有深度的科普系列。
    一年以内：在一年内，你可以组织一个大型的运动科学实验活动。你可以合作建立一个 临时的体能测试中心，邀请学生和社区居民参与。你可以设计各种测试项目，如心肺功 能测试、肌肉力量测试等，为参与者提供个性化的健康建议。通过这个活动，你将锻炼 项目管理、团队协作和数据分析的能力，同时服务社区，传播健康理念。 
    背景提升规划：除了参与学术和实践活动外，你还可以考虑策划一个创新性的"运动科学 展览"。你可以利用虚拟现实技术，打造一个沉浸式的展览环境，让参观者可以亲身体验 不同类型的运动和其对身体的影响。你可以合作设计师、程序员和医学专家，共同创造 一个有趣而富有教育价值的展览，以展示运动科学的魅力。 
    2. 生物科学(Biology)： 
    一周以内：在一周之内，你可以发起一个校内的生态探索活动。邀请同学们一起前往附 近的自然保护区或野外地区，进行一次生物多样性调查。你可以带领大家观察不同种类 的植物和动物，记录它们的分布和行为。通过这个活动，你将培养同学们的野外观察技 能，提升他们对生态系统的认识。 
    一个月以内：在一个月内，你可以启动一个“生物故事收集计划”。邀请周围的人们，包 括老人、农民、渔民等，分享他们与自然界的互动经历和传统知识。你可以采访他们， 记录这些有趣的生物观察和传说，然后将它们整理成书籍、博客或短片。通过这个计 划，你将传承当地的生物文化，弘扬生物科学的价值。 
    一年以内：在一年内，你可以发起一个“城市生态恢复计划”。与同学们合作，选择校园 或社区中的一个受损生态环境，如荒地或污染区，然后设计并实施一个生态恢复方案。 你可以种植适应性植物、引入天敌，同时监测环境变化。通过这个项目，你将锻炼项目 管理和环境保护技能，同时为城市生态的改善做出贡献。 
    背景提升规划：除了学术和实践活动外，你可以考虑参与一个“生物文化交流计划”。你 可以申请前往其他国家或地区，与当地的生物学家、民间艺术家和社区领袖合作，了解 他们的生物文化传统。你可以学习当地的野外观察方法、草药医学、传统故事等，以拓 展你的生物科学视野。将这些经验与你的专业知识相结合，创造出独特的研究或项目。 
    3. 物理治疗(Physical Therapy)： 
    一周以内：在一周之内，你可以组织一个“康复运动体验日”。邀请社区居民，特别是有 运动损伤或慢性疾病的人，参加一个轻松愉快的户外活动。你可以设计一系列简单的康 复性运动，如伸展、平衡训练和轻度有氧运动。通过这个活动，你将帮助参与者体验到 物理治疗的积极影响，同时提升他们的健康意识。 
    一个月以内：在一个月内，你可以发起一个“康复科普绘本创作项目”。与艺术学生合 作，创作一本有趣的绘本，介绍康复治疗的基本原理和方法。你可以选择一些常见的康 复案例，将科学知识用富有创意的故事和插画呈现出来。这本绘本可以用于儿童医院、 康复中心等地，帮助患者和家庭了解康复治疗。 
    一年以内：在一年内，你可以合作开发一个“虚拟康复实验室”。利用虚拟现实技术，创 造一个虚拟环境，模拟各种康复训练场景。用户可以通过VR头盔体验不同类型的运动、 平衡和康复训练，同时在虚拟环境中接受专业指导。这个项目将结合技术和康复实践， 为患者提供创新的康复体验。 
    背景提升规划：除了参与常规的实习和研究活动外，你可以考虑创办一个“社区康复支持 小组”。你可以定期组织康复知识分享会，为社区居民提供康复建议和指导。你还可以与 社区体育俱乐部合作，提供定制的康复训练方案。通过这个支持小组，你将深化对患者 需求的了解，同时提升你的康复咨询和沟通技能。)
    """

    Correspondence_college_recommendations
    gpt_input = f"{Correspondence_college_recommendations}"
    chat_completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": gpt_input}],
        temperature=0.2,
        top_p=0.5,
        frequency_penalty=0.7,
        presence_penalty=0.0 
    )
    generated_Correspondence_college_recommendations = chat_completion.choices[0].message.content
    print('done6')

    Correspondence_Courses
    gpt_input = f"{Correspondence_Courses}"
    chat_completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": gpt_input}],
        temperature=0.2,
        top_p=0.5,
        frequency_penalty=0.7,
        presence_penalty=0.0 
    )
    generated_Correspondence_Courses = chat_completion.choices[0].message.content
    print('done7')


    Major_development_history
    gpt_input = f"{Major_development_history}"
    chat_completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": gpt_input}],
        temperature=0.2,
        top_p=0.5,
        frequency_penalty=0.7,
        presence_penalty=0.0 
    )
    generated_Major_development_history = chat_completion.choices[0].message.content
    print('done8')

    # Cutting_edge_field
    gpt_input = f"{Cutting_edge_field}"
    chat_completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": gpt_input}],
        temperature=0.2,
        top_p=0.5,
        frequency_penalty=0.7,
        presence_penalty=0.0 
    )
    generated_Cutting_edge_field = chat_completion.choices[0].message.content
    print('done9')


    # gpt_input = f"{Visualization_p1}"
    # chat_completion = openai.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[{"role": "user", "content": gpt_input}],
    #     temperature=0.2,
    #     top_p=0.5,
    #     frequency_penalty=0.7,
    #     presence_penalty=0.0 
    # )
    # generated_visualization_score1 = chat_completion.choices[0].message.content
    # print(generated_visualization_score1 )

    # gpt_input = f" {Visualization_p2}"
    # chat_completion = openai.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[{"role": "user", "content": gpt_input}],
    #     temperature=0.2,
    #     top_p=0.5,
    #     frequency_penalty=0.7,
    #     presence_penalty=0.0 
    # )
    # generated_visualization_score2 = chat_completion.choices[0].message.content
    # print(generated_visualization_score2)

    gpt_input = f"{Visualization_p3}"
    chat_completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": gpt_input}],
        temperature=0.2,
        top_p=0.5,
        frequency_penalty=0.7,
        presence_penalty=0.0 
    )
    generated_visualization_p3 = chat_completion.choices[0].message.content
    print('done12')

    # Highschool_activities
    gpt_input = f"{Highschool_activities}"
    chat_completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": gpt_input}],
        temperature=0.2,
        top_p=0.5,
        frequency_penalty=0.7,
        presence_penalty=0.0 
    )
    generated_Highschool_activities = chat_completion.choices[0].message.content
    print("done13")
   
    return generated_summary,generated_major_prompt_two, generated_major_prompt_three, major_list, generated_potential_major, generated_Correspondence_college_recommendations , generated_Correspondence_Courses, generated_Major_development_history, generated_Cutting_edge_field ,generated_visualization_p3, generated_Highschool_activities

@app.get("/generate_pdf")
def main():
# here generating pdf report in latex. open file and insert neccesary output of the responce to the latex prepared template 
    file_path_xlsx = '/home/hello/Desktop/new.xlsx'
    name = 'Yicheng Xu'
   
    words, data, name, basic_info, major_preferences, college_preferences, potential_major_exploration, column_AU = process_csv_and_generate_content(file_path_xlsx,name)
    generated_summary,generated_major_prompt_two, generated_major_prompt_three, major_list, generated_potential_major, generated_Correspondence_college_recommendations , generated_Correspondence_Courses, generated_Major_development_history, generated_Cutting_edge_field ,generated_visualization_p3, generated_Highschool_activities=generate_gpt(data, name, basic_info, major_preferences, college_preferences, potential_major_exploration, column_AU) 
    # major_list,generated_visualization_score1,generated_visualization_score2 = generate_gpt(data,name,basic_info,major_preferences,college_preferences,potential_major_exploration,column_AU) 
    font_path ='/home/hello/VScode/NotoSansSC-VariableFont_wght.ttf'
    file_path = f"/home/hello/VScode/{name}.png"
    file_path = word_cloud(data, file_path, font_path, name)
    scores_dict=parse_generated_content(generated_visualization_score1,generated_visualization_score2)  
    template_path = "/home/hello/VScode/pro[2].tex"
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S") 
    pdf_path = f"/home/hello/VScode/ChatIvy专业匹配报告_{name}.tex"
    # if generated_visualization_score1 and generated_visualization_score2:
    #     scores_dict1 = parse_generated_content(generated_visualization_score1)
    #     preprocess_scores(scores_dict, expected_labels)

    #     scores_dict2 = parse_generated_content(generated_visualization_score2)
    #     preprocess_scores(scores_dict, expected_labels)

    copyfile(template_path,pdf_path)
    with open(pdf_path, 'r') as file:
        template_content = file.read()

    final_content = template_content.replace("%name_%", name)
    final_content = final_content.replace("image", file_path)
    final_content = final_content.replace("%generated_summary_%", generated_summary)
    final_content = final_content.replace("%generated_major_prompt_two_%", generated_major_prompt_two)
    final_content = final_content.replace("%generated_major_prompt_three_%", generated_major_prompt_three)
    final_content = final_content.replace("%major_list_%", major_list)
    final_content = final_content.replace("%generated_potential_major_%", generated_potential_major)
    final_content = final_content.replace("%generated_Correspondence_college_recommendations_%", generated_Correspondence_college_recommendations)
    final_content = final_content.replace("%generated_Correspondence_Courses_%", generated_Correspondence_Courses)
    final_content = final_content.replace("%generated_Major_development_history_%", generated_Major_development_history)
    final_content = final_content.replace("%generated_Cutting_edge_field_%", generated_Cutting_edge_field)
    final_content = final_content.replace("%generated_visualization_p3_%", generated_visualization_p3)
    final_content = final_content.replace("%generated_Highschool_activities_%", generated_Highschool_activities)
    
    with open(pdf_path, 'w') as file:
        file.write(final_content)

    try:
        result = subprocess.run(['pdflatex', pdf_path], cwd="/home/hello/VScode", check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("PDF generated")
    except subprocess.CalledProcessError as e:
        print("Failed to generate PDF:", e)
    
    # os.remove(pdf_path)
@app.on_event("startup")
async def startup_event():
    main()
    
