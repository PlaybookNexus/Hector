import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk
import time
import threading
from datetime import datetime
from RecoveryManager import RecoveryManager
from ux.theme import DARK_BG, TEXT_COLOR, ACCENT_COLOR, WARNING_COLOR, CRITICAL_COLOR, FONT

LOG_PATH = os.path.join(os.path.dirname(__file__), "..", "logs", "motion.log")
LOG_VIEWER_PATH = os.path.join(os.path.dirname(__file__), "recovery.log")

is_playing = False
play_thread = None

def replay_motion_log(scrollable_frame, status_label, lines):
    global is_playing
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    for i, line in enumerate(lines):
        if not is_playing:
            status_label.config(text="Paused.", fg=WARNING_COLOR)
            break

        line = line.strip()
        if not line:
            continue

        timestamp = time.strftime("%H:%M:%S")
        color = ACCENT_COLOR if "performing" in line else TEXT_COLOR if line.startswith("   ") else WARNING_COLOR
        label = tk.Label(scrollable_frame, text=f"{line} [{timestamp}]" if "performing" in line else line,
                         font=FONT, fg=color, bg=DARK_BG, anchor="w", justify="left")
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

def play_motion(scrollable_frame, status_label):
    global is_playing, play_thread
    if is_playing:
        status_label.config(text="Already playing.", fg=WARNING_COLOR)
        return

    lines, error = load_motion_log()
    if error:
        status_label.config(text=error, fg=CRITICAL_COLOR)
        return

    is_playing = True
    play_thread = threading.Thread(target=lambda: replay_motion_log(scrollable_frame, status_label, lines))
    play_thread.start()

def pause_motion(status_label):
    global is_playing
    is_playing = False
    status_label.config(text="Paused.", fg=WARNING_COLOR)

def delete_motion_log(status_label, scrollable_frame):
    global is_playing
    is_playing = False
    try:
        if os.path.exists(LOG_PATH):
            os.remove(LOG_PATH)
            status_label.config(text="motion.log deleted.", fg=CRITICAL_COLOR)
        else:
            status_label.config(text="motion.log not found.", fg=WARNING_COLOR)
    except Exception as e:
        status_label.config(text=f"Error deleting log: {e}", fg=CRITICAL_COLOR)

    clear_canvas(scrollable_frame, status_label)

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
    global is_playing
    is_playing = True
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

def confirm_delete_log(status_label, scrollable_frame):
    confirm_window = tk.Toplevel()
    confirm_window.title("Confirm Log Deletion")
    confirm_window.geometry("400x180")
    confirm_window.configure(bg=DARK_BG)

    tk.Label(confirm_window, text="Delete motion.log?", font=("Segoe UI", 14, "bold"),
             bg=DARK_BG, fg=CRITICAL_COLOR).pack(pady=10)

    tk.Label(confirm_window, text="This will permanently remove the motion log.\nAre you sure?",
             font=FONT, bg=DARK_BG, fg=TEXT_COLOR).pack(pady=5)

    button_frame = tk.Frame(confirm_window, bg=DARK_BG)
    button_frame.pack(pady=10)

    def confirm():
        delete_motion_log(status_label, scrollable_frame)
        confirm_window.destroy()

    def cancel():
        status_label.config(text="Deletion cancelled.", fg=WARNING_COLOR)
        confirm_window.destroy()

    tk.Button(button_frame, text="Delete", command=confirm,
              font=FONT, bg=CRITICAL_COLOR, fg="white", width=10).pack(side="left", padx=10)
    tk.Button(button_frame, text="Cancel", command=cancel,
              font=FONT, bg=ACCENT_COLOR, fg=DARK_BG, width=10).pack(side="left", padx=10)

def main():
    root = tk.Tk()
    root.title("Hector Visualizer")
    root.geometry("880x650")
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

    tk.Button(button_frame, text="▶ Play", command=lambda: play_motion(scrollable_frame, status_label),
              font=FONT, bg=ACCENT_COLOR, fg=DARK_BG, width=15).pack(side="left", padx=5)
    tk.Button(button_frame, text="Pause", command=lambda: pause_motion(status_label),
              font=FONT, bg=WARNING_COLOR, fg=DARK_BG, width=15).pack(side="left", padx=5)
    tk.Button(button_frame, text="Delete Log", command=lambda: confirm_delete_log(status_label, scrollable_frame),
              font=FONT, bg=CRITICAL_COLOR, fg="white", width=15).pack(side="left", padx=5)
    tk.Button(button_frame, text="View Recovery Log", command=view_recovery_log,
              font=FONT, bg="#2196F3", fg=DARK_BG, width=15).pack(side="left", padx=5)

    root.mainloop()

if __name__ == "__main__":
    main()