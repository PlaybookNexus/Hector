from datetime import datetime

def log_motion(agent_id, routine, frames):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [f"[{timestamp}] {agent_id} performing {routine} routine"]
    lines += [f"   {frame}" for frame in frames]

    try:
        with open("logs/motion.log", "a", encoding="utf-8") as log:
            log.write("\n".join(lines) + "\n")
    except Exception as e:
        print(f"Warning: Failed to write motion log: {e}")