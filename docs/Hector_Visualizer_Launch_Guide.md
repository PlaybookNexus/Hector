# 🧭 Hector Visualizer Launch Guide  
**Version:** 1.1 (No shell script)  
**Audience:** Contributors, remixers
**Purpose:** Replay Hector’s motion history using a graphical interface  
**Location:** `~/Hector/dashboard/visualizer_gui.py`

---

## 🧠 Prerequisites

Before launching, confirm:

- ✅ You’ve run `main.py` at least once to generate `logs/motion.log`
- ✅ You’re in the `Hector/dashboard/` folder
- ✅ Python 3 is installed
- ✅ (Optional) Virtual environment is activated

---

## 🚀 Launch Steps

### 1. Open a terminal and navigate to the dashboard folder:

```bash
cd ~/Hector/dashboard
```

### 2. (Optional) Activate the virtual environment:

```bash
source ../venv/bin/activate
```

### 3. Run the visualizer:

```bash
python3 visualizer_gui.py
```

---

## 📁 File Structure Overview

```
Hector/
├── main.py                  # Generates motion.log
├── logs/
│   └── motion.log           # Motion history file
├── venv/                    # Optional virtual environment
└── dashboard/
    └── visualizer_gui.py    # GUI visualizer
```

---

## 🧪 Troubleshooting

| Issue                          | Fix                                                                 |
|-------------------------------|----------------------------------------------------------------------|
| `motion.log not found`        | Run `main.py` from Hector root to generate motion history            |
| GUI opens but shows nothing   | Confirm `motion.log` has content; check path resolution in GUI code  |
| Python errors on launch       | Check Python version; confirm dependencies are installed             |

---

## 🧒 Remix Mode

- Try editing `visualizer_gui.py` to change colors, layout, or animation speed
- Add a button to replay only the last 10 frames
- Swap `motion.log` with a custom routine log for testing

