def color_risk(risk):
    if risk == "low":
        return f"\033[92m{risk}\033[0m"      # Green
    elif risk == "high":
        return f"\033[93m{risk}\033[0m"      # Yellow
    elif risk == "critical":
        return f"\033[91m{risk}\033[0m"      # Red
    return risk

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
import time

def animate_motion(agent_id, routine):
    print(f"\n🎭 {agent_id} performing {routine} routine...")
    frames = {
        "ballet": [
            "🩰 base sweep →",
            "🩰 arm extension ↑",
            "🩰 wrist flourish ✨",
            "🩰 gentle grip 🤏"
        ],
        "kata": [
            "🥋 guard stance 🛡️",
            "🥋 strike ➡️",
            "🥋 block ⛔",
            "🥋 bow 🙇"
        ]
    }

    for frame in frames.get(routine, []):
        print(f"   {frame}")
        time.sleep(0.3)