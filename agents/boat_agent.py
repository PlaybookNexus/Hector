# agents/boat_agent.py

class BoatAgent:
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.vector_state = {
            "status": "docked",
            "risk": "low",
            "location": "harbor"
        }

    def perform_routine(self, routine_name):
        print(f"{self.agent_id} executing boat routine: {routine_name}")