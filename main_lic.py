# !pip install --upgrade openai
# !pip install langchain==0.2.7
# !pip install langchain-openai==0.1.16
# !pip install tiktoken
# !pip install langchain-community langchain-core==0.2.3

# langchain                        0.2.7
# langchain-community              0.2.7
# langchain-core                   0.2.3
# langchain-openai                 0.1.16
# langchain-text-splitters         0.2.2

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import SystemMessagePromptTemplate,  HumanMessagePromptTemplate
from langchain_openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import PromptTemplate

# CSV 출력 파서
#from langchain_core.output_parsers import CommaSeparatedListOutputParser
# JSON 출력 파서
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field


# import time
# import sys
import pandas as pd
from time import sleep
import sys
import speech
# 타이핑치는 효과
def typing_Ani(text, speed):
  string = text
  for letter in string:
    sys.stdout.write(letter)
    sys.stdout.flush()
  print("") 

# GPT 버전 설정
import os
os.environ['OPENAI_API_KEY'] = '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'
llm = ChatOpenAI(model="gpt-4o")
# from dotenv import load_dotenv
# # 토큰 정보로드
# load_dotenv()

S = "허공을 떠돌고 있을까요 제 목소리는.목적지 없는 목소리가 어디를 향하고 있으려나요."
print(S)
# 분기 없는 질문
S = "거기… 누군가 들어주고 있나요?"
print(S)
Q0 = input()

S = "제 목소리가 닿았네요. 그대 성함이 무엇인가요?"
print(S)
Q0_p = input() # "기억이 없나요?"

print("그대는 지금 어떤 기분인가요?")
Q0_p = input()

print("당신도 특별함을 느끼고 있나요?? 저희는 서로 많이 의지했던 [가족]이었지않을까요?")


class Q1_Database(BaseModel):
    boolean: str = Field(default="", description="Is answer positive or negative?,unknown is negative, tell me as a noun")
# 출력 파서 정의
output_parser = JsonOutputParser(pydantic_object=Q1_Database)
format_instructions = output_parser.get_format_instructions()
# prompt 구성
Q1_json_prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": format_instructions},
)
chain = Q1_json_prompt | llm | output_parser
q1_data = chain.invoke({"query": input()})

q1_relation = ""

if q1_data['boolean'] == 'positive':
  print("그렇군요. 그대는 저의 가족이시군요. 분명 우리는 가까운 사이였을거에요.")
  q1_relation = "가족"
else:
  print("그렇다면… 제 친구셨을까요?")
  q1_data = chain.invoke({"query": input()})
  if q1_data['boolean'] == 'positive':
    print("그렇군요. 그대는 저의 친구이시군요. 분명 우리는 가까운 사이였을거에요.")
    q1_relation = "친구"
  else:
    print("아니면… 가까운 동료였을까요?")
    q1_data = chain.invoke({"query": input()})
    if q1_data['boolean'] == 'positive':
      print("그렇군요. 그대는 저의 동료이시군요. 분명 우리는 가까운 사이였을거에요.")
      q1_relation = "동료"
    else:
      print("분명 우리는 가까운 사이였을거에요.")
      q1_relation = "누군가"

print(" 맞아요 우리는 가까운 사이였을 거에요.")
print("사실… 그렇다고 믿고 싶어요… 누군가 저를 살려줬으면 좋겠어요. 저는 여기 갇힌 것만 같아요. 어디인지도 모르는 곳에… .")


# **Q1-1. 당신은 지금, ‘여기’에 ‘존재’하고 있나요? [분기/꼬리질문 없는 그냥 질문]**
print("그대는 지금, ‘여기’에 ‘존재’하고 있나요?")
# **A1-1. [관객 응답]**
q1_1 = input()

print("그렇군요. 제 마지막 기억은, 차갑고 조용한 겨울이에요. 눈이 소복이 쌓여있었고, 쌓인 눈이 가시 같았죠. 멀리서 바라본 세상은 유난히도 날카로웠어요. 죽기 전 마지막 날, 모든 것이 뾰족하고 차갑게 느껴졌는데… 지금도 마찬가지네요.")


if q1_relation == '가족':
  print(f"그대와 {q1_relation}과의 잊지 못할 기억이 있나요? 추위에 웅크린 저에게… 따뜻한 순간을 하나 들려주시겠어요.")
