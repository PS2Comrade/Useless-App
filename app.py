import tkinter as tk
from tkinter import filedialog, Text
from tkinter import ttk
import cv2
from PIL import Image, ImageTk

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Player and Text Editor")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both')

        self.video_frame = ttk.Frame(self.notebook)
        self.text_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.video_frame, text='Video Player')
        self.notebook.add(self.text_frame, text='Text Editor')

        self.create_video_player()
        self.create_text_editor()

    def create_video_player(self):
        self.video_label = tk.Label(self.video_frame)
        self.video_label.pack()

        self.open_button = tk.Button(self.video_frame, text="Open Video", command=self.open_video)
        self.open_button.pack()

        self.video_path = None
        self.cap = None
        self.playing = False

    def open_video(self):
        self.video_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mkv")])
        if self.video_path:
            self.cap = cv2.VideoCapture(self.video_path)
            self.playing = True
            self.play_video()

    def play_video(self):
        if self.playing and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)
                self.video_label.after(10, self.play_video)
            else:
                self.cap.release()

    def create_text_editor(self):
        self.text_editor = Text(self.text_frame)
        self.text_editor.pack(expand=True, fill='both')

        self.open_text_button = tk.Button(self.text_frame, text="Open Text File", command=self.open_text_file)
        self.open_text_button.pack()

        self.save_text_button = tk.Button(self.text_frame, text="Save Text File", command=self.save_text_file)
        self.save_text_button.pack()

    def open_text_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_editor.delete(1.0, tk.END)
                self.text_editor.insert(tk.END, content)

    def save_text_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as file:
                content = self.text_editor.get(1.0, tk.END)
                file.write(content)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)  
    root.mainloop()
  
