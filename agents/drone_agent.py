# agents/drone_agent.py

from agents.base_agent import BaseAgent

class DroneAgent(BaseAgent):
    def __init__(self, agent_id):
        super().__init__(agent_id)
        self.vector_state["status"] = "grounded"
        self.vector_state["altitude"] = 0

    def perform_routine(self, routine_name):
        print(f"[{self.agent_id}] executing drone routine: {routine_name}")
        self.vector_state["last_action"] = f"routine: {routine_name}"
        self.status = "idle"