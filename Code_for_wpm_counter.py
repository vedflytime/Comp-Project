import tkinter as tk
import time
import os
import random
from PIL import Image, ImageTk

sentences = [    "Granny in heaven, I’m higher than her, broke my heart so I went to the bank",
    "The quick brown fox jumps over the lazy dog\no",
    "Hard work beats talent when talent doesn’t work hard",
        "Practice typing daily to improve your speed and accuracy",
    "I love snowbunnies and they dont love me",
    """The pelagic argosy sights the deep
o"""]
TEXT = random.choice(sentences)   


LEADERBOARD_FILE = "leaderboard.txt"

#SLOW_IMG   = r"C:\Users\itz9x\OneDrive\Pictures\Saved Pictures\slow.png"
#MEDIUM_IMG = r"C:\Users\itz9x\OneDrive\Pictures\Saved Pictures\medium.png"
#FAST_IMG   = r"C:\Users\itz9x\OneDrive\Pictures\Saved Pictures\fast.png"

start_time = None   

def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as f:
            return [line.strip() for line in f.readlines()]
    return []

def save_score(name, wpm):
    scores = load_leaderboard()
    scores.append(f"{name} - {wpm:.2f} WPM")
    with open(LEADERBOARD_FILE, "w") as f:
        for s in scores:
            f.write(s + "\n")

def update_leaderboard_display():
    scores = load_leaderboard()
    leaderboard_text = "\n".join(scores[-10:])
    leaderboard_label.config(text=leaderboard_text)

def start_test():
    global start_time 
    global TEXT
    TEXT = random.choice(sentences)
    sentence_display.config(text=TEXT)

    entry.delete("1.0", "end")
    start_time = time.time()
    result_label.config(text="")
    meme_label.config(image="")

def calculate_results():
    if start_time is None:
        return

    end_time = time.time()
    typed = entry.get("1.0", "end")
    
    time_taken = end_time - start_time
    words = len(typed.split())
    
    wpm = (words / time_taken) * 60 if time_taken > 0 else 0

    correct_chars = sum(1 for a, b in zip(typed, TEXT) if a == b)
    accuracy = (correct_chars / len(TEXT)) * 100

    name = name_entry.get() or "Player"
    save_score(name, wpm)
    update_leaderboard_display()

    result_label.config(
        text=f"WPM: {wpm:.2f}   |   Accuracy: {accuracy:.2f}%"
    )

    """if wpm < 40:
        img_path = SLOW_IMG
    elif wpm < 80:
        img_path = MEDIUM_IMG
    else:
        img_path = FAST_IMG

    img = Image.open(img_path)
    img = img.resize((250, 250))
    img_tk = ImageTk.PhotoImage(img)

    meme_label.config(image=img_tk)
    meme_label.image = img_tk"""

root = tk.Tk()
root.title("Typing Speed Test with Leaderboard + Memes")

tk.Label(root, text="Enter your name:").pack()
name_entry = tk.Entry(root, width=30)
name_entry.pack(pady=5)

tk.Label(root, text="Type this sentence:").pack()

# Use label so we can update the sentence
sentence_display = tk.Label(root, text=TEXT, fg="blue")
sentence_display.pack(pady=5)

entry = tk.Text(root, width=60,height=10)
entry.pack(pady=20,padx = 20)



tk.Button(root, text="Start", command=start_test).pack()
tk.Button(root, text="Done", command=calculate_results).pack(pady=5)

result_label = tk.Label(root, text="", fg="green")
result_label.pack(pady=10)

tk.Label(root, text="Leaderboard (Last 10 scores):", fg="purple").pack()
leaderboard_label = tk.Label(root, text="", justify="left")
leaderboard_label.pack(pady=10)

meme_label = tk.Label(root)
meme_label.pack(pady=10)

update_leaderboard_display()

root.mainloop()