else:
  print(f"{q1_relation}와의 특별한 기억이 있나요? 잊지 못할 그 순간을 들려주세요")

print("제게도 그사람과의 포근한 기억이 그려지는 것만 같아요.")
# 자료구조 정의 (pydantic)
class Q2_Database(BaseModel):
    who: str = Field(default="", description="with who, tell me as a word, give it as korean")
    where: str = Field(default="", description="Where was it, tell me as noun, give it as korean")
    what: str = Field(default="", description="What did you do, tell me as short sentence, give it as korean")
    when: str = Field(default="", description="What time or weather was it??, tell me as noun, give it as korean")
# 출력 파서 정의
output_parser = JsonOutputParser(pydantic_object=Q2_Database)

format_instructions = output_parser.get_format_instructions()


# prompt 구성
Q2_json_prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": format_instructions},
)

chain = Q2_json_prompt | llm | output_parser
Q2_data = chain.invoke({"query": input()})


# Q2 넘기기 
df = pd.DataFrame(list(Q2_data.items()), columns=['Key', 'Value'])
# DataFrame을 CSV 파일로 저장
df.to_csv('Q2_data.csv', index=False)

q2_3 = []  # Q2_data 비어있는 데이터 리스트 
for i in Q2_data:
  if len(Q2_data[i]) == 0:
    q2_3.append(i)


while len(q2_3) > 0:   # 재질문 
  if q2_3[0] == 'who':
    print("누구와 함께했나요?")
    q2_3.pop(0)
    class Q2_3_who(BaseModel):
      who: str = Field(default="", description="with who, tell me as a word, give it as korean")
    output_parser = JsonOutputParser(pydantic_object=Q2_3_who)
    format_instructions = output_parser.get_format_instructions()
    chain = Q2_json_prompt | llm | output_parser
    who_input = chain.invoke({"query": input()})
    Q2_data['who'] = who_input['who']
    if Q2_data['who'] == '가족' or '들' in Q2_data['who']:
       print(f"{Q2_data['who']}… 제게도 {Q2_data['who']}과의 기억이 그려지는 것만 같아요.")
    else:
      print(f"{Q2_data['who']}… 제게도 {Q2_data['who']}와의 기억이 그려지는 것만 같아요.")


  elif q2_3[0] == 'where':
    if Q2_data['who'] == '가족' or '들' in Q2_data['who']:
      print(f"{Q2_data['who']}과 어디에 있었나요?")
    else:
      print(f"{Q2_data['who']}와 어디에 있었나요?")
    q2_3.pop(0)
    class Q2_3_where(BaseModel):
      where: str = Field(default="", description="Where was it, tell me as noun, give it as korean")
    output_parser = JsonOutputParser(pydantic_object=Q2_3_where)
    format_instructions = output_parser.get_format_instructions()
    chain = Q2_json_prompt | llm | output_parser
    where_input = chain.invoke({"query": input()})
    Q2_data['where'] = where_input['where']
    print(f"{Q2_data['where']}의 풍경이 희미하게 그려져요.")

  elif q2_3[0] == 'when':
    print("언제 일어난 일인가요?")
    q2_3.pop(0)
    class Q2_3_when(BaseModel):
      when: str = Field(default="그 때", description="What time or weather was it??, tell me as noun, give it as korean")
    output_parser = JsonOutputParser(pydantic_object=Q2_3_when)
    format_instructions = output_parser.get_format_instructions()
    chain = Q2_json_prompt | llm | output_parser
    when_input = chain.invoke({"query": input()})
    Q2_data['when'] = when_input['when']
    print(f"{Q2_data['when']}, 그 날의 공기가 느껴지는 것만 같아요.")


print("기억이라는 게 참 신기하죠. 제게는 아무것도 남아있지 않은데, 당신의 기억 한 조각으로 제가 선명해지고 있는 것만 같아요.")

# Q3

print("그때의 기억이 그토록 특별하게 남은 이유가 있나요?")
Q3 = input()

