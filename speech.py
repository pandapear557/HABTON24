from elevenlabs.client import ElevenLabs
from elevenlabs  import play, stream, save
import os
from dotenv import load_dotenv
from pydub import AudioSegment

def clone(text):
  sound = AudioSegment.from_file("./src/voice.mp3")

  first = sound[12000:]
  second = sound[-12000:]

  first.export("./src/v1.mp3", format="mp3")
  second.export("./src/v2.mp3", format="mp3")

  voice = client.clone(
      name="me",
      description="test api", # Optional
      files=["./src/v1.mp3","./src/v2.mp3"]
  )
  audio = client.generate(text=text,
                          voice=voice, model="eleven_multilingual_v2")

  save(audio, "./src/res.mp3")
  #play(audio)


if __name__ == "__main__":
  load_dotenv()
  XI_API_KEY = os.environ['XI_API_KEY']
  client = ElevenLabs(
    api_key=XI_API_KEY
  )
  clone("안녕, 오래 기다렸지. 나의 기억. 나의 감정... 그리고. 내 흔적들이. 너의 현재와 공명하고 있어... 얼른 와.. 우리. 함께 시간이라는 무대.. 위에서 존재의. 춤을 추자.")