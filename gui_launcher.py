import tkinter as tk
from tkinter import messagebox, scrolledtext
from main import main  # assumes main.py is in the same folder
import sys
import io

# Ensure UTF-8 output for emoji-safe logging
sys.stdout.reconfigure(encoding='utf-8')

class TextRedirector(io.TextIOBase):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, message):
        self.widget.configure(state='normal')
        self.widget.insert(tk.END, message)
        self.widget.see(tk.END)
        self.widget.configure(state='disabled')

def launch_hector():
    try:
        output_box.configure(state='normal')
        output_box.delete(1.0, tk.END)
        output_box.configure(state='disabled')

        sys.stdout = TextRedirector(output_box)
        print("🚀 Launching Hector mesh...\n")
        main()
        print("\n✅ Autonomy loop completed.")
        messagebox.showinfo("Hector Mesh", "✅ Hector finished his routine.")
    except Exception as e:
        messagebox.showerror("Error", f"❌ Failed to run Hector:\n{e}")

# GUI setup
root = tk.Tk()
root.title("Hector Launcher")
root.geometry("500x400")
root.resizable(False, False)

title_label = tk.Label(root, text="🧠 Launch Hector Mesh", font=("Arial", 16))
title_label.pack(pady=10)

launch_button = tk.Button(root, text="Run main.py", command=launch_hector,
                          font=("Arial", 12), bg="#4CAF50", fg="white", width=20)
launch_button.pack(pady=5)

output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Consolas", 10),
                                       width=60, height=15, state='disabled', bg="#f0f0f0")
output_box.pack(pady=10)

root.mainloop()