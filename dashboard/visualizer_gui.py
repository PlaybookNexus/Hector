import tkinter as tk
import time
import os
import sys
import threading
from RecoveryManager import RecoveryManager
from datetime import datetime

LOG_PATH = os.path.join(os.path.dirname(__file__), "..", "logs", "motion.log")
LOG_VIEWER_PATH = os.path.join(os.path.dirname(__file__), "recovery.log")

default_font = ("Arial", 12)
default_font_bold = ("Arial", 12, "bold")

def replay_motion_log(scrollable_frame, status_label, lines, start_time=None):
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue

        if start_time:
            try:
                log_time = line.split()[0]
                log_dt = datetime.strptime(log_time, "%H:%M:%S")
                if log_dt < start_time:
                    continue
            except Exception:
                pass

        timestamp = time.strftime("%H:%M:%S")
        if "performing" in line:
            label = tk.Label(scrollable_frame, text=f"\n{line} [{timestamp}]", font=default_font_bold, fg="blue", bg="white", anchor="w", justify="left")
        elif line.startswith("   "):
            label = tk.Label(scrollable_frame, text=line, font=default_font, fg="black", bg="white", anchor="w", justify="left")
        else:
            label = tk.Label(scrollable_frame, text=line, font=default_font, fg="gray", bg="white", anchor="w", justify="left")
        label.pack(anchor="w", padx=10, pady=2)
        scrollable_frame.update()
        scrollable_frame.master.yview_moveto(1.0)
        status_label.config(text=f"Replaying frame {i+1} of {len(lines)} — {timestamp}")
        time.sleep(0.2)

def load_motion_log():
    if not os.path.exists(LOG_PATH):
        return None, "motion.log not found."
    try:
        with open(LOG_PATH, encoding="utf-8") as log:
            lines = log.readlines()
            if not lines:
                return None, "motion.log is empty."
            return lines, None
    except Exception as e:
        return None, f"Error reading motion.log: {e}"

def view_recovery_log():
    log_window = tk.Toplevel()
    log_window.title("Recovery Log")
    log_window.geometry("500x300")
    text = tk.Text(log_window, wrap="word", font=default_font)
    text.pack(fill="both", expand=True)
    try:
        with open(LOG_VIEWER_PATH, "r", encoding="utf-8") as f:
            content = f.read()
            text.insert("1.0", content if content else "No recovery events logged yet.")
    except FileNotFoundError:
        text.insert("1.0", "Recovery log not found.")

def clear_canvas(scrollable_frame, status_label):
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    status_label.config(text="Canvas cleared.")

def load_and_replay(scrollable_frame, status_label, time_entry):
    lines, error = load_motion_log()
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    start_time = None
    time_str = time_entry.get().strip()
    if time_str:
        try:
            start_time = datetime.strptime(time_str, "%H:%M:%S")
        except ValueError:
            status_label.config(text="Invalid time format. Use HH:MM:SS.")
            return

    if error:
        RecoveryManager.trigger_fallback(error)
        status_label.config(text=f"{error} — Fallback mode activated.")
        sample = [
            "Frame 1: x=0, y=0, θ=0",
            "Frame 2: x=1, y=0, θ=15°",
            "Frame 3: x=2, y=1, θ=30°"
        ]
        for line in sample:
            label = tk.Label(scrollable_frame, text=line, font=default_font, fg="gray", bg="white", anchor="w", justify="left")
            label.pack(anchor="w", padx=10, pady=2)
        if not RecoveryManager.cooldown_ready():
            status_label.config(text="Cooldown active — please wait before retrying.")
    else:
        status_label.config(text="Motion log loaded — replaying...")
        replay_motion_log(scrollable_frame, status_label, lines, start_time)

def main():
    root = tk.Tk()
    root.title("Hector Visualizer")
    root.geometry("850x650")

    main_frame = tk.Frame(root)
    main_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(main_frame, bg="white")
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollable_frame = tk.Frame(canvas, bg="white")
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    status_label = tk.Label(root, text="Ready", font=default_font, fg="darkgreen", anchor="w")
    status_label.pack(side="bottom", fill="x")

    button_frame = tk.Frame(root)
    button_frame.pack(side="bottom", pady=10)

    time_label = tk.Label(button_frame, text="Start Time (HH:MM:SS):", font=default_font)
    time_label.pack(side="left", padx=5)

    time_entry = tk.Entry(button_frame, font=default_font, width=10)
    time_entry.pack(side="left", padx=5)

    tk.Button(button_frame, text="Replay", command=lambda: load_and_replay(scrollable_frame, status_label, time_entry), font=default_font).pack(side="left", padx=5)
    tk.Button(button_frame, text="Refresh", command=lambda: load_and_replay(scrollable_frame, status_label, time_entry), font=default_font).pack(side="left", padx=5)
    tk.Button(button_frame, text="Clear", command=lambda: clear_canvas(scrollable_frame, status_label), font=default_font).pack(side="left", padx=5)
    tk.Button(button_frame, text="View Recovery Log", command=view_recovery_log, font=default_font).pack(side="left", padx=5)

    root.mainloop()

if __name__ == "__main__":
    main()