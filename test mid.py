import tkinter as tk
import time
import random
from PIL import Image, ImageTk

# ------- Random sentences -------
sentences = [
    "The quick brown fox jumps over the lazy dog",
    "Typing fast is a useful skill for everyone",
    "Python is a great language for beginners",
    "Practice every day to improve your speed",
    "Artificial intelligence is changing the world"
]

# ------- Select a random one -------
current_sentence = random.choice(sentences)

start_time = None

def start_test(event):
    global start_time
    start_time = time.time()

def finish_test():
    end_time = time.time()
    time_taken = end_time - start_time

    typed = entry.get()
    words = len(typed.split())
    wpm = int(words / (time_taken / 60))

    # Update WPM label
    result_label.config(text=f"WPM: {wpm}")

    # ------- Show meme based on speed -------
    if wpm < 40:
        img_path = "slow.png"
    elif wpm < 80:
        img_path = "medium.png"
    else:
        img_path = "fast.png"

    img = Image.open(img_path)
    img = img.resize((250, 250))
    img_tk = ImageTk.PhotoImage(img)

    meme_label.config(image=img_tk)
    meme_label.image = img_tk  # keep reference


# ------- GUI -------
root = tk.Tk()
root.title("Typing Speed Test")

sentence_label = tk.Label(root, text=current_sentence, font=("Arial", 14))
sentence_label.pack(pady=10)

entry = tk.Entry(root, width=50, font=("Arial", 14))
entry.pack(pady=10)
entry.bind("<KeyPress>", start_test)

finish_button = tk.Button(root, text="Finish", command=finish_test)
finish_button.pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 16))
result_label.pack(pady=10)

meme_label = tk.Label(root)
meme_label.pack(pady=10)

root.mainloop()