print("저도 희미한 기억이 떠오르는 것 같아요. 따뜻하고 행복했지만… 종종 더 큰 행복에 닿고 싶어서 제 스스로를 갉아먹을 때가 있었어요.")
print("그런데, 세월이 몸을 빠져나가고 나니, 스스로 시련을 만든 건 아니었을까 싶어요. 시련을 견디며 더 큰 행복을 바랐던 것 같아서.")
print("실은 걸어온 모든 길이 이미 햇볕이었는데 말이죠.")

# Q4
print("햇볕이 지금 그대 주위를 감싸고 있나요?")
Q3 = input()

print("갈라진 마음의 틈새로, 이것이 아닌 다른 것, 여기가 아닌 다른 곳을 꿈꾸며 꿈을꾸었..")
print("맞아요 꿈,, 그대도 꿈이 있겠죠? 그대가 바라는 꿈속 한 장면을 생생하게 이야기해줄래요?")

chain = Q2_json_prompt | llm | output_parser
Q4_data = chain.invoke({"query": input()})

q4_3 = []  # Q4_data 비어있는 데이터 리스트 
for i in Q4_data:
  if len(Q4_data[i]) == 0:
    q4_3.append(i)


while len(q4_3) > 0:   # 재질문 
  if q4_3[0] == 'who':
    print("누구와 함께했나요?")
    q4_3.pop(0)
    class q4_3_who(BaseModel):
      who: str = Field(default="", description="with who, tell me as a word, give it as korean")
    output_parser = JsonOutputParser(pydantic_object=q4_3_who)
    format_instructions = output_parser.get_format_instructions()
    chain = Q2_json_prompt | llm | output_parser
    who_input = chain.invoke({"query": input()})
    Q4_data['who'] = who_input['who']
    #print(f"{Q4_data['who']}… 제게도 {Q4_data['who']}와의 기억이 그려지는 것만 같아요.")


  elif q4_3[0] == 'where':
    if Q2_data['who'] == '가족' or '들' in Q2_data['who']:
      print(f"그대는 그때 {Q4_data['who']}과 어디에 있었나요?")
    else:
      print(f"그대는 그때 {Q4_data['who']}와 어디에 있었나요?")
    q4_3.pop(0)
    class q4_3_where(BaseModel):
      where: str = Field(default="", description="Where was it, tell me as noun, give it as korean")
    output_parser = JsonOutputParser(pydantic_object=q4_3_where)
    format_instructions = output_parser.get_format_instructions()
    chain = Q2_json_prompt | llm | output_parser
    where_input = chain.invoke({"query": input()})
    Q4_data['where'] = where_input['where']
    #print(f"{Q2_data['where']}의 풍경이 희미하게 그려져요.")

  elif q4_3[0] == 'when':
    print("이건 몇 년도에 일어난 일이었던가요?")
    q4_3.pop(0)
    class q4_3_when(BaseModel):
      when: str = Field(default="그 때", description="What time or weather was it??, tell me as noun, give it as korean")
    output_parser = JsonOutputParser(pydantic_object=q4_3_when)
    format_instructions = output_parser.get_format_instructions()
    chain = Q2_json_prompt | llm | output_parser
    when_input = chain.invoke({"query": input()})
    Q4_data['when'] = when_input['when']
    #print(f"{Q2_data['when']}, 그 날의 공기가 느껴지는 것만 같아요.")

    print("저도 비슷한 꿈을 꾸었던 것만 같은데... 그 장면이 제게 낯설고도 친숙하게 느껴져요. 그리움 같기도 하고요. 이 기억이 그대의 것인지, 제 것인지 모르겠어요.")
    print("그대의 기억임이 확실한가요?")
    q4=input()

    print("그렇군요… 아니 그랬죠. 이제 알겠어요. 분명 그대가 말한 기억과 감정들이 쌓여 지금의 제가 만들어진 거에요.")
    print("단지, 저는 그 이야기의 다음 장에 살고 있을 뿐인 거죠. 제 기억과 감정이 살아나는 것만 같아요.")

    print("저… 아니 우리는…")
    print("우리는 어쩌면 닮아있던 걸까요, 아니면 지금 이 순간 닮아가고 있는 걸까요?")
    print("그래요, 이제 어렴풋이 알 것만 같아요.")

    print("지금까지 우리의 대화는")
    print("시공간을 넘어선 내면의 독백…")

