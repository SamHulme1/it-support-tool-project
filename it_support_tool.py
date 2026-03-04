import tkinter as tk
import subprocess
import socket
import platform
import os
from datetime import datetime

# Create main window
window = tk.Tk()
window.title("IT Support Toolkit")
window.geometry("600x500")

# Output box
output_box = tk.Text(window, height=18, width=70)
output_box.pack(pady=10)

def clear_output():
    output_box.delete(1.0, tk.END)

# =============================
# System Information
# =============================
def get_system_info():
    clear_output()
    info = f"""
==== SYSTEM INFORMATION ====

Date/Time: {datetime.now()}

System: {platform.system()}
Node Name: {platform.node()}
Release: {platform.release()}
Version: {platform.version()}
Machine: {platform.machine()}
Processor: {platform.processor()}
"""
    output_box.insert(tk.END, info)

# =============================
# IP Address
# =============================
def get_ip():
    clear_output()
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)

    output = f"""
==== NETWORK INFORMATION ====

Hostname: {hostname}
IP Address: {ip}
"""
    output_box.insert(tk.END, output)

# =============================
# Ping Test
# =============================
def ping_google():
    clear_output()
    result = subprocess.run(["ping", "8.8.8.8"], capture_output=True, text=True)
    output_box.insert(tk.END, result.stdout)

# =============================
# Disk Space Check
# =============================
def check_disk_space():
    clear_output()
    result = subprocess.run(["wmic", "logicaldisk", "get", "size,freespace,caption"],
                            capture_output=True, text=True)
    output_box.insert(tk.END, "==== DISK SPACE ====\n\n")
    output_box.insert(tk.END, result.stdout)

# =============================
# Open Windows Tools
# =============================
def open_task_manager():
    os.system("taskmgr")

def open_cmd():
    os.system("start cmd")

# =============================
# Save Report
# =============================
def save_report():
    content = output_box.get(1.0, tk.END)
    filename = f"support_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(filename, "w") as file:
        file.write(content)

    output_box.insert(tk.END, f"\n\nReport saved as {filename}")

# =============================
# Buttons
# =============================
tk.Button(window, text="Get System Info", width=25, command=get_system_info).pack(pady=5)
tk.Button(window, text="Get IP Address", width=25, command=get_ip).pack(pady=5)
tk.Button(window, text="Ping Google (8.8.8.😎", width=25, command=ping_google).pack(pady=5)
tk.Button(window, text="Check Disk Space", width=25, command=check_disk_space).pack(pady=5)
tk.Button(window, text="Open Task Manager", width=25, command=open_task_manager).pack(pady=5)
tk.Button(window, text="Open Command Prompt", width=25, command=open_cmd).pack(pady=5)
tk.Button(window, text="Save Report", width=25, command=save_report).pack(pady=5)

window.mainloop()