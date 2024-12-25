import tkinter as tk
import cv2
import pygame
import threading
import time

class Calculator:
    def __init__(self, master):
        self.master = master
        self.master.title("Calculator")
        self.master.geometry("360x410")
        self.result_var = tk.StringVar()

        self.entry = tk.Entry(
            master, textvariable=self.result_var, font=("Helvetica", 20),
            bd=15, insertwidth=4, width=14, justify="right"
        )
        self.entry.grid(row=0, column=0, columnspan=4)

        button_texts = [
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
            ("0", 4, 0), ("C", 4, 1), ("=", 4, 2), ("+", 4, 3),
        ]

        for text, row, column in button_texts:
            tk.Button(
                master, text=text, font=("Helvetica", 20),
                height=2, width=5, command=lambda t=text: self.button_click(t)
            ).grid(row=row, column=column)

        self.master.attributes("-topmost", True)
        self.block_keys()

    def block_keys(self):
        def block(event):
            return "break"
        for key in ["<Alt_L>", "<Alt_R>", "<Super_L>", "<Super_R>"]:
            self.master.bind(key, block)

    def button_click(self, text):
        if text == "=":
            try:
                self.result_var.set(int(eval(self.result_var.get())))
            except Exception:
                self.result_var.set("Error")
        elif text == "C":
            self.result_var.set("")
        else:
            self.result_var.set(self.result_var.get() + text)
        self.play_video()

    def play_video(self):
        pygame.display.init()
        cap = cv2.VideoCapture("boo.mp4")
        if not cap.isOpened():
            return

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_delay = 1 / fps if fps > 0 else 0.033

        cv2.namedWindow("Video", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.setWindowProperty("Video", cv2.WND_PROP_TOPMOST, 1)

        self.stop_music()
        threading.Thread(target=self.play_audio).start()

        while cap.isOpened():
            start_time = time.time()
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow("Video", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            time.sleep(max(0, frame_delay - (time.time() - start_time)))

        cap.release()
        cv2.destroyAllWindows()
        pygame.quit()
        self.master.quit()

    def play_audio(self):
        pygame.mixer.init()
        try:
            pygame.mixer.music.load("audio.mp3")
            pygame.mixer.music.play()
        except Exception:
            pass

    def stop_music(self):
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()

if __name__ == "__main__":
    root = tk.Tk()
    Calculator(root)
    root.mainloop()
