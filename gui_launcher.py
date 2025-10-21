import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import subprocess
import sys
import io
import os
import re
import logging
from math import sin, cos
from datetime import datetime, timedelta
import time

from ux.theme import DARK_BG, TEXT_COLOR, ACCENT_COLOR, WARNING_COLOR, CRITICAL_COLOR, FONT

ANSI_ESCAPE = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/motion.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

AGENT_COLORS = {
    "drone": "#00BCD4", "dog": "#FF9800", "car": "#4CAF50",
    "humanoid": "#9C27B0", "arm": "#795548", "boat": "#2196F3"
}

live_agents = {}

class LiveAgentNode:
    def __init__(self, canvas, agent_id, agent_type, x, y, theta):
        self.canvas = canvas
        self.agent_id = agent_id
        self.color = AGENT_COLORS.get(agent_type, TEXT_COLOR)
        self.node = canvas.create_oval(x-10, y-10, x+10, y+10, fill=self.color, outline="")
        self.label = canvas.create_text(x, y-16, text=agent_id, font=("Segoe UI", 8), fill=self.color)

    def update(self, x, y, theta):
        self.canvas.coords(self.node, x-10, y-10, x+10, y+10)
        self.canvas.coords(self.label, x, y-16)

def draw_env_background(canvas, env):
    canvas.delete("bg")
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    color = {"urban": "#2E2E2E", "forest": "#1B5E20", "fire_zone": "#B71C1C"}.get(env, "#2E2E2E")
    canvas.create_rectangle(0, 0, width, height, fill=color, tags="bg")
    canvas.create_text(width // 2, 20, text=f"Environment: {env}", font=("Segoe UI", 12), fill="#FFFFFF", tags="bg")
    
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
            theatre = THEATRE_MAP[selected_theatre.get()]
            duration = mission_duration.get()
            env = env_profile.get()
            risk = risk_threshold.get()

            agents = []
            for entry in agent_config:
                if entry:
                    atype, acount = entry
                    try:
                        count = int(acount.get())
                        for i in range(count):
                            agents.append((atype.get(), f"{atype.get()}-{i+1:02d}"))
                    except ValueError:
                        continue

            update_preview()
            status_label.config(text="Generating mission log...", fg=ACCENT_COLOR)
            output_box.configure(state='normal')
            output_box.delete(1.0, tk.END)
            output_box.configure(state='disabled')
            visualizer_canvas.delete("all")
            live_agents.clear()
            draw_env_background(visualizer_canvas, env)

            redirector = TextRedirector(output_box)
            sys.stdout = redirector
            sys.stderr = redirector

            print(f"Selected theatre: {selected_theatre.get()}")
            print(f"Agent config: {[aid for _, aid in agents]}")
            print("Generating motion.log...\n")

            with open("logs/motion.log", "w", encoding="utf-8") as f:
                start_time = datetime.now()
                for t in range(duration * 30):
                    timestamp = start_time + timedelta(seconds=t * 2)
                    f.write(f"# {timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n")

                    for atype, aid in agents:
                        i = int(aid.split("-")[-1]) - 1  # agent index
                        zone_offset = i * 8

                        # Base patrol orbit
                        x = zone_offset + sin(t / 10 + i) * 6
                        y = zone_offset + cos(t / 10 + i) * 6

                        # Mission-specific behavior
                        if theatre == "search_and_rescue":
                            x += sin((t + i * 3) / 15) * 4
                            y += cos((t + i * 2) / 18) * 4
                        elif theatre == "firefighting":
                            x += (i % 3) * 5 + sin(t / 3) * 2
                            y += (i % 2) * 3 + cos(t / 4) * 2
                        elif theatre == "combat_ops":
                            x += ((-1)**i) * t * 0.2
                            y += ((-1)**(i+1)) * t * 0.2

                        theta = (t * 12 + i * 30) % 360
                        
                        f.write(f"{aid}: x={x:.2f}, y={y:.2f}, θ={theta:.1f} degrees\n")

                        canvas_width = visualizer_canvas.winfo_width()
                        canvas_height = visualizer_canvas.winfo_height()

                        # Normalize x and y to fit within canvas
                        cx = (x % (canvas_width / 20)) * 20
                        cy = (y % (canvas_height / 20)) * 20
                        if aid not in live_agents:
                            live_agents[aid] = LiveAgentNode(visualizer_canvas, aid, atype, cx, cy, theta)
                        else:
                            live_agents[aid].update(cx, cy, theta)
                    visualizer_canvas.update()
                    time.sleep(0.2)

            print("\nMission log generated.")
            status_label.config(text="Mission log ready for replay.", fg=TEXT_COLOR)
            messagebox.showinfo("Hector Mission Control", "motion.log generated successfully.")
        except Exception as e:
            status_label.config(text="Error during mission generation.", fg=CRITICAL_COLOR)
            messagebox.showerror("Error", f"Failed to generate motion log:\n{e}")

    threading.Thread(target=run).start()

def clear_output():
    output_box.configure(state='normal')
    output_box.delete(1.0, tk.END)
    output_box.configure(state='disabled')
    visualizer_canvas.delete("all")
    live_agents.clear()
    status_label.config(text="Output cleared.", fg=WARNING_COLOR)

def launch_visualizer():
    try:
        subprocess.Popen(["python", "dashboard/graph_visualizer.py"])
        status_label.config(text="Graph Visualizer launched.", fg=ACCENT_COLOR)
    except Exception as e:
        status_label.config(text="Failed to launch Graph Visualizer.", fg=CRITICAL_COLOR)
        messagebox.showerror("Error", f"Could not launch Graph Visualizer:\n{e}")

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
root.geometry("1280x720")
root.configure(bg=DARK_BG)

THEATRE_MAP = {
    "Search and Rescue": "search_and_rescue",
    "Firefighting": "firefighting",
    "Combat Ops": "combat_ops"
}

selected_theatre = tk.StringVar(value="Search and Rescue")
mission_duration = tk.IntVar(value=4)
risk_threshold = tk.StringVar(value="medium")
env_profile = tk.StringVar(value="urban")
agent_config = []

# Main layout
main_frame = tk.Frame(root, bg=DARK_BG)
main_frame.pack(fill="both", expand=True)

left_panel = tk.Frame(main_frame, bg=DARK_BG)
left_panel.pack(side="left", fill="y", padx=10, pady=10)

right_panel = tk.Frame(main_frame, bg=DARK_BG)
right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# Left panel content
# Left panel content (continued)
tk.Label(left_panel, text="Mission Control", font=("Segoe UI", 16, "bold"),
         bg=DARK_BG, fg=ACCENT_COLOR).pack(pady=10)

version_label = tk.Label(left_panel, text=get_version_info(), font=("Segoe UI", 10),
                         bg=DARK_BG, fg=TEXT_COLOR)
version_label.pack(pady=(0, 10))

# Mission type selector
theatre_frame = tk.Frame(left_panel, bg=DARK_BG)
theatre_frame.pack(pady=5)

tk.Label(theatre_frame, text="Choose Mission Type:", font=FONT,
         bg=DARK_BG, fg=TEXT_COLOR).pack(side="left", padx=5)

theatre_dropdown = tk.OptionMenu(theatre_frame, selected_theatre, *THEATRE_MAP.keys())
theatre_dropdown.config(font=FONT, bg="#1E1E1E", fg=TEXT_COLOR, width=20)
theatre_dropdown.pack(side="left", padx=5)

# Mission parameters
param_frame = tk.Frame(left_panel, bg=DARK_BG)
param_frame.pack(pady=5)

tk.Label(param_frame, text="Duration (min):", font=FONT, bg=DARK_BG, fg=TEXT_COLOR).grid(row=0, column=0, padx=5, pady=2, sticky="w")
tk.Spinbox(param_frame, from_=1, to=999, textvariable=mission_duration, font=FONT, width=5).grid(row=0, column=1, padx=5, pady=2)

tk.Label(param_frame, text="Risk Threshold:", font=FONT, bg=DARK_BG, fg=TEXT_COLOR).grid(row=1, column=0, padx=5, pady=2, sticky="w")
tk.OptionMenu(param_frame, risk_threshold, "low", "medium", "high").grid(row=1, column=1, padx=5, pady=2)

tk.Label(param_frame, text="Environment:", font=FONT, bg=DARK_BG, fg=TEXT_COLOR).grid(row=2, column=0, padx=5, pady=2, sticky="w")
tk.OptionMenu(param_frame, env_profile, "urban", "forest", "fire_zone").grid(row=2, column=1, padx=5, pady=2)

# Agent swarm config
agent_frame = tk.Frame(left_panel, bg=DARK_BG)
agent_frame.pack(pady=5)

tk.Label(agent_frame, text="Agent Swarm:", font=FONT, bg=DARK_BG, fg=TEXT_COLOR).grid(row=0, column=0, columnspan=3, pady=(0, 5))

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

    tk.OptionMenu(agent_frame, agent_type_var, *AGENT_COLORS.keys()).grid(row=row, column=0, padx=5)
    tk.Entry(agent_frame, textvariable=agent_count_var, font=FONT, width=5).grid(row=row, column=1, padx=5)
    tk.Button(agent_frame, text="Remove", command=lambda: remove_agent_row(row), font=FONT, bg=WARNING_COLOR, fg=DARK_BG).grid(row=row, column=2, padx=5)

    agent_config.append((agent_type_var, agent_count_var))
    update_preview()

def remove_agent_row(index):
    for widget in agent_frame.grid_slaves(row=index):
        widget.destroy()
    agent_config[index - 1] = None
    agent_config[:] = [entry for entry in agent_config if entry is not None]
    update_preview()

tk.Button(agent_frame, text="Add Agent", command=add_agent_row, font=FONT, bg=ACCENT_COLOR, fg=DARK_BG).grid(row=99, column=0, columnspan=3, pady=5)

# Swarm Preview Panel
preview_frame = tk.Frame(left_panel, bg=DARK_BG)
preview_frame.pack(pady=5)

tk.Label(preview_frame, text="Swarm Preview:", font=FONT, bg=DARK_BG, fg=TEXT_COLOR).pack(anchor="w", padx=5)

preview_box = scrolledtext.ScrolledText(
    preview_frame,
    wrap=tk.WORD,
    font=FONT,
    width=40,
    height=6,
    state='disabled',
    bg="#1E1E1E",
    fg=TEXT_COLOR
)
preview_box.pack(padx=5, pady=5)

add_agent_row()

# Control Buttons
button_frame = tk.Frame(left_panel, bg=DARK_BG)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Start Mission", command=launch_hector,
          font=FONT, bg=ACCENT_COLOR, fg=DARK_BG, width=15).pack(side="left", padx=5)

