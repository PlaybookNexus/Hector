import tkinter as tk
from tkinter import messagebox
from main import main  # assumes main.py is in the same folder

def launch_hector():
    try:
        main()
        messagebox.showinfo("Hector Mesh", "✅ Autonomy loop completed.")
    except Exception as e:
        messagebox.showerror("Error", f"❌ Failed to run Hector:\n{e}")

root = tk.Tk()
root.title("Hector Launcher")

canvas = tk.Canvas(root, width=300, height=200)
canvas.pack()

label = tk.Label(root, text="🧠 Launch Hector Mesh", font=("Arial", 14))
canvas.create_window(150, 60, window=label)

launch_button = tk.Button(root, text="Run main.py", command=launch_hector, font=("Arial", 12), bg="#4CAF50", fg="white")
canvas.create_window(150, 120, window=launch_button)

root.mainloop()