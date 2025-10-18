import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import subprocess
import sys
import io
import os

from ux.theme import DARK_BG, TEXT_COLOR, ACCENT_COLOR, WARNING_COLOR, CRITICAL_COLOR, FONT

class TextRedirector(io.TextIOBase):
    def __init__(self, widget):
        self.widget = widget

    def write(self, message):
        self.widget.configure(state='normal')
        self.widget.insert(tk.END, message)
        self.widget.see(tk.END)
        self.widget.configure(state='disabled')

def launch_hector():
    def run():
        try:
            os.environ["HECTOR_THEATRE"] = selected_theatre.get()

            status_label.config(text="Launching Hector mesh...", fg=ACCENT_COLOR)
            output_box.configure(state='normal')
            output_box.delete(1.0, tk.END)
            output_box.configure(state='disabled')

            sys.stdout = TextRedirector(output_box)
            print(f"Selected theatre: {selected_theatre.get()}")
            print("Launching Hector mesh...\n")

            from main import main
            main()

            print("\nAutonomy loop completed.")
            status_label.config(text="Hector finished his routine.", fg=TEXT_COLOR)
            messagebox.showinfo("Hector Mesh", "Hector finished his routine.")
        except Exception as e:
            status_label.config(text="Error during execution.", fg=CRITICAL_COLOR)
            messagebox.showerror("Error", f"Failed to run Hector:\n{e}")

    threading.Thread(target=run).start()

def clear_output():
    output_box.configure(state='normal')
    output_box.delete(1.0, tk.END)
    output_box.configure(state='disabled')
    status_label.config(text="Output cleared.", fg=WARNING_COLOR)

def launch_visualizer():
    try:
        subprocess.Popen(["python", "dashboard/visualizer_gui.py"])
        status_label.config(text="Visualizer launched.", fg=ACCENT_COLOR)
    except Exception as e:
        status_label.config(text="Failed to launch visualizer.", fg=CRITICAL_COLOR)
        messagebox.showerror("Error", f"Could not launch visualizer:\n{e}")

def run_git_pull():
    def pull():
        try:
            status_label.config(text="Updating from Git...", fg=ACCENT_COLOR)
            output_box.configure(state='normal')
            output_box.insert(tk.END, "\nRunning: git pull\n")
            output_box.configure(state='disabled')

            result = subprocess.run(["git", "pull"], capture_output=True, text=True)
            output_box.configure(state='normal')
            output_box.insert(tk.END, result.stdout + result.stderr)
            output_box.configure(state='disabled')

            status_label.config(text="Update complete.", fg=TEXT_COLOR)
        except Exception as e:
            status_label.config(text="Git update failed.", fg=CRITICAL_COLOR)
            messagebox.showerror("Git Error", f"Failed to pull updates:\n{e}")

    threading.Thread(target=pull).start()

# GUI setup
root = tk.Tk()
root.title("Hector Launcher")
root.geometry("720x540")
root.resizable(False, False)
root.configure(bg=DARK_BG)

selected_theatre = tk.StringVar(value="search_and_rescue")

title_label = tk.Label(root, text="Launch Hector Mesh", font=("Segoe UI", 16, "bold"),
                       bg=DARK_BG, fg=ACCENT_COLOR)
title_label.pack(pady=10)

# Theatre selector
theatre_frame = tk.Frame(root, bg=DARK_BG)
theatre_frame.pack(pady=5)

theatre_label = tk.Label(theatre_frame, text="Mission Theatre:", font=FONT,
                         bg=DARK_BG, fg=TEXT_COLOR)
theatre_label.pack(side="left", padx=5)

theatre_dropdown = tk.OptionMenu(theatre_frame, selected_theatre,
                                 "search_and_rescue", "firefighting", "combat_ops")
theatre_dropdown.config(font=FONT, bg="#1E1E1E", fg=TEXT_COLOR, width=20)
theatre_dropdown.pack(side="left", padx=5)

# Buttons
button_frame = tk.Frame(root, bg=DARK_BG)
button_frame.pack(pady=5)

launch_button = tk.Button(button_frame, text="Start Mission", command=launch_hector,
                          font=FONT, bg=ACCENT_COLOR, fg=DARK_BG, width=15)
launch_button.pack(side="left", padx=5)

clear_button = tk.Button(button_frame, text="Clear Output", command=clear_output,
                         font=FONT, bg=WARNING_COLOR, fg=DARK_BG, width=15)
clear_button.pack(side="left", padx=5)

view_log_button = tk.Button(button_frame, text="View Log", command=launch_visualizer,
                            font=FONT, bg="#2196F3", fg=DARK_BG, width=15)
view_log_button.pack(side="left", padx=5)

update_button = tk.Button(button_frame, text="Update Hector", command=run_git_pull,
                          font=FONT, bg="#9C27B0", fg="white", width=15)
update_button.pack(side="left", padx=5)

# Output box
output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=FONT,
                                       width=70, height=20, state='disabled',
                                       bg="#1E1E1E", fg=TEXT_COLOR)
output_box.pack(pady=10)

status_label = tk.Label(root, text="Ready", font=FONT, fg=ACCENT_COLOR,
                        bg=DARK_BG, anchor="w")
status_label.pack(side="bottom", fill="x")

root.mainloop()