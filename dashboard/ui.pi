def render_dashboard(graph):
    print("\n🧠 Hector Override Dashboard")
    print("-" * 40)
    for agent_id, agent in graph.agents.items():
        status = agent.status
        risk = agent.vector_state.get("risk", "unknown")
        last = agent.vector_state.get("last_action", "none")
        override = agent.vector_state.get("status", "")
        print(f"🟢 {agent_id}")
        print(f"   Task: {agent.task}")
        print(f"   Status: {status}")
        print(f"   Risk: {risk}")
        print(f"   Last Action: {last}")
        if override:
            print(f"   Override Status: {override}")
        print("-" * 40)