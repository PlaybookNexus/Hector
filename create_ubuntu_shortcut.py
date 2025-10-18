import os
from pathlib import Path

# Paths
project_dir = Path(__file__).resolve().parent
desktop_entry_dir = Path.home() / ".local/share/applications"
desktop_entry_path = desktop_entry_dir / "hector-launcher.desktop"
launcher_script = project_dir / "launcher_gui.py"
icon_path = project_dir / "assets/icon.png"  # Optional: replace with your actual icon

# Create desktop entry content
entry = f"""[Desktop Entry]
Name=Hector Launcher
Comment=Launch the Hector autonomy mesh
Exec=python3 {launcher_script}
Icon={icon_path if icon_path.exists() else 'utilities-terminal'}
Terminal=false
Type=Application
Categories=Robotics;Utility;
"""

# Ensure directory exists
desktop_entry_dir.mkdir(parents=True, exist_ok=True)

# Write the .desktop file
with open(desktop_entry_path, "w") as f:
    f.write(entry)

# Make it executable
os.chmod(desktop_entry_path, 0o755)

print(f"Shortcut created: {desktop_entry_path}")
print("You can now find 'Hector Launcher' in your application menu.")