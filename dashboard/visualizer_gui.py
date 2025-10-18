import tkinter as tk
import time
import os
import sys
import threading
import subprocess
from RecoveryManager import RecoveryManager

LOG_PATH = os.path.join(os.path.dirname(__file__), "..", "logs", "motion.log")
MAIN_PATH = os.path.join(os.path.dirname(__file__), "..", "main.py")
LOG_VIEWER_PATH = os.path.join(os.path.dirname(__file__), "recovery.log")

def replay_motion_log(canvas, status_label, lines):
    canvas.delete("all")
    y = 20
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        timestamp = time.strftime("%H:%M:%S")
        if "performing" in line:
            canvas.create_text(10, y, anchor="nw", text=f"\n{line} [{timestamp}]", font=("Arial", 12, "bold"), fill="blue")
            y += 30
        elif line.startswith("   "):
            canvas.create_text(30, y, anchor="nw", text=f"{line}", font=("Arial", 12), fill="black")
            y += 25
        else:
            canvas.create_text(30, y, anchor="nw", text=f"{line}", font=("Arial", 12), fill="gray")
            y += 25
        canvas.update()
        status_label.config(text=f"✅ Replaying frame {i+1} of {len(lines)} — {timestamp}")
        time.sleep(0.2)

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

def run_main_and_stream(canvas, status_label):
    canvas.delete("all")
    status_label.config(text="🛠️ Running main.py — streaming output...")

    def stream():
        try:
            process = subprocess.Popen(
                ["python", MAIN_PATH],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8"
            )

            y = 20
            for i, line in enumerate(process.stdout):
                line = line.strip()
                if not line:
                    continue
                timestamp = time.strftime("%H:%M:%S")
                if "performing" in line:
                    canvas.create_text(10, y, anchor="nw", text=f"\n{line} [{timestamp}]", font=("Arial", 12, "bold"), fill="blue")
                    y += 30
                elif line.startswith("   "):
                    canvas.create_text(30, y, anchor="nw", text=line, font=("Arial", 12), fill="black")
                    y += 25
                else:
                    canvas.create_text(30, y, anchor="nw", text=line, font=("Arial", 12), fill="gray")
                    y += 25
                canvas.update()
                status_label.config(text=f"📡 Frame {i+1} — {timestamp}")
                time.sleep(0.2)

            process.wait()
            status_label.config(text="✅ main.py completed — loading motion log...")
            time.sleep(0.5)
            lines, error = load_motion_log()
            if error:
                status_label.config(text=f"{error} — fallback mode activated.")
                RecoveryManager.trigger_fallback(error)
            else:
                status_label.config(text="✅ Motion log loaded — replaying...")
                replay_motion_log(canvas, status_label, lines)

        except Exception as e:
            status_label.config(text=f"❌ Failed to run main.py: {e}")

    threading.Thread(target=stream).start()

def view_recovery_log():
    log_window = tk.Toplevel()
    log_window.title("📜 Recovery Log")
    log_window.geometry("500x300")
    text = tk.Text(log_window, wrap="word")
    text.pack(fill="both", expand=True)
    try:
        with open(LOG_VIEWER_PATH, "r", encoding="utf-8") as f:
            content = f.read()
            text.insert("1.0", content if content else "No recovery events logged yet.")
    except FileNotFoundError:
        text.insert("1.0", "Recovery log not found.")

def clear_canvas(canvas, status_label):
    canvas.delete("all")
    status_label.config(text="🧹 Canvas cleared.")

def load_and_replay(canvas, status_label):
    lines, error = load_motion_log()
    canvas.delete("all")

    if error:
        RecoveryManager.trigger_fallback(error)
        status_label.config(text=f"{error} — Fallback mode activated.")
        sample = [
            "Frame 1: x=0, y=0, θ=0",
            "Frame 2: x=1, y=0, θ=15°",
            "Frame 3: x=2, y=1, θ=30°"
        ]
        y = 80
        for line in sample:
            canvas.create_text(30, y, anchor="nw", text=line, font=("Arial", 12), fill="gray")
            y += 25
        if not RecoveryManager.cooldown_ready():
            status_label.config(text="⏱️ Cooldown active — please wait before retrying.")
    else:
        status_label.config(text="✅ Motion log loaded — replaying...")
        replay_motion_log(canvas, status_label, lines)

def main():
    root = tk.Tk()
    root.title("🧠 Hector Visualizer")
    root.geometry("800x600")

    main_frame = tk.Frame(root)
    main_frame.pack(fill="both", expand=True)

    canvas_frame = tk.Frame(main_frame)
    canvas_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(canvas_frame, bg="white")
    scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    status_label = tk.Label(root, text="🧭 Ready", font=("Arial", 10), fg="darkgreen", anchor="w")
    status_label.pack(side="bottom", fill="x")

    button_frame = tk.Frame(root)
    button_frame.pack(side="bottom", pady=10)

    tk.Button(button_frame, text="▶️ Replay", command=lambda: load_and_replay(canvas, status_label)).pack(side="left", padx=5)
    tk.Button(button_frame, text="🛠️ Run main.py", command=lambda: run_main_and_stream(canvas, status_label)).pack(side="left", padx=5)
    tk.Button(button_frame, text="🔄 Refresh", command=lambda: load_and_replay(canvas, status_label)).pack(side="left", padx=5)
    tk.Button(button_frame, text="🧹 Clear", command=lambda: clear_canvas(canvas, status_label)).pack(side="left", padx=5)
    tk.Button(button_frame, text="📜 View Recovery Log", command=view_recovery_log).pack(side="left", padx=5)

    root.mainloop()

if __name__ == "__main__":
    main()