import tkinter as tk
import sys, os, time, threading
from math import cos, sin, radians
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ux.theme import DARK_BG, TEXT_COLOR, ACCENT_COLOR, WARNING_COLOR, CRITICAL_COLOR, FONT

LOG_PATH = os.path.join(os.path.dirname(__file__), "..", "logs", "motion.log")
AGENT_COLORS = {
    "drone": "#00BCD4", "dog": "#FF9800", "car": "#4CAF50",
    "humanoid": "#9C27B0", "arm": "#795548", "boat": "#2196F3"
}

is_playing = False
play_thread = None
sample_agents = {}
mission_seconds = 0
env_type = "urban"

class AgentNode:
    def __init__(self, canvas, agent_id, agent_type, x, y, theta):
        self.canvas = canvas
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.color = AGENT_COLORS.get(agent_type, TEXT_COLOR)
        self.x, self.y, self.theta = x, y, theta
        self.node = canvas.create_oval(x-12, y-12, x+12, y+12, fill=self.color, outline="")
        self.label = canvas.create_text(x, y-18, text=agent_id, font=("Segoe UI", 8), fill=self.color)

    def update(self, x, y, theta):
        self.x, self.y, self.theta = x, y, theta
        self.canvas.coords(self.node, x-12, y-12, x+12, y+12)
        self.canvas.coords(self.label, x, y-18)

def draw_environment(canvas, env):
    canvas.delete("env")
    if env == "urban":
        canvas.create_rectangle(0, 0, 960, 760, fill="#2E2E2E", tags="env")
        canvas.create_text(480, 30, text="🏙️ Urban Zone", font=("Segoe UI", 14), fill="#CCCCCC", tags="env")
    elif env == "forest":
        canvas.create_rectangle(0, 0, 960, 760, fill="#1B5E20", tags="env")
        canvas.create_text(480, 30, text="🌲 Forest Zone", font=("Segoe UI", 14), fill="#EEEEEE", tags="env")
    elif env == "fire_zone":
        canvas.create_rectangle(0, 0, 960, 760, fill="#B71C1C", tags="env")
        canvas.create_text(480, 30, text="🔥 Fire Zone", font=("Segoe UI", 14), fill="#FFFFFF", tags="env")

