from graph.mission_graph import MissionGraph
from graph.override import OverrideManager
from graph.recovery import RecoveryManager
from agents.robot_arm_agent import RobotArmAgent
from agents.humanoid_agent import HumanoidAgent
from dashboard.ui import render_dashboard, animate_motion

def main():
    print("Booting Hector mesh...")

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
    animate_motion("arm-01", "ballet")  # ← synced with dispatch

    # Assign tasks to humanoid
    graph.assign_task("humanoid-01", "saluting")
    graph.dispatch_all()

    graph.assign_task("humanoid-01", "kata")
    graph.dispatch_all()
    animate_motion("humanoid-01", "kata")  # ← synced with dispatch

    # Simulate risk escalation
    humanoid.vector_state["risk"] = "high"
    arm.vector_state["risk"] = "critical"

    # Check for overrides
    override = OverrideManager(graph)
    override.check_risk_levels()

    # Animate intercept reflex if triggered
    animate_motion("humanoid-01", "intercept")

    # Show vector summary
    print("\n Vector Summary:")
    for agent_id, state in graph.get_vector_summary().items():
        print(f"{agent_id}: {state}")

    # Recovery phase
    recovery = RecoveryManager(graph)
    recovery.check_and_recover()

    # Final dashboard
    render_dashboard(graph)

if __name__ == "__main__":
    main()