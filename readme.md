## 🧠 `README.md` — Hector: Modular Autonomy Mesh

```markdown
# 🧠 Hector: Modular Autonomy Mesh

Hector is a remixable autonomy framework for expressive agents, override choreography, and contributor empowerment. Designed for robotics, sensors, and legal transparency, Hector supports pick/place routines, martial arts flows, and real-time reflex logic.

---

## 🚀 Quick Start (Linux, Raspberry Pi, or Windows)

```bash
git clone https://github.com/PlaybookNexus/Hector.git
cd Hector
PYTHONIOENCODING=utf-8 python gui_launcher.py
```

If you see logging errors:

```bash
mkdir logs
```

---

## 🧩 What Hector Does

- Animates routines like ballet, kata, saluting, intercept
- Logs every motion to `logs/motion.log` with emoji and timestamps
- Triggers override and recovery based on agent risk thresholds
- Renders a live dashboard with agent status and vector summaries
- Supports multi-agent swarms with custom types and counts
- Launches via GUI cockpit with visualizer, git pull, and logging

---

## 🛠️ Folder Overview

```
Hector/
├── agents/         # RobotArmAgent, HumanoidAgent, DroneAgent, etc.
├── graph/          # MissionGraph, OverrideManager, RecoveryManager
├── dashboard/      # UI, motion routines, visualizer
├── ux/             # Theme and cockpit styling
├── logs/           # Motion history (auto-created)
├── gui_launcher.py # Swarm-ready launcher with cockpit controls
├── main.py         # Entry point for orchestration and dispatch
```

---

## 🎛️ Launching Missions

Use `gui_launcher.py` to configure:

- Mission type (search and rescue, firefighting, combat ops)
- Duration, environment, and risk threshold
- Agent swarm: mix drones, dogs, cars, boats, etc.
- Visualizer and log viewer

Agent config is passed as:

```bash
HECTOR_AGENT_CONFIG="drone:5,dog:2,car:1"
```

This enables dynamic instantiation of agents like `drone-01`, `drone-02`, … `dog-01`, `car-01`, etc.

---

## 🧠 Remixing Hector

- Add new routines in `dashboard/motions.py`
- Animate with `animate_motion(agent_id, "routine")`
- Log with `log_motion(agent_id, routine, frames)`
- Visualize with `visualizer_gui.py` (live preview)
- Extend override logic in `graph/override.py`
- Add new agent classes in `agents/`

---

## 🧪 Example Routines

```python
animate_motion("humanoid-01", "salute")
animate_motion("drone-03", "intercept")
animate_motion("dog-01", "guard_pose")
```

---

## 🤝 Contributing

Coming soon: `CONTRIBUTING.md` with guides for:

- Adding new agent classes and reflex logic
- Designing override choreography
- Building teachable onboarding flows
- Creating expressive motion routines

---

Built for remixing. Ready to dance.
```