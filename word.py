from openai import OpenAI
import pandas as pd
import yaml
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from datetime import datetime
import subprocess
import requests 
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib as mpl
import os,sys
from matplotlib.font_manager import FontProperties
import re
from wordcloud import WordCloud, STOPWORDS



openai = OpenAI()
app = FastAPI(title='gpt-4',)

# Load OpenAI API key from config file
def load_api_key():
    with open("config.yaml") as f:
        config_yaml = yaml.safe_load(f)
    return config_yaml['api_key']

openai.api_key=load_api_key()

# def get_words(file, name):
#     try:
#         df = pd.read_excel(file)
#         name_column = '学生拼音/英文姓名（例：Eric Zhang 或者 Runxin Zhang）Student Name (First Name + Last Name)'
#         dat =df[df[name_column]==name].astype(str)
#         data = dat.iloc[:, 6:79].astype(str)
#         print(data)
#         return data
#     except ValueError as e:
#         print('need inf')


# def word_cloud(data, file_path, font_path, name):
#     stopwords = set(STOPWORDS)
#     custom_words = ["非常同意", "同意", "适度", '强烈反对', '跳过', '是', '否', 'Yes', ' No', 'neutral', 'maybe','Agree', '非常同意 Strongly Agree', '强烈反对 Strongly disagree']
#     stopwords.update(word.lower() for word in custom_words)
#     stopwords.discard(name.lower()) 
#     text = ' '.join(data.astype(str).values.flatten())
#     text += (' ' + name) * 1000  
#     wc = WordCloud(
#         background_color='white',
#         width=1280,
#         height=1600,
#         stopwords=stopwords,
#         font_path=font_path,
#         prefer_horizontal=1.0,
#         collocations=False
#     ).generate(text)

#     plt.figure(figsize=(12.8, 16))
#     plt.imshow(wc, interpolation='bilinear')
#     plt.axis('off')
#     plt.savefig(file_path)
#     plt.close()
#     print(f"Word cloud image '{name}' created and saved to {file_path}")
    
# def main():
#     name = "Jake Li"
#     file_path=f"/home/hello/Desktop/{name}.png"
#     file= f"/home/hello/Desktop/new.xlsx"
#     font_path ='/home/hello/VScode/NotoSansSC-VariableFont_wght.ttf'
#     data = get_words(file, name)
#     word_cloud(data, file_path, font_path, name)


# if __name__=='__main__':
#     main()


def process_csv_and_generate_content(file, name):
    try:
        df = pd.read_excel(file)
        name_column = '学生拼音/英文姓名（例：Eric Zhang 或者 Runxin Zhang）Student Name (First Name + Last Name)'
        data = df[df[name_column] == name].astype(str)

        if data.empty:
            return None, None, None, None, None, None, None, None
        
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
def parse_generated_content(generated_visualization_score):
    lines = generated_visualization_score.strip().split("\n")
    scores_dict = {}
    
    for line in lines:
        if "：" in line:
            category, scores_str = line.split("：", 1)
            category = category.split("（")[0]

            scores = [int(score.strip("）").strip()) if score.strip("）").strip().isdigit() else 0 
                      for score in scores_str.split(',')]
            
            scores_dict[category] = scores
    return scores_dict

def create_spider_chart(scores_dict, font_path, filename="spider_chart.png"):
    categories = list(scores_dict.keys())
    num_vars = len(categories)

    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    # Load the font properties from the specified font file
    font_prop = FontProperties(fname=font_path)
    plt.rcParams['axes.unicode_minus'] = False

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    for category, values in scores_dict.items():
        if len(values) == num_vars - 1:
            values += values[:1]
        ax.plot(angles, values, linewidth=1, linestyle='solid', label=category)
        ax.fill(angles, values, alpha=0.25)

    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontproperties=font_prop)

    ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))

    plt.savefig(os.path.join("/home/hello/VScode", filename))
    plt.close()
    print(f"Saved: {os.path.join('/home/hello/VScode', filename)}")

