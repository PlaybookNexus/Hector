#!/bin/bash

echo "🧠 Launching Hector Visualizer..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
  source venv/bin/activate
  echo "✅ Virtual environment activated."
else
  echo "⚠️ No virtual environment found. Continuing without it..."
fi

# Check for motion.log
LOG_PATH="logs/motion.log"
if [ ! -f "$LOG_PATH" ]; then
  echo "⚠️ motion.log not found at $LOG_PATH"
  echo "➡️ Run main.py to generate motion history before visualizing."
  exit 1
fi

# Launch the visualizer
echo "🎭 Replaying motion history..."
python3 dashboard/visualizer_gui.py

# Create desktop shortcut (Linux GUI only)
DESKTOP_PATH=~/Desktop/HectorVisualizer.desktop
if [ -d ~/Desktop ]; then
  echo "🖥️ Creating desktop shortcut..."
  cat <<EOF > "$DESKTOP_PATH"
[Desktop Entry]
Name=Hector Visualizer
Comment=Replay Hector's motion history
Exec=bash -c 'cd ~/Hector && ./run_visualizer.sh'
Icon=utilities-terminal
Terminal=true
Type=Application
EOF
  chmod +x "$DESKTOP_PATH"
  echo "✅ Shortcut created at $DESKTOP_PATH"
fi