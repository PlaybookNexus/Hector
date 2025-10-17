import time

class HumanoidAgent:
    def __init__(self, id, stance="neutral"):
        self.id = id
        self.stance = stance
        self.status = "idle"
        self.vector_state = {
            "pose": "standing",
            "risk": "low",
            "last_action": None
        }

    def update(self):
        if self.status == "saluting":
            self.salute()
        elif self.status == "kata":
            self.perform_kata()
        elif self.status == "intercept":
            self.intercept()
        elif self.status == "tribute":
            self.tribute()
        else:
            self.vector_state["last_action"] = "waiting"

    def assign_task(self, task):
        self.status = task
        self.vector_state["last_action"] = f"task assigned: {task}"

    def salute(self):
        print(f"[{self.id}] Saluting contributor...")
        time.sleep(0.5)
        self.vector_state["pose"] = "salute"
        self.vector_state["last_action"] = "salute complete"
        self.status = "idle"

    def perform_kata(self):
        print(f"[{self.id}] Performing kata routine...")
        for move in ["guard", "strike", "block", "bow"]:
            print(f"[{self.id}] Move: {move}")
            time.sleep(0.3)
        self.vector_state["pose"] = "kata stance"
        self.vector_state["last_action"] = "kata complete"
        self.status = "idle"

    def intercept(self):
        print(f"[{self.id}] Intercepting override...")
        self.vector_state["risk"] = "high"
        self.vector_state["pose"] = "intercept"
        self.vector_state["last_action"] = "override intercepted"
        self.status = "idle"

    def tribute(self):
        print(f"[{self.id}] Performing ceremonial tribute...")
        for motion in ["kneel", "extend arms", "nod"]:
            print(f"[{self.id}] Motion: {motion}")
            time.sleep(0.4)
        self.vector_state["pose"] = "tribute"
        self.vector_state["last_action"] = "tribute complete"
        self.status = "idle"