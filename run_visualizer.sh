#!/bin/bash

echo "🧠 Launching Hector Visualizer..."

# Activate virtual environment if it exists.
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