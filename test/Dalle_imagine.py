from openai import OpenAI
import os
import webbrowser

import urllib.request
import time
from dotenv import load_dotenv
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Replace YOUR_API_KEY with your OpenAI API key
load_dotenv()
OPENAI_API_KEY = os.environ['OPEN_AI_KEY']
client = OpenAI(api_key=OPENAI_API_KEY)

def generate(prompt):
    # 1장 생성 시 0.03$ 
    response = client.images.generate(
    model="dall-e-3",
    prompt=prompt,
    size="1024x1024",
    quality="standard",
    n=1,
    )
    url = response.data[0].url
    return url

def save_img(url,name):
    img_dest = "./src/img/"
    start = time.time()

    urllib.request.urlretrieve(url, img_dest+f"{name}")

    end = time.time()
    print(f"총 소요시간 {end-start}초")
if __name__ == "__main__":
##who, where, when, what >> 아버지랑 미국에서 살던 컨트리 동네를 한 바뀌 둘러보았던 기억
   save_img(generate("A serene lakeside scene in the impressionist style, with vibrant colors and visible brushstrokes." 
                    + "The scene captures the moment" 
                    + "A memory of walking around a country neighborhood in the US with my dad." 
                    + "The overall mood is peaceful and calm"), "t1.jpg")
   
##who, where, when, what >> 호주 강변에서 가족들이랑 보던 불꽃놀이
   save_img(generate("impressionist style, with vibrant colors and visible brushstrokes." 
                    + "The scene captures the moment" 
                    + "Watching fireworks with my family by the river in Australia" 
                    + "The overall mood is peaceful and calm"), "t2.jpg")