def parse_motion_log():
    if not os.path.exists(LOG_PATH):
        return [], "motion.log not found."

    frame_groups = []
    current_time = None
    current_agents = []

    try:
        with open(LOG_PATH, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if line.startswith("#"):
                    if current_agents:
                        frame_groups.append((current_time, current_agents))
                        current_agents = []
                    current_time = line[1:].strip()
                    continue
                if ":" not in line:
                    continue
                parts = line.split(":")
                if len(parts) < 2:
                    continue
                agent_id = parts[0].strip()
                data = parts[1].strip()
                if "x=" in data and "y=" in data and "θ=" in data:
                    try:
                        x = float(data.split("x=")[1].split(",")[0])
                        y = float(data.split("y=")[1].split(",")[0])
                        theta = float(data.split("θ=")[1].replace("degrees", "").strip())
                        agent_type = agent_id.split("-")[0]
                        current_agents.append((agent_id, agent_type, x*20+300, y*20+300, theta))
                    except Exception:
                        continue
        if current_agents:
            frame_groups.append((current_time, current_agents))
        return frame_groups, None
    except Exception as e:
        return [], f"Error reading motion.log: {e}"

def replay_frames(canvas, status_label, agents, frame_groups):
    global is_playing
    for i, (timestamp, agent_data) in enumerate(frame_groups):
        if not is_playing:
            status_label.config(text="Paused.", fg=WARNING_COLOR)
            break
        for agent_id, agent_type, x, y, theta in agent_data:
            if agent_id not in agents:
                agents[agent_id] = AgentNode(canvas, agent_id, agent_type, x, y, theta)
            else:
                agents[agent_id].update(x, y, theta)
        status_label.config(text=f"{timestamp} • Frame {i+1}/{len(frame_groups)}", fg=ACCENT_COLOR)
        canvas.update()
        time.sleep(0.5)

def play_motion(canvas, status_label):
    global is_playing, play_thread, mission_seconds
    if is_playing:
        status_label.config(text="Already playing.", fg=WARNING_COLOR)
        return
    frame_groups, error = parse_motion_log()
    if error:
        status_label.config(text=error, fg=CRITICAL_COLOR)
        return
    is_playing = True
    mission_seconds = 0
    draw_environment(canvas, env_type)
    agents = {}
    play_thread = threading.Thread(target=lambda: replay_frames(canvas, status_label, agents, frame_groups))
    play_thread.start()

def pause_motion(status_label):
    global is_playing
    is_playing = False
    status_label.config(text="Paused.", fg=WARNING_COLOR)

def reload_motion(canvas, status_label):
    clear_canvas(canvas, status_label)
    play_motion(canvas, status_label)

def clear_canvas(canvas, status_label):
    global is_playing, sample_agents, mission_seconds
    is_playing = False
    sample_agents = {}
    mission_seconds = 0
    canvas.delete("all")
    status_label.config(text="Canvas cleared.", fg=WARNING_COLOR)

def update_clock(status_label):
    def tick():
        global mission_seconds, is_playing
        if is_playing:
            mission_seconds += 1
            hrs = mission_seconds // 3600
            mins = (mission_seconds % 3600) // 60
            secs = mission_seconds % 60
            status_label.config(text=f"Mission Time: {hrs:02d}:{mins:02d}:{secs:02d}", fg=ACCENT_COLOR)
        status_label.after(1000, tick)
    status_label.after(1000, tick)

def generate_sample_swarm(canvas, status_label, agent_type, count):
    global sample_agents, is_playing, mission_seconds
    clear_canvas(canvas, status_label)
    draw_environment(canvas, env_type)
    sample_agents = {}
    for i in range(count):
        agent_id = f"{agent_type}-{i+1:02d}"
        x = 100 + (i % 5) * 120
        y = 100 + (i // 5) * 120
        theta = (i * 45) % 360
        sample_agents[agent_id] = AgentNode(canvas, agent_id, agent_type, x, y, theta)
    status_label.config(text=f"Generated {count} {agent_type} agents.", fg=ACCENT_COLOR)
    is_playing = True
    mission_seconds = 0
    animate_sample_swarm(canvas)

def animate_sample_swarm(canvas):
    def loop():
        if not is_playing or not sample_agents:
            return
        for agent in sample_agents.values():
            agent.x += 2 * cos(radians(agent.theta))
            agent.y += 2 * sin(radians(agent.theta))
            agent.theta = (agent.theta + 5) % 360
            agent.update(agent.x, agent.y, agent.theta)
        canvas.update()
        canvas.after(200, loop)
    canvas.after(200, loop)

def main():
    global env_type
    root = tk.Tk()
    root.title("Hector Graph Visualizer")
    root.geometry("960x760")
    root.configure(bg=DARK_BG)

    canvas = tk.Canvas(root, bg=DARK_BG, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    status_label = tk.Label(root, text="Ready", font=FONT, fg=ACCENT_COLOR, bg=DARK_BG, anchor="w")
    status_label.pack(side="bottom", fill="x")
    update_clock(status_label)

    config_frame = tk.Frame(root, bg=DARK_BG)
    config_frame.pack(pady=10)

    tk.Label(config_frame, text="Agent Type:", font=FONT, bg=DARK_BG, fg=TEXT_COLOR).grid(row=0, column=0, padx=5)
    agent_type_var = tk.StringVar(value="drone")
    tk.OptionMenu(config_frame, agent_type_var, *AGENT_COLORS.keys()).grid(row=0, column=1, padx=5)

    tk.Label(config_frame, text="Agent Count:", font=FONT, bg=DARK_BG, fg=TEXT_COLOR).grid(row=0, column=2, padx=5)
    agent_count_var = tk.IntVar(value=5)
    tk.Spinbox(config_frame, from_=1, to=20, textvariable=agent_count_var, font=FONT, width=5).grid(row=0, column=3, padx=5)

    tk.Label(config_frame, text="Environment:", font=FONT, bg=DARK_BG, fg=TEXT_COLOR).grid(row=0, column=4, padx=5)
    env_var = tk.StringVar(value="urban")
    tk.OptionMenu(config_frame, env_var, "urban", "forest", "fire_zone").grid(row=0, column=5, padx=5)

    def update_env():
        global env_type
        env_type = env_var.get()
        draw_environment(canvas, env_type)
        status_label.config(text=f"Environment set to {env_type}.", fg=ACCENT_COLOR)

    tk.Button(config_frame, text="🌍 Set Environment", command=update_env,
              font=FONT, bg="#607D8B", fg="white").grid(row=0, column=6, padx=10)

    tk.Button(config_frame, text="🧪 Generate Sample Swarm",
              command=lambda: generate_sample_swarm(canvas, status_label, agent_type_var.get(), agent_count_var.get()),
              font=FONT, bg=ACCENT_COLOR, fg=DARK_BG).grid(row=0, column=7, padx=10)

    button_frame = tk.Frame(root, bg=DARK_BG)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="▶ Play", command=lambda: play_motion(canvas, status_label),
              font=FONT, bg=ACCENT_COLOR, fg=DARK_BG, width=12).pack(side="left", padx=5)

    tk.Button(button_frame, text="⏸ Pause", command=lambda: pause_motion(status_label),
              font=FONT, bg=WARNING_COLOR, fg=DARK_BG, width=12).pack(side="left", padx=5)

    tk.Button(button_frame, text="🔄 Reload", command=lambda: reload_motion(canvas, status_label),
              font=FONT, bg="#2196F3", fg=DARK_BG, width=12).pack(side="left", padx=5)

    tk.Button(button_frame, text="🗑️ Clear", command=lambda: clear_canvas(canvas, status_label),
              font=FONT, bg=CRITICAL_COLOR, fg="white", width=12).pack(side="left", padx=5)

    root.mainloop()

if __name__ == "__main__":
    main()