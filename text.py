import tkinter as tk
from tkinter import messagebox
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

import TypeHangul as type_md
from dotenv import load_dotenv


class Chatbot:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def chat(self, user_input):
        response = self.client.Completion.create(
            engine="text-davinci-003",
            prompt=user_input,
            max_tokens=150
        )
        return response.choices[0].text.strip()

    def save_data(self, file_path):
        # Placeholder for saving data, implement as needed
        pass


class MyApp:
    def __init__(self, root, chatbot_instance):
        image_path = "./src/ui.png"
        self.image = ImageTk.PhotoImage(Image.open(image_path))

        self.root = root
        self.root.title("넋을 찾아주세요")
        self.font = tkinter.font.Font(family="Nanum Pen Script OTF", size=24)

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
        self.canvas.create_window(100, 100, window=self.entry)

        # 지시문 레이블
        self.label = tk.Label(root, text="텍스트를 입력하고 엔터 키를 누르세요.")
        self.canvas.create_window(100, 150, window=self.label)

        # 엔터 키 이벤트 바인딩
        self.entry.bind("<Return>", self.process_input)

    def process_input(self, event):
        user_input = self.entry.get()
        if user_input.lower() == "kill":
            self.root.destroy()
            print("Chatbot: Goodbye!")
            sys.exit()
            return

        if user_input:
            response = self.chatbot_instance.chat(user_input)
            self.chatbot_instance.save_data("data.json")
            self.entry.delete(0, tk.END)
            
            typing_instance = type_md.TypeHangul(self.label, response, delay=50)
            typing_instance.start_typing()

    def play_sound(self):
        self.sound.play()

    def sound_ctl(self):
        def timer():
            while True:
                time.sleep(10)  # 10초마다 사운드 재생
                self.play_sound()

        thread = threading.Thread(target=timer)
        thread.daemon = True  # 프로그램 종료 시 스레드도 종료
        thread.start()


# GUI 애플리케이션 실행
if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("API key not found. Please set the OPENAI_API_KEY environment variable.")
        sys.exit(1)

    chatbot_instance = Chatbot(api_key=api_key)
    root = tk.Tk()
    app = MyApp(root, chatbot_instance)

    root.mainloop()
