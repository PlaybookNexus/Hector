class OverrideManager:
    def __init__(self, graph):
        self.graph = graph
        self.override_log = []

    def check_risk_levels(self):
        for agent_id, state in self.graph.get_vector_summary().items():
            if state.get("risk") == "high":
                self.trigger_override(agent_id)

    def trigger_override(self, agent_id):
        agent = self.graph.agents.get(agent_id)
        if agent and hasattr(agent, "intercept"):
            agent.assign_task("intercept")
            self.override_log.append(f"Override triggered for {agent_id}")
            print(f"[Override] Triggered intercept for {agent_id}")
        else:
            print(f"[Override] No intercept available for {agent_id}")