def generate_gpt(data, name, basic_info, major_preferences, college_preferences, potential_major_exploration, column_AU):
    major_prompt_three = f"""请根据以下补充信息（被3个引号括起）继续从上述10个专业中进行第二步的3个最匹配专业的筛选。请给出推荐这三个专业的更详细的理由，理由需要要足够多的细节，证据和推理过程。理由都不能少于300字。请同时给出专业匹配度（0为最不匹配，100为最匹配）。请把三个专业分为三个自然段给出理由，匹配度需要在专业名称后面的括号内，每个自然段之间请加入空行'''{college_preferences}'''""" 
    
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

    Visualization_p1 = f"""
        1. 知识掌握程度（Knowledge Mastery）：这个维度可以通过测试或者评估来测量学生对于该学科的核心概念和技能的理解程度。这可能包括学生的课堂表现、作业、项目、测试和考试成绩。
        2. 热爱程度（Interest Level）：这个维度可以通过调查或者问卷来测量学生对于该学科的兴趣。这可能包括学生选择学习这个学科的频率、在这个学科上投入的时间、以及在这个学科上的自我激励程度。
        3. 实践应用能力（Practical Application）：这个维度可以通过评估学生对于该学科的实际应用能力。这可能包括学生在实验、项目或者实习中的表现，以及他们如何将学到的知识应用到实际问题中。
        4. 创新能力（Innovative Capability）：这个维度可以通过观察学生在该学科中的创新表现来测量。这可能包括他们是否能提出新的观点、解决问题的新方法、或者创作新的作品。
        5. 对未来的投入意愿（Future Commitment）：这个维度可以通过询问学生他们对于在这个学科上投入更多时间和精力的意愿来测量。这可能包括他们对于未来在这个领域内工作或者进一步学习的计划。
        请根据以下问卷结果对该学生的各个学科分别对相应的五个维度进行打分（0-5分），并以如下格式返回：'学科名称：分数,分数,分数,分数,分数'。每个学科的分数之间请加入空行，并确保使用中文学科名称。 use this related information。'''{potential_major_exploration}''' 请直接给出分数，不需要任何分析。参考格式为5,5,5,5,5；4,5,4,4,5；5,4,5,5,4；3,3,4,3,4。请在每个专业的分数之间加入空行 """
    Visualization_p2 = f"""请根据以下问卷结果对该学生的三个最推荐专业'''{major_list}'''分别对相应的五个维度进行打分（0-5分）：'''{basic_info},{major_preferences},{college_preferences} '''。请直接给出分数，不需要任何分析。参考格式为5,5,5,5,5；4,5,4,4,5；5,4,5,5,4；3,3,4,3,4。请在每个专业的分数之间加入空行 """

    gpt_input = f"{Visualization_p1}"
    chat_completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": gpt_input}],
        temperature=0.2,
        top_p=0.5,
        frequency_penalty=0.7,
        presence_penalty=0.0 
    )
    generated_visualization_score1 = chat_completion.choices[0].message.content
    print(generated_visualization_score1)
    gpt_input = f" {Visualization_p2}"
    chat_completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": gpt_input}],
        temperature=0.2,
        top_p=0.5,
        frequency_penalty=0.7,
        presence_penalty=0.0 
    )
    generated_visualization_score2 = chat_completion.choices[0].message.content
    print(generated_visualization_score2)

    return major_list,generated_visualization_score1,generated_visualization_score2

def main():
    name = "Elsa"
    # file_path=f"/home/hello/Desktop/{name}.png"
    file= f"/home/hello/Desktop/new.xlsx"
    word, data, name, basic_info, major_preferences, college_preferences, potential_major_exploration, column_AU = process_csv_and_generate_content(file, name)
    font_path ='/home/hello/VScode/NotoSansSC-VariableFont_wght.ttf'
    # data = get_words(file, name)
    # word_cloud(data, file_path, font_path, name)
    major_list,generated_visualization_score1,generated_visualization_score2 = generate_gpt(data, name, basic_info, major_preferences, college_preferences, potential_major_exploration, column_AU)
    scores_dict1 = parse_generated_content(generated_visualization_score1)
    scores_dict2 = parse_generated_content(generated_visualization_score2)
    create_spider_chart(scores_dict1, font_path,filename="spider_chart1.png")
    create_spider_chart(scores_dict2, font_path,filename="spider_chart2.png")  


if __name__=='__main__':
    main()