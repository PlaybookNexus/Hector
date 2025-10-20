import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import subprocess
import sys
import io
import os
import re
import logging

from ux.theme import DARK_BG, TEXT_COLOR, ACCENT_COLOR, WARNING_COLOR, CRITICAL_COLOR, FONT

# Strip ANSI escape codes
ANSI_ESCAPE = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Configure motion log
logging.basicConfig(
    filename="logs/motion.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

class TextRedirector(io.TextIOBase):
    def __init__(self, widget):
        self.widget = widget

    def write(self, message):
        clean_msg = ANSI_ESCAPE.sub('', message).strip()
        if clean_msg:
            logging.info(clean_msg)
        self.widget.configure(state='normal')
        self.widget.insert(tk.END, clean_msg + "\n")
        self.widget.see(tk.END)
        self.widget.configure(state='disabled')

    def flush(self):
        pass

def get_version_info():
    try:
        commit = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], text=True).strip()
        date = subprocess.check_output(["git", "log", "-1", "--format=%cd", "--date=short"], text=True).strip()
        return f"Version: {commit} • Updated: {date}"
    except Exception:
        return "Version info unavailable"

def launch_hector():
    def run():
        try:
            os.environ["HECTOR_THEATRE"] = THEATRE_MAP[selected_theatre.get()]
            os.environ["HECTOR_DURATION"] = str(mission_duration.get())
            os.environ["HECTOR_RISK_THRESHOLD"] = risk_threshold.get()
            os.environ["HECTOR_ENV_PROFILE"] = env_profile.get()

            config_str = ",".join(
                f"{atype.get()}:{acount.get()}"
                for atype, acount in agent_config
                if atype and acount
            )
            os.environ["HECTOR_AGENT_CONFIG"] = config_str

            update_preview()

            status_label.config(text="Launching Hector mesh...", fg=ACCENT_COLOR)
            output_box.configure(state='normal')
            output_box.delete(1.0, tk.END)
            output_box.configure(state='disabled')

            redirector = TextRedirector(output_box)
            sys.stdout = redirector
            sys.stderr = redirector

            print(f"Selected theatre: {selected_theatre.get()}")
            print(f"Agent config: {config_str}")
            print("Launching Hector mesh...\n")

            from main import main
            main()

            print("\nAutonomy loop completed.")
            status_label.config(text="Hector finished his routine.", fg=TEXT_COLOR)
            messagebox.showinfo("Hector Mission Control", "Hector completed his mission.")
        except Exception as e:
            status_label.config(text="Error during execution.", fg=CRITICAL_COLOR)
            messagebox.showerror("Error", f"Failed to run Hector:\n{e}")

    threading.Thread(target=run).start()

def clear_output():
    output_box.configure(state='normal')
    output_box.delete(1.0, tk.END)
    output_box.configure(state='disabled')
    status_label.config(text="Output cleared.", fg=WARNING_COLOR)

def launch_visualizer():
    try:
        subprocess.Popen(["python", "dashboard/visualizer_gui.py"])
        status_label.config(text="Visualizer launched.", fg=ACCENT_COLOR)
    except Exception as e:
        status_label.config(text="Failed to launch visualizer.", fg=CRITICAL_COLOR)
        messagebox.showerror("Error", f"Could not launch visualizer:\n{e}")

def run_git_pull():
    def pull():
        try:
            status_label.config(text="Updating from Git...", fg=ACCENT_COLOR)
            output_box.configure(state='normal')
            output_box.insert(tk.END, "\nRunning: git pull\n")
            output_box.configure(state='disabled')

            result = subprocess.run(["git", "pull"], capture_output=True, text=True)
            output_box.configure(state='normal')
            output_box.insert(tk.END, result.stdout + result.stderr)
            output_box.configure(state='disabled')

            status_label.config(text="Update complete.", fg=TEXT_COLOR)
            version_label.config(text=get_version_info())
        except Exception as e:
            status_label.config(text="Git update failed.", fg=CRITICAL_COLOR)
            messagebox.showerror("Git Error", f"Failed to pull updates:\n{e}")

    threading.Thread(target=pull).start()

# GUI setup
root = tk.Tk()
root.title("Hector Mission Control")
root.geometry("720x800")
root.resizable(False, False)
root.configure(bg=DARK_BG)

THEATRE_MAP = {
    "Search and Rescue": "search_and_rescue",
    "Firefighting": "firefighting",
    "Combat Ops": "combat_ops"
}

selected_theatre = tk.StringVar(value="Search and Rescue")
mission_duration = tk.IntVar(value=15)
risk_threshold = tk.StringVar(value="medium")
env_profile = tk.StringVar(value="urban")
agent_config = []

# Title and version
tk.Label(root, text="Mission Control", font=("Segoe UI", 16, "bold"),
         bg=DARK_BG, fg=ACCENT_COLOR).pack(pady=10)

version_label = tk.Label(root, text=get_version_info(), font=("Segoe UI", 10),
                         bg=DARK_BG, fg=TEXT_COLOR)
version_label.pack(pady=(0, 10))

# Mission type selector
theatre_frame = tk.Frame(root, bg=DARK_BG)
theatre_frame.pack(pady=5)

tk.Label(theatre_frame, text="Choose Mission Type:", font=FONT,
         bg=DARK_BG, fg=TEXT_COLOR).pack(side="left", padx=5)

