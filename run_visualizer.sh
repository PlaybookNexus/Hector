#!/bin/bash

echo "🧠 Launching Hector Visualizer..."

# Resolve absolute path to Hector root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate virtual environment if present
VENV_PATH="$SCRIPT_DIR/venv"
if [ -d "$VENV_PATH" ]; then
  source "$VENV_PATH/bin/activate"
  echo "✅ Virtual environment activated."
else
  echo "⚠️ No virtual environment found — continuing without it..."
fi

# Check for motion.log
LOG_PATH="$SCRIPT_DIR/logs/motion.log"
echo "🔍 Looking for motion log at: $LOG_PATH"
if [ ! -f "$LOG_PATH" ]; then
  echo "⚠️ motion.log not found."
  echo "➡️ Run main.py to generate motion history before visualizing."
  exit 1
fi

# Launch the visualizer
echo "🎭 Replaying motion history..."
python3 "$SCRIPT_DIR/dashboard/visualizer_gui.py"

# Desktop shortcut logic (Linux GUI only)
DESKTOP_PATH=~/Desktop/HectorVisualizer.desktop
if [ -d ~/Desktop ]; then
  if [ ! -f "$DESKTOP_PATH" ]; then
    echo -n "🖥️ No desktop shortcut found. Create one now? [y/N]: "
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
      echo "📁 Creating shortcut..."
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
      echo "🚫 Shortcut creation skipped."
    fi
  else
    echo "🖥️ Shortcut already exists at $DESKTOP_PATH"
  fi
else
  echo "⚠️ No Desktop folder detected — are you on a GUI-enabled system?"
fi