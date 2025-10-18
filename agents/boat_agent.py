# agents/boat_agent.py

from agents.base_agent import BaseAgent

class BoatAgent(BaseAgent):
    def __init__(self, agent_id):
        super().__init__(agent_id)
        self.vector_state["location"] = "harbor"
        self.vector_state["status"] = "docked"

    def perform_routine(self, routine_name):
        print(f"[{self.agent_id}] executing boat routine: {routine_name}")
        self.vector_state["last_action"] = f"routine: {routine_name}"
        self.status = "idle"