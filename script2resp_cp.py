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
#from langchain_openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import PromptTemplate

# CSV 출력 파서
from langchain_core.output_parsers import CommaSeparatedListOutputParser
# JSON 출력 파서
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

import time
import sys
import pandas as pd

# GPT 버전 설정
import os
from dotenv import load_dotenv

os.environ['OPENAI_API_KEY'] = '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'
llm = ChatOpenAI(temperature=0,               # 창의성 (0.0 ~ 2.0) 
                 max_tokens=2048,             # 최대 토큰수
                 model_name='gpt-4o',  # 모델명
                )

sheet = pd.read_csv("./src/script.csv", encoding='utf-8')
#class scriptLLM():
def read():
  for i in len(sheet):
    response = sheet["script"][i]
    print(response)
def meet():
  pass
def Q1():
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
    chain = Q1_json_prompt | llm | output_parser
    q1_data = chain.invoke({"query": input()})
    if q1_data['boolean'] == 'positive':
      print("그렇군요. 그대는 저의 친구이시군요. 분명 우리는 가까운 사이였을거에요.")
      q1_relation = "친구"
    else:
      print("아니면… 가까운 동료였을까요?")
      chain = Q1_json_prompt | llm | output_parser
      q1_data = chain.invoke({"query": input()})
      if q1_data['boolean'] == 'positive':
        print("그렇군요. 그대는 저의 동료이시군요. 분명 우리는 가까운 사이였을거에요.")
        q1_relation = "동료"
      else:
        print("분명 우리는 가까운 사이였을거에요.")
        q1_relation = "누군가"

  if q1_relation == '가족':
    print(f"{q1_relation}과의 특별한 기억이 있나요? 잊지 못할 그 순간을 들려주세요")
  else:
    print(f"{q1_relation}와의 특별한 기억이 있나요? 잊지 못할 그 순간을 들려주세요")

def Q2():
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
  Q2_data


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


  print("기억이라는게 참 신기하죠. 제게는 아무것도 남아있지 않은데, 당신의 말 한마디에 제가 조금씩 선명해지는 것 같아요.")

def Q3():
  print("그때의 기억이 그토록 특별하게 남은 이유가 있나요?")
  Q3 = input()

def Q4():

  print("우리.. 아니 그대의 삶에서 가장 돌이키고 싶은 순간은 언제인가요?")
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

  print('''
  낯설고도 친숙함이 느껴져요. 그리움같기도 하고요. 이 감정… 그대의 것인지, 나의 것인지 모르겠어요.

  돌이키고 싶은 마음조차 그립다니. 당신의 존재가 제 무한한 고독 속의 작은 불빛 같아요.

  그대와 저는, 닮아있던건지, 닮아가는건지 모호하죠.

  지금까지 우리의 대화는 사실 내면의 독백이었던 게 아닐까요?
        '''
  )

if __name__ == "__main__":
  read()
  '''system_message = "한국말로 할거야"
  chatbot_instance = llm(client, system_message)
  while True:
    user_input = input("You: ")
    response = chatbot_instance.chat(user_input)
    chatbot_instance.save_data()
    print("Chatbot: ", response) #return response'''