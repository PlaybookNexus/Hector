import os
import time
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
    "drone": DroneAgent,
    # Aliases
    "noble": RobotDogAgent,
    "phantom": DroneAgent,
    "warthog": CarAgent,
    "pelican": BoatAgent
}

def main():
    print("Booting Hector mesh...")

    # Load mission parameters from environment
    theatre_name = os.environ.get("HECTOR_THEATRE", "search_and_rescue")
    duration_min = int(os.environ.get("HECTOR_DURATION", "15"))
    risk_threshold = os.environ.get("HECTOR_RISK_THRESHOLD", "medium")
    agent_count = int(os.environ.get("HECTOR_AGENT_COUNT", "1"))
    env_profile = os.environ.get("HECTOR_ENV_PROFILE", "urban")

    print(f"Selected theatre: {theatre_name}")
    print(f"Mission duration: {duration_min} min")
    print(f"Risk threshold: {risk_threshold}")
    print(f"Agent count: {agent_count}")
    print(f"Environment profile: {env_profile}")

    # Load theatre routines
    try:
        selected_routines = importlib.import_module(f"routines.{theatre_name}")
    except ModuleNotFoundError:
        print(f"Error: Theatre '{theatre_name}' not found. Defaulting to search_and_rescue.")
        selected_routines = importlib.import_module("routines.search_and_rescue")

    # Initialize mission graph
    graph = MissionGraph()
    agents = {}

    # Swarm-ready agent instantiation
    default_type = "drone"  # You can make this dynamic later
    agent_class = AGENT_CLASSES.get(default_type)

    if not agent_class:
        print(f"Error: Unknown agent type '{default_type}'")
        return

    for i in range(agent_count):
        agent_id = f"{default_type}-{i+1:02d}"
        agent = agent_class(agent_id)
        agent.vector_state["env"] = env_profile
        agents[agent_id] = agent
        graph.register_agent(agent)

    # Assign routines if available
    for agent_id in agents:
        routines = selected_routines.ROUTINES.get(agent_id)
        if not routines:
            print(f"No routines found for {agent_id}")
            continue

        for routine_name, frames in routines.items():
            graph.assign_task(agent_id, routine_name)
            graph.dispatch_all()
            animate_motion(agent_id, routine_name)

            if os.environ.get("HECTOR_TEACHABLE") == "true":
                print(f"Dispatched '{routine_name}' to {agent_id}")

    # Inject risk levels
    risk_levels = getattr(selected_routines, "RISK_LEVELS", {})
    for agent_id, risk in risk_levels.items():
        if agent_id in agents:
            agents[agent_id].vector_state["risk"] = risk

    # Duration-based loop
    start_time = time.time()
    max_duration = duration_min * 60  # seconds

    while time.time() - start_time < max_duration:
        graph.dispatch_all()
        time.sleep(1)  # tick rate

    print("\nMission duration reached. Proceeding to override and recovery...")

    # Override logic
    override = OverrideManager(graph)
    override.check_risk_levels(threshold=risk_threshold)

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
