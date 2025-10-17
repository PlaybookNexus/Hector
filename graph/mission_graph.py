import time
from agents.robot_arm_agent import RobotArmAgent

class MissionGraph:
    def __init__(self):
        self.agents = {}
        self.task_queue = []
        self.log = []

    def register_agent(self, agent):
        self.agents[agent.id] = agent
        self.log_event(f"Registered agent: {agent.id}")

    def assign_task(self, agent_id, task):
        if agent_id in self.agents:
            self.agents[agent_id].assign_task(task)
            self.log_event(f"Assigned task '{task}' to {agent_id}")
        else:
            self.log_event(f"Agent {agent_id} not found")

    def dispatch_all(self):
        for agent in self.agents.values():
            agent.update()
            self.log_event(f"{agent.id} status: {agent.status}, last: {agent.vector_state['last_action']}")

    def log_event(self, message):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {message}"
        self.log.append(entry)
        print(entry)

    def get_vector_summary(self):
        summary = {}
        for agent in self.agents.values():
            summary[agent.id] = agent.vector_state
        return summary