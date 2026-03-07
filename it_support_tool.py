import tkinter as tk
import psutil
import shutil
import socket
import subprocess
import os
from datetime import datetime

# Store test results
results = []

# -----------------------------
# Create window
# -----------------------------
window = tk.Tk()
window.title("IT Support Diagnostic Tool")
window.geometry("600x500")

# Output box
output_box = tk.Text(window, height=20, width=70)
output_box.pack(pady=10)

# -----------------------------
# Clear output function
# -----------------------------
def clear_output():
    output_box.delete(1.0, tk.END)

# -----------------------------
# CPU TEST
# -----------------------------
def check_cpu():
    clear_output()
    try:
        cpu_usage = psutil.cpu_percent(interval=1)

        if cpu_usage < 70:
            status = "PASS"
            fix = "CPU usage within normal range."

        elif cpu_usage < 90:
            status = "WARNING"
            fix = """Troubleshooting steps:
1. Open Task Manager and check which processes use CPU
2. Close unnecessary applications
3. Disable unused startup programs
4. Check for background updates
5. Run the test again
"""

        else:
            status = "FAIL"
            fix = """Troubleshooting steps:
1. Identify high CPU processes in Task Manager
2. End unnecessary tasks
3. Restart the computer
4. Check for Windows updates
5. Run malware scan
6. Escalate to IT support if issue persists
"""

        results.append(("CPU Usage", status, fix))

        output_box.insert("end", f"CPU Usage: {cpu_usage}% - {status}\n")
        output_box.insert("end", f"{fix}\n\n")

    except:
        output_box.insert("end", "CPU test failed\n\n")


# -----------------------------
# RAM TEST
# -----------------------------
def check_ram():
    clear_output()
    memory = psutil.virtual_memory()
    percent = memory.percent

    if percent < 70:
        status = "PASS"
        fix = "RAM usage normal."

    elif percent < 90:
        status = "WARNING"
        fix = """Troubleshooting steps:
1. Close unused applications
2. Check Task Manager memory usage
3. Restart the computer
4. Disable unnecessary startup apps
"""

    else:
        status = "FAIL"
        fix = """Troubleshooting steps:
1. Close memory heavy applications
2. Restart the system
3. Check Task Manager for high memory processes
4. Escalate if issue continues
"""

    results.append(("RAM Usage", status, fix))

    output_box.insert("end", f"RAM Usage: {percent}% - {status}\n")
    output_box.insert("end", f"{fix}\n\n")


# -----------------------------
# DISK TEST
# -----------------------------
def check_disk():
    clear_output()
    total, used, free = shutil.disk_usage("C:\\")
    percent = (used / total) * 100

    if percent < 80:
        status = "PASS"
        fix = "Disk space healthy."

    elif percent < 90:
        status = "WARNING"
        fix = """Troubleshooting steps:
1. Empty recycle bin
2. Delete temporary files
3. Remove unused applications
"""

    else:
        status = "FAIL"
        fix = """Troubleshooting steps:
1. Delete large unnecessary files
2. Clear temporary files
3. Move files to external storage
4. Escalate if storage remains critically full
"""

    results.append(("Disk Space", status, fix))

    output_box.insert("end", f"Disk Usage: {percent:.2f}% - {status}\n")
    output_box.insert("end", f"{fix}\n\n")


# -----------------------------
# NETWORK TEST
# -----------------------------
def check_network():
    clear_output()
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)

        response = subprocess.run(
            ["ping", "-n", "1", "8.8.8.8"],
            capture_output=True,
            text=True
        )

        output = response.stdout
        ping = int(output.split("time=")[1].split("ms")[0])

        if ping < 50:
            status = "PASS"
            fix = "Network latency normal."

        elif ping < 100:
            status = "WARNING"
            fix = """Troubleshooting steps:
1. Check Wi-Fi signal
2. Move closer to router
3. Disconnect unused devices
4. Try Ethernet connection
"""

        else:
            status = "FAIL"
            fix = """Troubleshooting steps:
1. Restart router/modem
2. Check network cables
3. Close bandwidth heavy apps
4. Try wired Ethernet
5. Escalate if latency persists
"""

        results.append(("Network Connection", status, fix))

        output_box.insert("end", f"Network Ping: {ping} ms - {status}\n")
        output_box.insert("end", f"{fix}\n\n")

    except:
        status = "FAIL"
        fix = """Troubleshooting steps:
1. Check Wi-Fi or Ethernet connection
2. Restart router/modem
3. Disable and re-enable network adapter
4. Escalate if connection cannot be restored
"""

        results.append(("Network Connection", status, fix))

        output_box.insert("end", "Network test failed - No connection\n")
        output_box.insert("end", f"{fix}\n\n")


# -----------------------------
# SAVE REPORT
# -----------------------------
def save_report():

    folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Reports")

    if not os.path.exists(folder):
        os.makedirs(folder)

    filename = os.path.join(
        folder,
        f"IT_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    )

    with open(filename, "w") as file:

        file.write("==== IT SUPPORT TOOL REPORT ====\n\n")
        file.write(f"Generated: {datetime.now()}\n\n")

        for test, status, fix in results:
            file.write(f"Test: {test}\n")
            file.write(f"Status: {status}\n\n")

    output_box.insert("end", f"\nReport saved to Reports folder\n\n")


# -----------------------------
# BUTTONS
# -----------------------------
tk.Button(window, text="Check CPU", width=25, command=check_cpu).pack(pady=3)
tk.Button(window, text="Check RAM", width=25, command=check_ram).pack(pady=3)
tk.Button(window, text="Check Disk", width=25, command=check_disk).pack(pady=3)
tk.Button(window, text="Check Network", width=25, command=check_network).pack(pady=3)

tk.Button(window, text="Save Report", width=25, command=save_report).pack(pady=8)


# Run application
window.mainloop()