tk.Button(button_frame, text="Clear Output", command=clear_output,
          font=FONT, bg=WARNING_COLOR, fg=DARK_BG, width=15).pack(side="left", padx=5)

tk.Button(button_frame, text="View Log", command=launch_visualizer,
          font=FONT, bg="#2196F3", fg=DARK_BG, width=15).pack(side="left", padx=5)

tk.Button(button_frame, text="Update Hector", command=run_git_pull,
          font=FONT, bg="#9C27B0", fg="white", width=15).pack(side="left", padx=5)

# Right panel content
tk.Label(right_panel, text="Live Visualizer:", font=FONT, bg=DARK_BG, fg=TEXT_COLOR).pack(anchor="w", padx=5, pady=(0, 5))

visualizer_canvas = tk.Canvas(right_panel, bg="#1E1E1E", width=680, height=360, highlightthickness=0)
visualizer_canvas.pack(padx=5, pady=5, fill="both", expand=True)

tk.Label(right_panel, text="Mission Log Output:", font=FONT, bg=DARK_BG, fg=TEXT_COLOR).pack(anchor="w", padx=5, pady=(10, 0))

output_box = scrolledtext.ScrolledText(
    right_panel,
    wrap=tk.WORD,
    font=FONT,
    width=70,
    height=12,
    state='disabled',
    bg="#1E1E1E",
    fg=TEXT_COLOR
)
output_box.pack(padx=5, pady=5, fill="both", expand=True)

# Status label
status_label = tk.Label(root, text="Ready", font=FONT, fg=ACCENT_COLOR, bg=DARK_BG, anchor="w")
status_label.pack(side="bottom", fill="x")

# Launch GUI
root.mainloop()