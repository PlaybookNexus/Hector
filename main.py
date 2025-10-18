import os
import sys
import importlib

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
os.makedirs("logs", exist_ok=True)

# Agent class registry
AGENT_CLASSES = {
    "arm": RobotArmAgent,
    "humanoid": HumanoidAgent,
    "dog": RobotDogAgent,
    "car": CarAgent,
    "boat": BoatAgent,
    "drone": DroneAgent
}

def main():
    print("Booting Hector mesh...")

    # Load theatre from environment
    theatre_name = os.environ.get("HECTOR_THEATRE", "search_and_rescue")
    print(f"Selected theatre: {theatre_name}")

    try:
        selected_routines = importlib.import_module(f"routines.{theatre_name}")
    except ModuleNotFoundError:
        print(f"Error: Theatre '{theatre_name}' not found. Defaulting to search_and_rescue.")
        selected_routines = importlib.import_module("routines.search_and_rescue")

    # Initialize mission graph
    graph = MissionGraph()

    # Instantiate agents based on routine keys
    agents = {}
    for agent_id in selected_routines.ROUTINES.keys():
        prefix = agent_id.split("-")[0]
        agent_class = AGENT_CLASSES.get(prefix)
        if agent_class:
            agents[agent_id] = agent_class(agent_id)
            graph.register_agent(agents[agent_id])
        else:
            print(f"Warning: No agent class found for prefix '{prefix}'")

    # Assign and dispatch routines
    for agent_id, routines in selected_routines.ROUTINES.items():
        for routine_name, frames in routines.items():
            graph.assign_task(agent_id, routine_name)
            graph.dispatch_all()
            animate_motion(agent_id, routine_name)

            if os.environ.get("HECTOR_TEACHABLE") == "true":
                print(f"Dispatched '{routine_name}' to {agent_id}")

    # Inject risk levels if defined
    risk_levels = getattr(selected_routines, "RISK_LEVELS", {})
    for agent_id, risk in risk_levels.items():
        if agent_id in agents:
            agents[agent_id].vector_state["risk"] = risk

    # Check for overrides
    override = OverrideManager(graph)
    override.check_risk_levels()

    # Animate intercept reflex if triggered
    animate_motion("humanoid-01", "intercept")

    # Vector summary
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