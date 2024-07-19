import tkinter as tk
from tkinter import Canvas
import tkinter.font
from ttkthemes import ThemedTk

from PIL import Image, ImageTk

import pygame
import threading
import time
import sys

from openai import OpenAI
import os
import json

import Chatbot as chat_md
import TypeHangul as type_md
from dotenv import load_dotenv

class MyApp:
    def __init__(self, root, chatbot_instance):
        image_path = "./src/ui.png" 
        self.image = ImageTk.PhotoImage(Image.open(image_path))

        self.root = root
        self.root.title("넋을 찾아주세요")
        self.font = tkinter.font.Font(family="AppleSDGothicNeoM00", size=18)
        self.refont = tkinter.font.Font(family="AppleSDGothicNeoSB00", size=20)
        self.width = 1440
        self.height = 900
        self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()

        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)

        self.chatbot_instance = chatbot_instance

        # Pygame 초기화 및 사운드 로드
        pygame.mixer.init()
        self.sound = pygame.mixer.Sound("./src/climax.mp3")

        # 텍스트 입력 위젯
        self.entry = tk.Entry(self.root, font=self.font, fg='white', bg='black')      
        self.canvas.create_window(35, 550, window=self.entry, width=850, height=50, anchor=tk.SW)

        # 지시문 레이블
        #self.label = tk.Label(self.root, text="텍스트를 입력하고 엔터 키를 누르세요.", 
        #                     font=self.font, fg='white', relief="solid", width=10, height=5)
        #self.label.pack()
        self.label=tkinter.Label(self.root, text=" ", fg="white", bg="black",
                                          font=self.refont, justify = "left")
        self.label.place(x=35, y=380)

        # 엔터 키 이벤트 바인딩
        self.entry.bind("<Return>", self.process_input)

    def process_input(self, event):
        user_input = self.entry.get()
        if user_input:
            self.entry.delete(0, tk.END)
            threading.Thread(target=self.handle_response, args=(user_input,)).start()

    def handle_response(self, user_input):
        response = self.chatbot_instance.chat(user_input)
        self.chatbot_instance.save_data()

        self.label.config(text=response)
        typing_instance = type_md.TypeHangul(self.label, response)
        typing_instance.start_typing()
    
    def full_screen(self):
        self.root.attributes("-fullscreen", True)

# GUI 애플리케이션 실행
if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    client = OpenAI(api_key=api_key)
    
    system_message = "한국말로 할거야"
    chatbot_instance = chat_md.Chatbot(client, system_message)
    
    root = tk.Tk()
    app = MyApp(root, chatbot_instance)
    
    root.mainloop()
