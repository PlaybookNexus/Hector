class DroneAgent:
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.id = agent_id  # ✅ Alias for graph compatibility
        self.vector_state = {
            "status": "grounded",
            "risk": "low",
            "altitude": 0
        }

    def perform_routine(self, routine_name):
        print(f"{self.agent_id} executing drone routine: {routine_name}")