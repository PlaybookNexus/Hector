# agents/robot_dog_agent.py

from agents.base_agent import BaseAgent

class RobotDogAgent(BaseAgent):
    def __init__(self, agent_id):
        super().__init__(agent_id)
        self.vector_state["location"] = "unknown"
        self.vector_state["status"] = "idle"

    def perform_routine(self, routine_name):
        print(f"[{self.agent_id}] executing dog routine: {routine_name}")
        self.vector_state["last_action"] = f"routine: {routine_name}"
        self.status = "idle"