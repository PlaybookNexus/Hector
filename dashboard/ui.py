import time
from datetime import datetime
from dashboard.motions import motions

def color_risk(risk):
    colors = {
        "low": "\033[92m",       # Green
        "high": "\033[93m",      # Yellow
        "critical": "\033[91m"   # Red
    }
    color = colors.get(risk, "")
    return f"{color}{risk}\033[0m" if color else risk

def render_dashboard(graph):
    print("\n🧠 Hector Override Dashboard")
    print("-" * 40)
    for agent_id, agent in graph.agents.items():
        agent_type = agent.__class__.__name__
        status = getattr(agent, "status", "unknown")
        task = getattr(agent, "task", "—")
        risk_raw = agent.vector_state.get("risk", "unknown")
        risk = color_risk(risk_raw)
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
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_lines = [f"[{timestamp}] {agent_id} performing {routine} routine"]

    print(f"\n🎭 {agent_id} performing {routine} routine...")
    for frame in motions.get(routine, []):
        print(f"   {frame}")
        log_lines.append(f"   {frame}")
        time.sleep(0.3)

    try:
        with open("logs/motion.log", "a") as log:
            for line in log_lines:
                log.write(line + "\n")
    except FileNotFoundError:
        print("⚠️ motion.log not found — skipping log write.")