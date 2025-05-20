import os
import random
from konlpy.tag import Okt
import json

from config import settings

# 형태소 분석기 준비
okt = Okt()

# 동의어 사전
synonym_dict = {
    "deep learning": "딥러닝",
    "deeplearning": "딥러닝",
    "machine learning": "머신러닝",
    "머신 러닝": "머신러닝",
    "tensorflow": "TensorFlow",
    "scikit learn": "Scikit-learn",
    "문제 해결":"문제해결",
    "목표 의식":"목표의식",
    "성취 감":"성취감",
    "공감 능력":"공감능력",
    "논리적사고":"논리적 사고",
    "자기 개발":"자기개발",
    "목표설정":"목표 설정",
    "자료 조사":"자료조사",
    "비판적사고":"비판적 사고",
    "강한의지":"강한 의지",
    "시간엄수":"시간 엄수",
    "업무우선순위설정":"업무 우선순위 설정",
    "업무우선순위 설정":"업무 우선순위 설정",
    "업무 우선순위설정":"업무 우선순위 설정",
    "의사 소통":"의사소통",
    "경험 중심":"경험중심",
    "실천 중심":"실천중심",
    "상황판단력":"상황 판단력",
    "디테일집중":"디테일 집중",
    "결과도출":"결과 도출",
    "환경적응력":"환경 적응력",
}

# 불용어
stopwords = ["열심히", "최선을 다해", "항상", "끊임없이", "노력하는", "좋은", "많은", "다양한", "계속해서", "보통", 
    "자주", "충분히", "어느 정도", "그냥", "당연히", "보이게", "잘", "흔히", "약간", "적당히", 
    "적극적으로", "정말", "진짜", "굉장히", "매우", "상당히", "무조건", "계속", "가끔", "대부분", 
    "자연스럽게", "비교적", "상시로", "항상처럼", "가능한", "되도록", "일단", "어느 날", "종종", "어쩌다", 
    "이러한", "그러한", "다소", "어떤", "이런", "저런", "특별히", "대충", "대략", "간혹", 
    "몰라도", "잘 모르지만", "생각합니다", "느꼈습니다", "같습니다"]

def normalize_text(text):
    # 소문자화 + 동의어 치환
    text = text.lower()
    for synonym, standard in synonym_dict.items():
        text = text.replace(synonym, standard.lower())
    return text

def evaluate_answer(answer,job):
    skills = []
    beds = []
    file_path = os.path.join(settings.BASE_DIR, 'static', 'AI개발데이터', f'skillList_{job}.json')
    print("Trying to load:", file_path)
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for skill_group in data['SkillList']:
            for skill in skill_group['Skill']:
                skills.append(skill['Skill_Name'])
    with open(os.path.join(settings.BASE_DIR, 'static', 'AI개발데이터', f'skillList_공통.json'), 'r', encoding='utf-8') as f:
        data = json.load(f)
        for skill in data['all_skillList']:
                skills.append(skill)
        
    with open(os.path.join(settings.BASE_DIR, 'static', 'ban_word.json'), 'r', encoding='utf-8') as f:
        data = json.load(f)
        for bed in data['bed']:
                beds.append(bed)
    # 전처리
    answer = normalize_text(answer)
    
    # 형태소 분석
    tokens = okt.morphs(answer)
    # 불용어 제거
    tokens = [token for token in tokens if token not in stopwords]

    # 소문자화 (영문 스킬 대응)
    tokens_lower = [token.lower() for token in tokens]

    # 평가
    matched_skills = set()
    matched_beds = set()
    for skill in skills:
        if skill.lower() in tokens_lower:
            matched_skills.add(skill)
        elif skill.lower() in answer:
            matched_skills.add(skill)
    for bed in beds:
        if bed.lower() in tokens_lower:
            matched_beds.add(bed)
    # 점수 계산 (비율 + 출현 빈도)
    skill_score = (len(matched_skills) * 10)
    if skill_score>40:
        skill_score=40
    bed_score = len(matched_beds)*5
    skill_score -= bed_score
    result = ""
    if(len(answer)>100):
        skill_score+=10
    elif(len(answer)<30):
        skill_score-=10
    if skill_score>=50:
        result= "매우 좋음"
    elif skill_score>=40:
        result= "좋음"
    elif skill_score>=30:
        result= "적당"
    elif skill_score>=20:
        result= "평범"
    else:
        result="미흡"
    return  "평가 : "+result+" 포함_스킬 : "+ str(list(matched_skills))+ " 안좋은_말 : "+str(list(matched_beds))
def get_job_question(job):
    file_path = os.path.join(settings.BASE_DIR,'static','job_questions.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for entry in data:
            if entry['job'] == job:
                return random.choice(entry['questions'])
    return "직무를 찾지 못했습니다"
def get_me_question():
    question=[  { "question": "본인의 강점과 약점을 말씀해주세요." },
  { "question": "이전에 수행했던 주요 프로젝트나 업무 경험을 말씀해주세요." },
  { "question": "가장 도전적이었던 과제를 어떻게 해결했나요?" },
  { "question": "협업 또는 팀 프로젝트 경험을 소개해주세요." },
  { "question": "업무 중 예상치 못한 문제를 어떻게 해결했나요?" },
  { "question": "업무 중 실수를 한 경험이 있다면, 어떻게 대처했나요?" },
  { "question": "상사나 동료와 의견 충돌이 있었을 때 어떻게 해결했나요?" },
  { "question": "새로운 환경에 어떻게 적응하시나요?" },
  { "question": "직무 관련 자격증, 학습 또는 연구 경험을 말씀해주세요." },
  { "question": "최근 직무 관련 트렌드나 기술을 어떻게 공부하고 있나요?" },
  { "question": "회사에서 어떤 성과를 이루고 싶으신가요?" },
  { "question": "본인의 직업 가치관은 무엇인가요?" },
  { "question": "입사 후 가장 먼저 하고 싶은 일은 무엇인가요?" },
  { "question": "업무 성과를 높이기 위해 어떤 노력을 하시나요?" },
  { "question": "과거 실패 경험과 그로부터 얻은 교훈은 무엇인가요?" },
  { "question": "스트레스를 어떻게 관리하시나요?" },
  { "question": "가장 자신 있는 역량은 무엇이고, 이를 어떻게 개발했나요?" },
  { "question": "본인이 생각하는 리더십이란 무엇인가요?" },
  { "question": "우리 회사의 어떤 점이 가장 매력적이라고 생각하시나요?" },
  { "question": "동료 또는 팀원과 좋은 관계를 유지하기 위해 어떻게 노력하시나요?" }]
    return random.choice([q["question"] for q in question])