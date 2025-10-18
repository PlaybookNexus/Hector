#!/bin/bash

echo "🧠 Launching Hector Visualizer..."

# Resolve absolute path to dashboard folder
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Activate virtual environment if it exists
VENV_PATH="$ROOT_DIR/venv"
if [ -d "$VENV_PATH" ]; then
  source "$VENV_PATH/bin/activate"
  echo "✅ Virtual environment activated."
else
  echo "⚠️ No virtual environment found at $VENV_PATH — continuing without it..."
fi

# Check for motion.log
LOG_PATH="$ROOT_DIR/logs/motion.log"
echo "🔍 Checking for motion log at: $LOG_PATH"

if [ ! -f "$LOG_PATH" ]; then
  echo "❌ motion.log not found."
  echo "➡️ Run main.py from the Hector root to generate motion history before visualizing."
  exit 1
else
  echo "✅ motion.log found."
fi

# Launch the visualizer
echo "🎭 Replaying motion history..."
python3 "$SCRIPT_DIR/visualizer_gui.py"