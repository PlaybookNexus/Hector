import tkinter as tk
import time

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

def load_and_replay(canvas):
    try:
        with open(LOG_PATH, encoding="utf-8") as log:
            lines = log.readlines()
            replay_motion_log(canvas, lines)
    except FileNotFoundError:
        canvas.create_text(10, 20, anchor="nw", text="⚠️ motion.log not found.", font=("Arial", 12))

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