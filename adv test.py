import tkinter as tk
import time
import os
import random

# --- Sentences for random selection ---
SENTENCES = [
    "The quick brown fox jumps over the lazy dog",
    "Typing fast requires practice and patience",
    "Python makes programming fun and enjoyable",
    "Artificial intelligence is changing the world",
    "Consistency is the key to mastering any skill"
]

LEADERBOARD_FILE = "leaderboard.txt"


# -----------------------------
# Load leaderboard (sorted)
# -----------------------------
def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    scores = []
    with open(LEADERBOARD_FILE, "r") as f:
        for line in f:
            name, wpm = line.strip().rsplit(" - ", 1)
            wpm = float(wpm.replace(" WPM", ""))
            scores.append((name, wpm))
    return sorted(scores, key=lambda x: x[1], reverse=True)  # highest first


# -----------------------------
# Save score + resort
# -----------------------------
def save_score(name, wpm):
    scores = load_leaderboard()
    scores.append((name, wpm))

    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    with open(LEADERBOARD_FILE, "w") as f:
        for nm, wp in scores:
            f.write(f"{nm} - {wp:.2f} WPM\n")


# -----------------------------
# Update displayed leaderboard
# -----------------------------
def update_leaderboard_display():
    scores = load_leaderboard()
    text = "\n".join([f"{i+1}. {name} - {wpm:.2f} WPM"
                      for i, (name, wpm) in enumerate(scores[:10])])
    leaderboard_label.config(text=text)


# -----------------------------
# Start Test
# -----------------------------
def start_test():
    global start_time, TEXT

    TEXT = random.choice(SENTENCES)
    text_display.config(state="normal")
    text_display.delete("1.0", tk.END)
    text_display.insert("1.0", TEXT)
    text_display.tag_config("correct", foreground="green")
    text_display.tag_config("wrong", foreground="red")
    text_display.config(state="disabled")

    entry.delete(0, tk.END)
    result_label.config(text="")
    start_time = time.time()


# -----------------------------
# Real-time highlighting
# -----------------------------
def highlight(event=None):
    typed = entry.get()

    text_display.config(state="normal")
    text_display.delete("1.0", tk.END)

    for i, char in enumerate(TEXT):
        if i < len(typed):
            if typed[i] == char:
                text_display.insert(tk.END, char, "correct")
            else:
                text_display.insert(tk.END, char, "wrong")
        else:
            text_display.insert(tk.END, char)

    text_display.config(state="disabled")


# -----------------------------
# Calculate results when Done
# -----------------------------
def calculate_results():
    end_time = time.time()
    typed = entry.get()

    time_taken = end_time - start_time
    words = len(typed.split())
    wpm = (words / time_taken) * 60 if time_taken > 0 else 0

    # Accuracy
    correct_chars = sum(1 for a, b in zip(typed, TEXT) if a == b)
    accuracy = (correct_chars / len(TEXT)) * 100

    # Save score
    name = name_entry.get() or "Player"
    save_score(name, wpm)
    update_leaderboard_display()

    result_label.config(
        text=f"WPM: {wpm:.2f}   |   Accuracy: {accuracy:.2f}%"
    )


# -----------------------------
# GUI
# -----------------------------
root = tk.Tk()
root.title("Typing Speed Test - Upgraded")
root.geometry("700x600")

title = tk.Label(root, text="Typing Speed Test", font=("Arial", 22, "bold"))
title.pack(pady=10)

# Name entry
tk.Label(root, text="Enter your name:", font=("Arial", 14)).pack()
name_entry = tk.Entry(root, width=30, font=("Arial", 14))
name_entry.pack(pady=5)

# Text display (highlightable)
text_display = tk.Text(root, height=3, width=60, font=("Arial", 16), wrap="word")
text_display.pack(pady=10)
text_display.config(state="disabled")

# Input box
entry = tk.Entry(root, width=60, font=("Arial", 16))
entry.pack(pady=10)
entry.bind("<KeyRelease>", highlight)

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack()

tk.Button(btn_frame, text="Start", font=("Arial", 14),
          command=start_test).grid(row=0, column=0, padx=10)

tk.Button(btn_frame, text="Done", font=("Arial", 14),
          command=calculate_results).grid(row=0, column=1, padx=10)

# Result
result_label = tk.Label(root, text="", font=("Arial", 16), fg="blue")
result_label.pack(pady=20)

# Leaderboard
tk.Label(root, text="Leaderboard (Top 10):", font=("Arial", 16, "bold"),
         fg="purple").pack()
leaderboard_label = tk.Label(root, text="", font=("Arial", 14),
                             justify="left")
leaderboard_label.pack()

update_leaderboard_display()

root.mainloop()
