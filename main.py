import gui
import tkinter as tk
from PIL import ImageTk, Image
from dotenv import load_dotenv

import os
import sys

from openai import OpenAI
import Chatbot as chat_md

import time
    
    
if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    client = OpenAI(api_key=api_key)
    system_message = "한국말로 할거야"
    chatbot_instance = chat_md.Chatbot(client, system_message)
    root = tk.Tk()
    app = gui.MyApp(root, chatbot_instance)
    root.mainloop