class OverrideManager:
    def __init__(self, graph):
        self.graph = graph
        self.override_log = []

    def check_risk_levels(self, threshold="high"):
        """
        Checks each agent's risk level against the mission threshold.
        Triggers override if agent's risk is equal to or higher than the threshold.
        """
        print(f"Checking risk levels with threshold: {threshold}")
        threshold_rank = self._risk_rank(threshold)

        for agent_id, state in self.graph.get_vector_summary().items():
            agent_risk = state.get("risk", "low")
            agent_rank = self._risk_rank(agent_risk)

            print(f"[{agent_id}] Risk: {agent_risk} (rank {agent_rank})")

            if agent_rank >= threshold_rank:
                self.trigger_override(agent_id)

    def trigger_override(self, agent_id):
        """
        Triggers an override routine for the agent if available.
        """
        agent = self.graph.agents.get(agent_id)
        if agent and hasattr(agent, "assign_task"):
            agent.assign_task("intercept")
            self.override_log.append(f"Override triggered for {agent_id}")
            print(f"[Override] Triggered intercept for {agent_id}")
        else:
            print(f"[Override] No intercept available for {agent_id}")

    def _risk_rank(self, level):
        """
        Converts risk level string to numeric rank for comparison.
        """
        ranks = {
            "low": 1,
            "medium": 2,
            "high": 3
        }
        return ranks.get(level, 0)