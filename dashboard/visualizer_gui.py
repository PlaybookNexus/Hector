import tkinter as tk
import time
import os

LOG_PATH = os.path.join(os.path.dirname(__file__), "..", "logs", "motion.log")

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

def load_and_replay(canvas):
    lines, error = load_motion_log()
    canvas.delete("all")
    if error:
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
    else:
        replay_motion_log(canvas, lines)

def main():
    root = tk.Tk()
    root.title("🧠 Hector Visualizer")
    root.geometry("600x400")

    canvas = tk.Canvas(root, bg="white")
    canvas.pack(fill="both", expand=True)

    replay_button = tk.Button(root, text="▶️ Replay Motions", command=lambda: load_and_replay(canvas))
    replay_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()