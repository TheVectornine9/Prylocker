import tkinter as tk
from tkinter import messagebox
from screeninfo import get_monitors
import json

windows = []

try:
    with open("config.json", "r") as f:
        lines = f.read()
        CORRECT_PASSCODE = json.loads(lines)["passcode"]
except FileNotFoundError:
    with open("config.json", "w") as f:
        
        
        root = tk.Tk()
        root.withdraw()  # Hide the root window

        def set_passcode():
            new_passcode = passcode_entry.get()
            if new_passcode:
                with open("config.json", "w") as config_file:
                    json.dump({"passcode": new_passcode}, config_file)
                messagebox.showinfo("Success", "Passcode has been set.")
                set_passcode_window.destroy()
            else:
                messagebox.showerror("Error", "Passcode cannot be empty.")

        set_passcode_window = tk.Toplevel()
        set_passcode_window.title("Set Passcode")
        set_passcode_window.geometry("300x150")
        set_passcode_window.resizable(False, False)

        tk.Label(set_passcode_window, text="Enter a new passcode:", font=("Arial", 12)).pack(pady=10)
        passcode_entry = tk.Entry(set_passcode_window, show="*", font=("Arial", 12))
        passcode_entry.pack(pady=5)
        passcode_entry.focus_set()

        tk.Button(set_passcode_window, text="Set Passcode", command=set_passcode, font=("Arial", 12)).pack(pady=10)

        root.mainloop()
        
        

        messagebox.showerror("Finished", "Pascode has been set. Please restart the program.")
        exit(0)


def unlock():  # Removed unused _event parameter
    entered_passcode = entry.get()
    if entered_passcode == CORRECT_PASSCODE:
        for win in windows:
            win.destroy()
    else:
        messagebox.showerror("Access Denied", "Incorrect passcode.")
        entry.delete(0, tk.END)

def block_close():
    pass  # Prevent window close

def block_keys():
    return "break"

def alt_f4_guard(event):
    if event.keysym == 'F4' and (event.state & 0x0008):  # Alt is held
        return "break"

# Create a fullscreen lock window on each monitor
for i, m in enumerate(get_monitors()):
    win = tk.Tk()
    win.overrideredirect(True)
    win.geometry(f"{m.width}x{m.height}+{m.x}+{m.y}")
    win.configure(bg="black")
    win.protocol("WM_DELETE_WINDOW", block_close)

    # Block escape routes
    win.bind("<Alt-F4>", block_keys)
    win.bind("<Escape>", block_keys)
    win.bind("<F4>", alt_f4_guard)
    win.bind_all("<KeyPress-F4>", alt_f4_guard)

    label = tk.Label(win, text="Pc locked. \n\nPlease enter the  passcode" if i == 0 else "",
                     font=("Arial", 36), fg="red", bg="black")
    label.pack(pady=100)

    if i == 0:
        entry = tk.Entry(win, show="*", font=("Arial", 24), justify="center")
        entry.pack()
        entry.focus_set()
        entry.bind("<Return>", unlock)  # ✅ Bind Enter key to unlock

        btn = tk.Button(win, text="Unlock", font=("Arial", 20), command=unlock)
        btn.pack(pady=20)

    win.attributes("-topmost", True)
    windows.append(win)

tk.mainloop()
