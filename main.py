import os
import sys
import importlib

sys.stdout.reconfigure(encoding='utf-8')

from graph.mission_graph import MissionGraph
from graph.override import OverrideManager
from graph.recovery import RecoveryManager

from agents.robot_arm_agent import RobotArmAgent
from agents.humanoid_agent import HumanoidAgent
from agents.robot_dog_agent import RobotDogAgent
from agents.car_agent import CarAgent
from agents.boat_agent import BoatAgent
from agents.drone_agent import DroneAgent

from dashboard.ui import render_dashboard, animate_motion

# Ensure logs directory exists
if not os.path.exists("logs"):
    os.makedirs("logs")

def main():
    print("Booting Hector mesh...")

    # Load selected theatre from environment variable
    theatre_name = os.environ.get("HECTOR_THEATRE", "search_and_rescue")
    print(f"Selected theatre: {theatre_name}")

    try:
        selected_routines = importlib.import_module(f"routines.{theatre_name}")
    except ModuleNotFoundError:
        print(f"Error: Theatre '{theatre_name}' not found. Defaulting to search_and_rescue.")
        selected_routines = importlib.import_module("routines.search_and_rescue")

    # Initialize mission graph
    graph = MissionGraph()

    # Instantiate agents
    agents = {
        "arm-01": RobotArmAgent("arm-01"),
        "humanoid-01": HumanoidAgent("humanoid-01"),
        "noble-01": RobotDogAgent("noble-01"),
        "warthog-01": CarAgent("warthog-01"),
        "pelican-01": BoatAgent("pelican-01"),
        "phantom-01": DroneAgent("phantom-01")
    }

    # Register agents
    for agent in agents.values():
        graph.register_agent(agent)

    # Assign and dispatch routines from selected theatre
    for agent_id, routines in selected_routines.ROUTINES.items():
        for routine_name, frames in routines.items():
            graph.assign_task(agent_id, routine_name)
            graph.dispatch_all()
            animate_motion(agent_id, routine_name)

    # Simulate risk escalation
    agents["humanoid-01"].vector_state["risk"] = "high"
    agents["arm-01"].vector_state["risk"] = "critical"
    agents["noble-01"].vector_state["risk"] = "medium"

    # Check for overrides
    override = OverrideManager(graph)
    override.check_risk_levels()

    # Animate intercept reflex if triggered
    animate_motion("humanoid-01", "intercept")

    # Show vector summary
    print("\nVector Summary:")
    for agent_id, state in graph.get_vector_summary().items():
        print(f"{agent_id}: {state}")

    # Recovery phase
    recovery = RecoveryManager(graph)
    recovery.check_and_recover()

    # Final dashboard
    render_dashboard(graph)

if __name__ == "__main__":
    main()