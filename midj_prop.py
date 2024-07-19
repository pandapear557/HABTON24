import os
os.environ['OPENAI_API_KEY'] = 'sk-None-PjRacYmvRYUCidM6CvJDT3BlbkFJtcgv5RvJ6805Xe9MrmCC' # 내 키
import openai
from dotenv import load_dotenv

# 토큰 정보로드
load_dotenv()

from openai import OpenAI

client = OpenAI()

from langchain_core.prompts import PromptTemplate
import pandas as pd
import csv

def midj_prompt_generate(who='사람들과', where='근처에서', what='지냈다',when='그 때'):
    def midf_prom(who, where, what,when):
        # 'name'과 'age'라는 두 개의 변수를 사용하는 프롬프트 템플릿을 정의
        template_text = "누구와인지는 {who}이고, 어디서였는지는 {where}, 무엇을 했는지는 {what}, 언제였는지는 {when}으로 화가 모네와 반 고흐같은 인상주의 그림을 생성할 수 있는 프롬프트를 English로 작성해줘."
        # PromptTemplate 인스턴스를 생성
        prompt_template = PromptTemplate.from_template(template_text)
        # 템플릿에 값을 채워서 프롬프트를 완성
        filled_prompt = prompt_template.format(who=who, where=where, what=what, when=when)
        return prompt_template

    midj_prompt1 = midf_prom('가족','바다','수영을 했다','여름')

    from langchain_openai import ChatOpenAI
    from langchain_core.output_parsers import StrOutputParser

    llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
    chain = midj_prompt1 | llm | StrOutputParser()
    return chain.invoke({"who":who,"where":where,"what":what,"when":when})



############################## csv 에서 인자 가져오기
# CSV 파일 읽기
with open("Q2_data.csv", mode='r', encoding='utf-8-sig') as file:
    reader = csv.reader(file)
    next(reader)  # 첫 번째 줄은 헤더이므로 건너뜁니다.
    
    # 각 행을 함수의 파라미터로 전달
    for row in reader:
        if len(row) == 2:  # 정확히 두 개의 열이 있는 경우에만 처리
            key = row[0].strip()  # 키
            value = row[1].strip()  # 값
            
            # 함수 호출
            if key == 'who':
                who = value
            elif key == 'where':
                where = value
            elif key == 'what':
                what = value
            elif key == 'when':
                when = value
    
    # 함수 호출
    P = midj_prompt_generate('남자친구','야외',"따뜻한 밥")


DF = pd.DataFrame({'prompt' : [P.split('\n')[-1]]})
# CSV 파일 경로
csv_file_path = 'midj.csv'

# CSV 파일이 존재하는지 확인
if os.path.exists(csv_file_path):
    # 기존 CSV 파일 읽기
    df = pd.read_csv(csv_file_path)
else:
    # 새로운 DataFrame 생성
    df = pd.DataFrame(columns=['prompt'])

# 새로운 프롬프트를 DataFrame에 추가
df = df.append({'prompt': P.split('\n')[-1]}, ignore_index=True)

# DataFrame을 CSV 파일로 저장
df.to_csv(csv_file_path, index=False)

print(f"프롬프트가 {csv_file_path} 파일에 추가 또는 업데이트되었습니다.")

# CSV 파일 읽기
df_updated = pd.read_csv(csv_file_path)

# DataFrame 출력
print("CSV 파일에서 읽은 데이터:")
print(df_updated)