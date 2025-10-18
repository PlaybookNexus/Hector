# agents/robot_arm_agent.py

import random
import time
from agents.base_agent import BaseAgent

class RobotArmAgent(BaseAgent):
    def __init__(self, agent_id, base_location=(0, 0)):
        super().__init__(agent_id)
        self.base_location = base_location
        self.joint_angles = [0.0 for _ in range(6)]
        self.gripper_open = True
        self.holding_object = False
        self.vector_state["reach_zone"] = (1.0, 1.0)

    def update(self):
        if self.task == "ballet":
            self.perform_ballet()
            self.task = None
        elif self.task:
            self.execute_task()
        else:
            self.status = "idle"
            self.vector_state["last_action"] = "waiting"

    def execute_task(self):
        if self.task == "pick":
            self.status = "picking"
            self.simulate_joint_motion()
            self.gripper_open = False
            self.holding_object = True
            self.vector_state["last_action"] = "picked object"
        elif self.task == "place":
            self.status = "placing"
            self.simulate_joint_motion()
            self.gripper_open = True
            self.holding_object = False
            self.vector_state["last_action"] = "placed object"
        self.task = None

    def simulate_joint_motion(self):
        self.joint_angles = [angle + random.uniform(-5, 5) for angle in self.joint_angles]
        time.sleep(0.5)

    def perform_ballet(self):
        self.status = "dancing"
        self.vector_state["last_action"] = "ballet start"

        for pos in range(90, 121, 5):
            self.joint_angles[0] = pos
            self.joint_angles[3] = pos
            self.log_motion("base sweep")
            time.sleep(0.02)

        for pos in range(90, 44, -5):
            self.joint_angles[1] = pos
            self.joint_angles[2] = 180 - pos
            self.log_motion("arm extension")
            time.sleep(0.02)

        for pos in range(90, 121, 5):
            self.joint_angles[3] = pos
            self.log_motion("wrist flourish")
            time.sleep(0.015)

        for pos in range(85, 29, -5):
            self.joint_angles[4] = pos
            self.log_motion("gentle grip")
            time.sleep(0.01)

        self.vector_state["last_action"] = "ballet finish"
        self.status = "idle"

    def log_motion(self, step):
        print(f"[{self.agent_id}] Motion: {step}")

    def abort(self):
        print(f"[Override] Aborting tasks for {self.agent_id}")
        self.vector_state["status"] = "aborted"
        self.vector_state["task"] = None

        with open("logs/override.log", "a") as log:
            log.write(f"{time.time()} - {self.agent_id} aborted\n")