import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import subprocess
import sys
import io
from main import main  # assumes main.py is in the same folder

# Optional: UTF-8 output for broader character support
sys.stdout.reconfigure(encoding='utf-8')

default_font = ("Arial", 10)

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
            status_label.config(text="Launching Hector mesh...")
            output_box.configure(state='normal')
            output_box.delete(1.0, tk.END)
            output_box.configure(state='disabled')

            sys.stdout = TextRedirector(output_box)
            print("Launching Hector mesh...\n")
            main()
            print("\nAutonomy loop completed.")
            status_label.config(text="Hector finished his routine.")
            messagebox.showinfo("Hector Mesh", "Hector finished his routine.")
        except Exception as e:
            status_label.config(text="Error during execution.")
            messagebox.showerror("Error", f"Failed to run Hector:\n{e}")

    threading.Thread(target=run).start()

def clear_output():
    output_box.configure(state='normal')
    output_box.delete(1.0, tk.END)
    output_box.configure(state='disabled')
    status_label.config(text="Output cleared.")

def launch_visualizer():
    try:
        subprocess.Popen(["python", "dashboard/visualizer_gui.py"])
        status_label.config(text="Visualizer launched.")
    except Exception as e:
        status_label.config(text="Failed to launch visualizer.")
        messagebox.showerror("Error", f"Could not launch visualizer:\n{e}")

# GUI setup
root = tk.Tk()
root.title("Hector Launcher")
root.geometry("600x500")
root.resizable(False, False)

title_label = tk.Label(root, text="Launch Hector Mesh", font=("Arial", 16))
title_label.pack(pady=10)

button_frame = tk.Frame(root)
button_frame.pack(pady=5)

launch_button = tk.Button(button_frame, text="Run main.py", command=launch_hector,
                          font=default_font, bg="#4CAF50", fg="white", width=15)
launch_button.pack(side="left", padx=5)

clear_button = tk.Button(button_frame, text="Clear Output", command=clear_output,
                         font=default_font, bg="#f44336", fg="white", width=15)
clear_button.pack(side="left", padx=5)

view_log_button = tk.Button(button_frame, text="View Log", command=launch_visualizer,
                            font=default_font, bg="#2196F3", fg="white", width=15)
view_log_button.pack(side="left", padx=5)

output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=default_font,
                                       width=70, height=20, state='disabled', bg="#f0f0f0")
output_box.pack(pady=10)

status_label = tk.Label(root, text="Ready", font=default_font, fg="darkgreen", anchor="w")
status_label.pack(side="bottom", fill="x")

root.mainloop()