import time

class RecoveryManager:
    def __init__(self, graph, cooldown=2.0):
        self.graph = graph
        self.cooldown = cooldown  # seconds

    def check_and_recover(self):
        for agent in self.graph.agents.values():
            if agent.vector_state.get("status") == "aborted":
                print(f"[RecoveryManager] Cooldown for {agent.id}...")
                time.sleep(self.cooldown)
                agent.reset()
                self.log_recovery(agent.id)

    def log_recovery(self, agent_id):
        with open("logs/override.log", "a") as log:
            log.write(f"{time.time()} - {agent_id} recovered\n")