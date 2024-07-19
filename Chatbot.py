from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.environ['OPEN_AI_KEY']
client = OpenAI(api_key=OPENAI_API_KEY)

class Chatbot:
    def __init__(self, client, system_message):
        self.client = client
        self.system_message = system_message
        self.chat_history = []
         
    def chat(self, user_input):
        messages = [{"role": "system", "content": self.system_message}]
        for message in self.chat_history:
            messages.append(message)
        messages.append({"role": "user", "content": user_input})
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        
        assistant_message = response.choices[0].message.content
        self.chat_history.append({"role": "user", "content": user_input})
        self.chat_history.append({"role": "assistant", "content": assistant_message})
        return assistant_message
        
    def save_data(self):
        with open("./src/data.json", 'w', encoding='utf-8') as json_file:
            json.dump(self.chat_history, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    # 시스템 메시지 설정
    system_message = "한국말로 할거야"

    # Chatbot 인스턴스 생성
    chatbot_instance = Chatbot(client, system_message)

    # 챗봇과 대화 예시
    user_input = "제대로 작동하고 있다면 [READY]를 출력하시오"
    response = chatbot_instance.chat(user_input)
    print("Chatbot: ", response)

    while True:
        user_input = input("You: ")

        if user_input.lower() == "KILL":
            print("Chatbot: Goodbye!")
            break

        response = chatbot_instance.chat(user_input)
        chatbot_instance.save_data()
        print("Chatbot: ", response)