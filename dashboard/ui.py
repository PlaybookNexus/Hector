import time
from dashboard.motions import motions
from utils.logger import log_motion  # Centralized logging
from datetime import datetime

def color_risk(risk):
    color_map = {
        "low": "\033[92m",       # Green
        "high": "\033[93m",      # Yellow
        "critical": "\033[91m"   # Red
    }
    return f"{color_map.get(risk, '')}{risk}\033[0m" if risk in color_map else risk

def render_dashboard(graph):
    print("\n🧠 Hector Override Dashboard")
    print("-" * 40)
    for agent_id, agent in graph.agents.items():
        agent_type = agent.__class__.__name__
        status = getattr(agent, "status", "unknown")
        task = getattr(agent, "task", "—")
        risk = color_risk(agent.vector_state.get("risk", "unknown"))
        last = agent.vector_state.get("last_action", "none")
        override = agent.vector_state.get("status", "")

        print(f"🟢 {agent_id} ({agent_type})")
        print(f"   Task: {task}")
        print(f"   Status: {status}")
        print(f"   Risk: {risk}")
        print(f"   Last Action: {last}")
        if override:
            print(f"   Override Status: {override}")
        print("-" * 40)

def animate_motion(agent_id, routine):
    frames = motions.get(routine, [])
    print(f"\n🎭 {agent_id} performing {routine} routine...")
    for frame in frames:
        print(f"   {frame}")
        time.sleep(0.3)

    log_motion(agent_id, routine, frames)