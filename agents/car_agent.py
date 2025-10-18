# agents/car_agent.py

class CarAgent:
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.vector_state = {
            "status": "parked",
            "risk": "low",
            "location": "garage"
        }

    def perform_routine(self, routine_name):
        print(f"{self.agent_id} executing car routine: {routine_name}")