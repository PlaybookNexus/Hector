import tkinter as tk
import time
import os
import subprocess
from RecoveryManager import RecoveryManager

LOG_PATH = os.path.join(os.path.dirname(__file__), "..", "logs", "motion.log")
MAIN_PATH = os.path.join(os.path.dirname(__file__), "..", "main.py")

def replay_motion_log(canvas, lines):
    canvas.delete("all")
    y = 20
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if "performing" in line:
            canvas.create_text(10, y, anchor="nw", text=f"\n{line}", font=("Arial", 12, "bold"))
            y += 30
        elif line.startswith("   "):
            canvas.create_text(30, y, anchor="nw", text=line, font=("Arial", 12))
            y += 25
            canvas.update()
            time.sleep(0.3)

def load_motion_log():
    if not os.path.exists(LOG_PATH):
        return None, "⚠️ motion.log not found."
    try:
        with open(LOG_PATH, encoding="utf-8") as log:
            lines = log.readlines()
            if not lines:
                return None, "⚠️ motion.log is empty."
            return lines, None
    except Exception as e:
        return None, f"⚠️ Error reading motion.log: {e}"

def launch_main():
    try:
        subprocess.Popen(["python3", MAIN_PATH])
    except Exception as e:
        print(f"Error launching main.py: {e}")

def load_and_replay(canvas, launch_btn, cooldown_label):
    lines, error = load_motion_log()
    canvas.delete("all")
    launch_btn.pack_forget()
    cooldown_label.pack_forget()

    if error:
        RecoveryManager.trigger_fallback(error)
        canvas.create_text(10, 20, anchor="nw", text=f"{error}\nFallback mode activated.", font=("Arial", 12), fill="red")

        sample = [
            "Frame 1: x=0, y=0, θ=0",
            "Frame 2: x=1, y=0, θ=15°",
            "Frame 3: x=2, y=1, θ=30°"
        ]
        y = 80
        for line in sample:
            canvas.create_text(30, y, anchor="nw", text=line, font=("Arial", 12), fill="gray")
            y += 25

        launch_btn.pack(pady=10)

        if not RecoveryManager.cooldown_ready():
            cooldown_label.config(text="⏱️ Cooldown active — please wait before retrying.")
            cooldown_label.pack(pady=5)
    else:
        replay_motion_log(canvas, lines)

def main():
    root = tk.Tk()
    root.title("🧠 Hector Visualizer")
    root.geometry("600x400")

    canvas = tk.Canvas(root, bg="white")
    canvas.pack(fill="both", expand=True)

    launch_btn = tk.Button(root, text="🛠️ Run main.py to generate log", command=launch_main)
    cooldown_label = tk.Label(root, text="", font=("Arial", 10), fg="orange")

    replay_btn = tk.Button(root, text="▶️ Replay Motions", command=lambda: load_and_replay(canvas, launch_btn, cooldown_label))
    replay_btn.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()