theatre_dropdown = tk.OptionMenu(theatre_frame, selected_theatre,
                                 *THEATRE_MAP.keys())
theatre_dropdown.config(font=FONT, bg="#1E1E1E", fg=TEXT_COLOR, width=20)
theatre_dropdown.pack(side="left", padx=5)

# Mission parameters
param_frame = tk.Frame(root, bg=DARK_BG)
param_frame.pack(pady=5)

tk.Label(param_frame, text="Duration (min):", font=FONT, bg=DARK_BG, fg=TEXT_COLOR).grid(row=0, column=0, padx=5, pady=2, sticky="w")
tk.Spinbox(param_frame, from_=1, to=999, textvariable=mission_duration, font=FONT, width=5).grid(row=0, column=1, padx=5, pady=2)

tk.Label(param_frame, text="Risk Threshold:", font=FONT, bg=DARK_BG, fg=TEXT_COLOR).grid(row=1, column=0, padx=5, pady=2, sticky="w")
tk.OptionMenu(param_frame, risk_threshold, "low", "medium", "high").grid(row=1, column=1, padx=5, pady=2)

tk.Label(param_frame, text="Environment:", font=FONT, bg=DARK_BG, fg=TEXT_COLOR).grid(row=2, column=0, padx=5, pady=2, sticky="w")
tk.OptionMenu(param_frame, env_profile, "urban", "forest", "fire_zone").grid(row=2, column=1, padx=5, pady=2)

# Agent swarm config
agent_frame = tk.Frame(root, bg=DARK_BG)
agent_frame.pack(pady=5)

tk.Label(agent_frame, text="Agent Swarm:", font=FONT, bg=DARK_BG, fg=TEXT_COLOR).grid(row=0, column=0, columnspan=3, pady=(0, 5))

# Swarm Preview Panel
preview_frame = tk.Frame(root, bg=DARK_BG)
preview_frame.pack(pady=5)

tk.Label(preview_frame, text="Swarm Preview:", font=FONT, bg=DARK_BG, fg=TEXT_COLOR).pack(anchor="w", padx=5)

preview_box = scrolledtext.ScrolledText(preview_frame, wrap=tk.WORD, font=FONT,
                                        width=60, height=6, state='disabled',
                                        bg="#1E1E1E", fg=TEXT_COLOR)
preview_box.pack(padx=5, pady=5)

def update_preview():
    preview_box.configure(state='normal')
    preview_box.delete(1.0, tk.END)

    for i, (atype, acount) in enumerate(agent_config):
        if atype and acount:
            try:
                count = int(acount.get())
                for j in range(count):
                    agent_id = f"{atype.get()}-{j+1:02d}"
                    preview_box.insert(tk.END, f"🟢 {agent_id}\n")
            except ValueError:
                preview_box.insert(tk.END, f"⚠️ Invalid count for {atype.get()}\n")

    preview_box.configure(state='disabled')

def add_agent_row():
    row = len(agent_config) + 1
    agent_type_var = tk.StringVar(value="drone")
    agent_count_var = tk.StringVar(value="1")

    tk.OptionMenu(agent_frame, agent_type_var, "drone", "dog", "car", "humanoid", "arm", "boat").grid(row=row, column=0, padx=5)
    tk.Entry(agent_frame, textvariable=agent_count_var, font=FONT, width=5).grid(row=row, column=1, padx=5)
    tk.Button(agent_frame, text="Remove", command=lambda: remove_agent_row(row), font=FONT, bg=WARNING_COLOR, fg=DARK_BG).grid(row=row, column=2, padx=5)

    agent_config.append((agent_type_var, agent_count_var))
    update_preview()

def remove_agent_row(index):
    for widget in agent_frame.grid_slaves(row=index):
        widget.destroy()
    agent_config[index - 1] = None
    update_preview()

tk.Button(agent_frame, text="Add Agent", command=add_agent_row, font=FONT, bg=ACCENT_COLOR, fg=DARK_BG).grid(row=99, column=0, columnspan=3, pady=5)
add_agent_row()

# Buttons
button_frame = tk.Frame(root, bg=DARK_BG)
button_frame.pack(pady=5)

tk.Button(button_frame, text="Start Mission", command=launch_hector,
          font=FONT, bg=ACCENT_COLOR, fg=DARK_BG, width=15).pack(side="left", padx=5)

tk.Button(button_frame, text="Clear Output", command=clear_output,
          font=FONT, bg=WARNING_COLOR, fg=DARK_BG, width=15).pack(side="left", padx=5)

tk.Button(button_frame, text="View Log", command=launch_visualizer,
          font=FONT, bg="#2196F3", fg=DARK_BG, width=15).pack(side="left", padx=5)

tk.Button(button_frame, text="Update Hector", command=run_git_pull,
          font=FONT, bg="#9C27B0", fg="white", width=15).pack(side="left", padx=5)

# Output box
output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=FONT,
                                       width=70, height=20, state='disabled',
                                       bg="#1E1E1E", fg=TEXT_COLOR)
output_box.pack(pady=10)

# Status label
status_label = tk.Label(root, text="Ready", font=FONT, fg=ACCENT_COLOR,
                        bg=DARK_BG, anchor="w")
status_label.pack(side="bottom", fill="x")

# Launch GUI
root.mainloop()