from graph.mission_graph import MissionGraph
from agents.robot_arm_agent import RobotArmAgent
from agents.humanoid_agent import HumanoidAgent

def main():
    print("🧠 Booting Hector mesh...")

    # Initialize mission graph and agents
    graph = MissionGraph()
    arm = RobotArmAgent("arm-01")
    humanoid = HumanoidAgent("humanoid-01")

    # Register agents
    graph.register_agent(arm)
    graph.register_agent(humanoid)

    # Assign tasks to arm
    graph.assign_task("arm-01", "pick")
    graph.dispatch_all()

    graph.assign_task("arm-01", "ballet")
    graph.dispatch_all()

    # Assign tasks to humanoid
    graph.assign_task("humanoid-01", "saluting")
    graph.dispatch_all()

    graph.assign_task("humanoid-01", "kata")
    graph.dispatch_all()

    # Show vector summary
    print("\n🧠 Vector Summary:")
    for agent_id, state in graph.get_vector_summary().items():
        print(f"{agent_id}: {state}")

if __name__ == "__main__":
    main()