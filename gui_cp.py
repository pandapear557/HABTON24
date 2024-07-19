import tkinter as tk
from tkinter import Canvas
import tkinter.font

from PIL import Image, ImageTk

import pygame
import threading
import time
import sys

from openai import OpenAI
import os
import json

import pandas as pd
import TypeHangul as type_md

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

import gui
import json
# GPT 버전 설정
import os
os.environ['OPENAI_API_KEY'] = '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'
llm = ChatOpenAI(model="gpt-4o")

class MyApp:
    def __init__(self, root):
        image_path = "./src/ui.png" 
        self.image = ImageTk.PhotoImage(Image.open(image_path))
        self.cnt = 0
        self.status = True
        self.relation = ""
        self.sheet = pd.read_excel("./src/script.xlsx")
        self.sheet.set_index(self.sheet.columns[0], inplace=True)

        self.root = root
        self.root.title("넋을 찾아주세요")
        self.font = tkinter.font.Font(family="AppleSDGothicNeoM00", size=18)
        self.refont = tkinter.font.Font(family="AppleSDGothicNeoSB00", size=20)
        self.width = 1440
        self.height = 900
        self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()

        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)
        

        # Pygame 초기화 및 사운드 로드
        pygame.mixer.init()
        self.sound = pygame.mixer.Sound("./src/climax.mp3")

        # 텍스트 입력 위젯
        self.entry = tk.Entry(self.root, font=self.font, fg='white', bg='black')      
        self.canvas.create_window(35, 550, window=self.entry, width=850, height=50, anchor=tk.SW)

        self.label=tkinter.Label(self.root, text=f"{self.sheet['script'].iloc[0]}", fg="white", bg="black", font=self.refont, justify = "left")
        self.label.place(x=35, y=380)

        # 엔터 키 이벤트 바인딩
        self.entry.bind("<Return>", self.process_input)

    def process_input(self, event):
        user_input = self.entry.get()
        if user_input:
            self.cnt += 1
            self.status = True
            self.entry.delete(0, tk.END)
            self.handle_response(user_input)

    def handle_response(self, user_input):
        buff = True
        while(self.status):
            if self.sheet["type"][self.cnt-1] == "nar":
                response = self.sheet["script"][self.cnt]
                print(self.cnt, self.sheet["script"][self.cnt])                
                self.label.config(text=response)
                typing_instance = type_md.TypeHangul(self.label, response)
                typing_instance.start_typing()
                if not type_md.is_typing:
                    self.cnt += 1
            else:
                print(self.cnt, self.sheet["script"][self.cnt])
                self.label.config(text=response)
                typing_instance = type_md.TypeHangul(self.label, response)
                typing_instance.start_typing()
                if not type_md.is_typing:              
                    self.status = False
        
        
    def llm_instance(self, user_input):
        if self.cnt < 7: #Q1
            #if(self.status): #True
            class Q1_Database(BaseModel):
                boolean: str = Field(default="", description="Is answer positive or negative?,unknown is negative, tell me as a noun")
            output_parser = JsonOutputParser(pydantic_object=Q1_Database)
            format_instructions = output_parser.get_format_instructions()
            
            Q1_json_prompt = PromptTemplate(
                template="Answer the user query.\n{format_instructions}\n{query}\n",
                input_variables=["query"],
                partial_variables={"format_instructions": format_instructions},
            )
        
            chain = Q1_json_prompt | llm | output_parser
            q1_data = chain.invoke({"query": user_input})

            if q1_data['boolean'] == 'positive':
                mapping = {5: "가족", 6: "친구", 7:"동료"}
                self.relation =  mapping[self.cnt]
                self.cnt = 8
                return self.sheet["script"][self.cnt]
            else:
                return self.sheet["script"][self.cnt]

    def save_data():
        pass
    
    def full_screen(self):
        self.root.attributes("-fullscreen", True)

# GUI 애플리케이션 실행
if __name__ == "__main__":

    root = tk.Tk()
    app = MyApp(root)
    
    root.mainloop()
