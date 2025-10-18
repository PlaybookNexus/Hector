import tkinter as tk
import time
import os
import threading
from datetime import datetime
from RecoveryManager import RecoveryManager
from ux.theme import DARK_BG, TEXT_COLOR, ACCENT_COLOR, WARNING_COLOR, CRITICAL_COLOR, FONT

LOG_PATH = os.path.join(os.path.dirname(__file__), "..", "logs", "motion.log")
LOG_VIEWER_PATH = os.path.join(os.path.dirname(__file__), "recovery.log")

def replay_motion_log(scrollable_frame, status_label, lines):
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue

        timestamp = time.strftime("%H:%M:%S")
        if "performing" in line:
            label = tk.Label(scrollable_frame, text=f"\n{line} [{timestamp}]",
                             font=FONT, fg=ACCENT_COLOR, bg=DARK_BG, anchor="w", justify="left")
        elif line.startswith("   "):
            label = tk.Label(scrollable_frame, text=line,
                             font=FONT, fg=TEXT_COLOR, bg=DARK_BG, anchor="w", justify="left")
        else:
            label = tk.Label(scrollable_frame, text=line,
                             font=FONT, fg=WARNING_COLOR, bg=DARK_BG, anchor="w", justify="left")
        label.pack(anchor="w", padx=10, pady=2)
        scrollable_frame.update()
        scrollable_frame.master.yview_moveto(1.0)
        status_label.config(text=f"Replaying frame {i+1} of {len(lines)} — {timestamp}", fg=ACCENT_COLOR)

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
    log_window.configure(bg=DARK_BG)

    text = tk.Text(log_window, wrap="word", font=FONT, bg=DARK_BG, fg=TEXT_COLOR)
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
    status_label.config(text="Canvas cleared.", fg=WARNING_COLOR)

def load_and_replay(scrollable_frame, status_label):
    lines, error = load_motion_log()
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    if error:
        RecoveryManager.trigger_fallback(error)
        status_label.config(text=f"{error} — Fallback mode activated.", fg=CRITICAL_COLOR)
        sample = [
            "Frame 1: x=0, y=0, θ=0",
            "Frame 2: x=1, y=0, θ=15 degrees",
            "Frame 3: x=2, y=1, θ=30 degrees"
        ]
        for line in sample:
            label = tk.Label(scrollable_frame, text=line,
                             font=FONT, fg=WARNING_COLOR, bg=DARK_BG, anchor="w", justify="left")
            label.pack(anchor="w", padx=10, pady=2)
        if not RecoveryManager.cooldown_ready():
            status_label.config(text="Cooldown active — please wait before retrying.", fg=WARNING_COLOR)
    else:
        status_label.config(text="Motion log loaded — replaying...", fg=ACCENT_COLOR)
        replay_motion_log(scrollable_frame, status_label, lines)

def main():
    root = tk.Tk()
    root.title("Hector Visualizer")
    root.geometry("850x650")
    root.configure(bg=DARK_BG)

    main_frame = tk.Frame(root, bg=DARK_BG)
    main_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(main_frame, bg=DARK_BG, highlightthickness=0)
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollable_frame = tk.Frame(canvas, bg=DARK_BG)
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    status_label = tk.Label(root, text="Ready", font=FONT, fg=ACCENT_COLOR, bg=DARK_BG, anchor="w")
    status_label.pack(side="bottom", fill="x")

    button_frame = tk.Frame(root, bg=DARK_BG)
    button_frame.pack(side="bottom", pady=10)

    tk.Button(button_frame, text="Replay", command=lambda: load_and_replay(scrollable_frame, status_label),
              font=FONT, bg=ACCENT_COLOR, fg=DARK_BG, width=15).pack(side="left", padx=5)
    tk.Button(button_frame, text="Refresh", command=lambda: load_and_replay(scrollable_frame, status_label),
              font=FONT, bg=ACCENT_COLOR, fg=DARK_BG, width=15).pack(side="left", padx=5)
    tk.Button(button_frame, text="Clear", command=lambda: clear_canvas(scrollable_frame, status_label),
              font=FONT, bg=WARNING_COLOR, fg=DARK_BG, width=15).pack(side="left", padx=5)
    tk.Button(button_frame, text="View Recovery Log", command=view_recovery_log,
              font=FONT, bg="#2196F3", fg=DARK_BG, width=15).pack(side="left", padx=5)

    root.mainloop()

if __name__ == "__main__":
    main()