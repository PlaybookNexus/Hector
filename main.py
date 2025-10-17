# main.py

from agents.robot_arm_agent import RobotArmAgent

def main():
    print("🧠 Booting Hector mesh...")

    # Initialize agent
    arm = RobotArmAgent("arm-01")

    # Assign and execute pick task
    arm.assign_task("pick")
    for _ in range(3):
        arm.update()
        print(f"[{arm.id}] Status: {arm.status}, Holding: {arm.holding_object}, Last: {arm.vector_state['last_action']}")

    # Perform ballet routine
    arm.perform_ballet()
    print(f"[{arm.id}] Finished ballet. Last action: {arm.vector_state['last_action']}")

if __name__ == "__main__":
    main()