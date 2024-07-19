import tkinter as tk

class SyncWindows:
    def __init__(self):
        self.main_window = self.create_main_window()
        self.duplicate_window = self.create_duplicate_window()
        
        # Initialize the windows with some content
        self.init_main_window_content()
        self.init_duplicate_window_content()
        
        # Set up trace to synchronize changes
        self.setup_trace()

    def create_main_window(self):
        main_window = tk.Tk()
        main_window.title("Main Window")
        main_window.geometry("400x200")
        return main_window

    def create_duplicate_window(self):
        duplicate_window = tk.Toplevel()
        duplicate_window.title("Duplicate Window")
        duplicate_window.geometry("400x200")
        self.move_window_to_secondary_screen(duplicate_window)
        return duplicate_window

    def move_window_to_secondary_screen(self, window):
        # 현재 스크린의 정보를 얻습니다
        window.update_idletasks()
        primary_screen_width = window.winfo_screenwidth()
        primary_screen_height = window.winfo_screenheight()
        
        # 보조 스크린의 좌표를 설정합니다 (이 예제에서는 오른쪽에 있는 보조 스크린을 가정합니다)
        secondary_screen_x = primary_screen_width
        secondary_screen_y = 0
        
        # 창을 보조 스크린으로 이동합니다
        window.geometry(f"+{secondary_screen_x}+{secondary_screen_y}")

    def init_main_window_content(self):
        self.main_label_text = tk.StringVar(value="This is the main window")
        self.main_label = tk.Label(self.main_window, textvariable=self.main_label_text, font=("Helvetica", 16))
        self.main_label.pack(pady=50)
        
        self.main_entry = tk.Entry(self.main_window, textvariable=self.main_label_text)
        self.main_entry.pack(pady=10)

    def init_duplicate_window_content(self):
        self.duplicate_label_text = tk.StringVar(value="This is the duplicate window")
        self.duplicate_label = tk.Label(self.duplicate_window, textvariable=self.duplicate_label_text, font=("Helvetica", 16))
        self.duplicate_label.pack(pady=50)

    def setup_trace(self):
        # Trace changes to main_label_text variable
        self.main_label_text.trace_add("write", self.update_duplicate_window)

    def update_duplicate_window(self, *args):
        self.duplicate_label_text.set(self.main_label_text.get())

    def run(self):
        self.main_window.mainloop()

if __name__ == "__main__":
    app = SyncWindows()
    app.run()
