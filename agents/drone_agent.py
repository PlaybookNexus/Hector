class DroneAgent:
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.id = agent_id  # Alias for graph compatibility
        self.status = "idle"
        self.task = None
        self.vector_state = {
            "status": "grounded",
            "risk": "low",
            "altitude": 0,
            "last_action": None
        }

    def assign_task(self, task):
        self.task = task
        self.status = "assigned"
        self.vector_state["last_action"] = f"task assigned: {task}"

    def update(self):
        if self.task:
            self.perform_routine(self.task)
            self.task = None
        else:
            self.status = "idle"
            self.vector_state["last_action"] = "waiting"

    def perform_routine(self, routine_name):
        print(f"[{self.agent_id}] executing drone routine: {routine_name}")
        self.vector_state["last_action"] = f"routine: {routine_name}"
        self.status = "idle"

    def reset(self):
        print(f"[Recovery] Resetting {self.agent_id}")
        self.status = "idle"
        self.task = None
        self.vector_state["status"] = "recovered"
        self.vector_state["last_action"] = "reset complete"