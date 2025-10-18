#!/bin/bash

echo "🧠 Launching Hector Visualizer..."

# Get absolute path to Hector root
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
echo "🔍 Checking for motion log at: $LOG_PATH"

if [ ! -f "$LOG_PATH" ]; then
  echo "❌ motion.log not found."
  echo "➡️ Run main.py to generate motion history before visualizing."
  exit 1
else
  echo "✅ motion.log found."
fi

# Launch the visualizer
echo "🎭 Replaying motion history..."
python3 "$SCRIPT_DIR/dashboard/visualizer_gui.py"