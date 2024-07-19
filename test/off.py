import subprocess
from pynput import keyboard

def set_brightness(level):
    script = f'do shell script "/opt/homebrew/Cellar/brightness/1.2/bin/brightness {level}"'
    subprocess.run(["osascript", "-e", script])

def on_press(key):
    try:
        if key.char == 'a':
            set_brightness(1)  # 밝기 최대
        elif key.char == 'b':
            set_brightness(0)  # 밝기 최소
    except AttributeError:
        pass

def main():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()

