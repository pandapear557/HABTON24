import tkinter as tk
import time
import textwrap

class TypeHangul:
    is_typing = False
    def __init__(self, label, text, delay=10, line_length=55):
        self.label = label
        self.text = self.wrap_text(text, line_length)
        self.delay = delay
        self.current_index = 0

    def wrap_text(self, text, line_length):
        if len(text) > line_length:
            wrapped_text = '\n'.join(textwrap.wrap(text, width=line_length))
            return wrapped_text
        else: return text
    
    def type_character(self):
        if self.current_index < len(self.text):
            self.label.config(text=self.label.cget("text") + self.text[self.current_index])
            self.current_index += 1
            self.label.after(self.delay, self.type_character)

    def start_typing(self):
        if not is_typing:
            is_typing = True
            self.label.config(text="")
            self.current_index = 0
            self.type_character()
        
    

def main():
    root = tk.Tk()
    root.title("Type Hangul Effect")

    label = tk.Label(root, text="", font=("Arial", 24))
    label.pack(pady=20)

    text = "안녕하세요. 한글 타이핑 효과입니다. 걱정마세요 줄바꿈을 적절한 타이밍에 해줄테니까"

    type_hangul = TypeHangul(label, text, delay=200)
    type_hangul.start_typing()

    root.mainloop()

if __name__ == "__main__":
    main()
