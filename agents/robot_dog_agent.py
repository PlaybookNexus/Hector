# agents/robot_dog_agent.py

class RobotDogAgent:
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.vector_state = {
            "status": "idle",
            "risk": "low",
            "location": "unknown"
        }

    def perform_routine(self, routine_name):
        print(f"{self.agent_id} executing dog routine: {routine_name}")