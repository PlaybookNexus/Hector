#!/bin/bash

echo "🧠 Launching Hector Visualizer..."

# Get absolute path to Hector root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate virtual environment if it exists
if [ -d "$SCRIPT_DIR/venv" ]; then
  source "$SCRIPT_DIR/venv/bin/activate"
  echo "✅ Virtual environment activated."
else
  echo "⚠️ No virtual environment found. Continuing without it..."
fi

# Check for motion.log
LOG_PATH="$SCRIPT_DIR/logs/motion.log"
if [ ! -f "$LOG_PATH" ]; then
  echo "⚠️ motion.log not found at $LOG_PATH"
  echo "➡️ Run main.py to generate motion history before visualizing."
  exit 1
fi

# Launch the visualizer
echo "🎭 Replaying motion history..."
python3 "$SCRIPT_DIR/dashboard/visualizer_gui.py"

# Check for desktop shortcut (Linux GUI only)
DESKTOP_PATH=~/Desktop/HectorVisualizer.desktop
if [ -d ~/Desktop ]; then
  if [ ! -f "$DESKTOP_PATH" ]; then
    echo -n "🖥️ No desktop shortcut found. Create one now? [y/N]: "
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
      cat <<EOF > "$DESKTOP_PATH"
[Desktop Entry]
Name=Hector Visualizer
Comment=Replay Hector's motion history
Exec=bash -c 'cd "$SCRIPT_DIR" && ./run_visualizer.sh'
Icon=utilities-terminal
Terminal=true
Type=Application
EOF
      chmod +x "$DESKTOP_PATH"
      echo "✅ Shortcut created at $DESKTOP_PATH"
    else
      echo "🚫 Skipped shortcut creation."
    fi
  else
    echo "🖥️ Shortcut already exists at $DESKTOP_PATH"
  fi
fi