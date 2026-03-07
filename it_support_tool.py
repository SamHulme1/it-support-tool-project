import tkinter as tk
import psutil
import shutil
import socket
import subprocess
import os
from datetime import datetime

# -----------------------------
# Store test results
# -----------------------------
results = []

# -----------------------------
# Main Window
# -----------------------------
window = tk.Tk()
window.title("IT Support Diagnostic Tool")
window.geometry("900x600")

# Output box
output_box = tk.Text(window, height=20, width=100)
output_box.pack(pady=10)

# -----------------------------
# Helper to run tests
# -----------------------------
def run_test(test_func):
    output_box.delete("1.0", "end")  # Clear previous output
    results.clear()  # Clear previous results
    test_func()

# -----------------------------
# System Check Functions
# -----------------------------
def check_cpu():
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        if cpu_usage < 70:
            status = "PASS"
            fix = "CPU usage normal."
        elif cpu_usage < 90:
            status = "WARNING"
            fix = "Close unnecessary apps or restart system."
        else:
            status = "FAIL"
            fix = "Investigate high CPU usage."
        results.append(("CPU Usage", status, fix))
        output_box.insert("end", f"CPU Usage: {cpu_usage}% - {status}\n{fix}\n\n")
    except:
        output_box.insert("end", "CPU test failed\n\n")

def check_ram():
    memory = psutil.virtual_memory()
    percent = memory.percent
    if percent < 70:
        status = "PASS"
        fix = "RAM usage normal."
    elif percent < 90:
        status = "WARNING"
        fix = "Close unused applications."
    else:
        status = "FAIL"
        fix = "Investigate high RAM usage."
    results.append(("RAM Usage", status, fix))
    output_box.insert("end", f"RAM Usage: {percent}% - {status}\n{fix}\n\n")

def check_disk():
    total, used, free = shutil.disk_usage("C:\\")
    percent = (used / total) * 100
    if percent < 80:
        status = "PASS"
        fix = "Disk space healthy."
    elif percent < 90:
        status = "WARNING"
        fix = "Delete unnecessary files."
    else:
        status = "FAIL"
        fix = "Clear disk urgently."
    results.append(("Disk Space", status, fix))
    output_box.insert("end", f"Disk Usage: {percent:.2f}% - {status}\n{fix}\n\n")

def check_network():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        response = subprocess.run(["ping", "-n", "1", "8.8.8.8"], capture_output=True, text=True)
        ping = int(response.stdout.split("time=")[1].split("ms")[0])
        if ping < 50:
            status = "PASS"
            fix = "Network latency normal."
        elif ping < 100:
            status = "WARNING"
            fix = "Check Wi-Fi or close heavy apps."
        else:
            status = "FAIL"
            fix = "Restart router or check network."
        results.append(("Network Connection", status, fix))
        output_box.insert("end", f"Network Ping: {ping} ms - {status}\n{fix}\n\n")
    except:
        status = "FAIL"
        fix = "Network test failed. Check connection."
        results.append(("Network Connection", status, fix))
        output_box.insert("end", f"{fix}\n\n")

# -----------------------------
# Security & Drivers Functions
# -----------------------------
def open_antivirus():
    os.system("start windowsdefender:")

def check_antivirus():
    global fix_button_antivirus
    try:
        result = subprocess.run(
            ["powershell", "Get-MpComputerStatus | Select-Object -ExpandProperty AntivirusEnabled"],
            capture_output=True, text=True
        )
        enabled = result.stdout.strip()
        if enabled == "True":
            status = "PASS"
            fix_button_antivirus.config(state="disabled")
            fix_text = "Antivirus active."
        else:
            status = "FAIL"
            fix_button_antivirus.config(state="normal")
            fix_text = "Antivirus inactive."
        results.append(("Antivirus Status", status, ""))
        output_box.insert("end", f"Antivirus Status: {status}\n{fix_text}\n\n")
    except:
        status = "FAIL"
        fix_button_antivirus.config(state="normal")
        results.append(("Antivirus Status", status, ""))
        output_box.insert("end", "Antivirus check failed\n\n")

def open_windows_update():
    os.system("start ms-settings:windowsupdate")

def check_updates():
    global fix_button_update
    try:
        result = subprocess.run(
            ["powershell", "Get-WindowsUpdate -MicrosoftUpdate -IgnoreUserInput | Select-Object -ExpandProperty KBArticleIDs"],
            capture_output=True, text=True
        )
        updates_available = bool(result.stdout.strip())
        if updates_available:
            status = "WARNING"
            fix_button_update.config(state="normal")
            fix_text = "Updates pending."
        else:
            status = "PASS"
            fix_button_update.config(state="disabled")
            fix_text = "System up to date."
        results.append(("Windows Updates", status, ""))
        output_box.insert("end", f"Windows Updates: {status}\n{fix_text}\n\n")
    except:
        status = "FAIL"
        fix_button_update.config(state="normal")
        results.append(("Windows Updates", status, ""))
        output_box.insert("end", "Update check failed\n\n")

def open_device_manager():
    os.system("devmgmt.msc")

def check_drivers():
    global fix_button_drivers
    try:
        result = subprocess.run(
            ["powershell", "Get-PnpDevice | Where-Object {$_.Status -eq 'Error'} | Select-Object -ExpandProperty Name"],
            capture_output=True, text=True
        )
        driver_issue = bool(result.stdout.strip())
        if driver_issue:
            status = "FAIL"
            fix_button_drivers.config(state="normal")
            fix_text = "Driver issue detected."
        else:
            status = "PASS"
            fix_button_drivers.config(state="disabled")
            fix_text = "Drivers OK."
        results.append(("Driver Status", status, ""))
        output_box.insert("end", f"Driver Check: {status}\n{fix_text}\n\n")
    except:
        status = "FAIL"
        fix_button_drivers.config(state="normal")
        results.append(("Driver Status", status, ""))
        output_box.insert("end", "Driver check failed\n\n")

# -----------------------------
# Report Window
# -----------------------------
def open_report_window():
    report_window = tk.Toplevel(window)
    report_window.title("Finalize Report")
    report_window.geometry("500x400")

    tk.Label(report_window, text="Select Computer Location:").pack(pady=5)
    location_var = tk.StringVar()
    location_menu = tk.OptionMenu(report_window, location_var, "Office A", "Office B", "Remote", "Other")
    location_menu.pack(pady=5)

    tk.Label(report_window, text="Actions Taken:").pack(pady=5)
    actions_text = tk.Text(report_window, height=5, width=50)
    actions_text.pack(pady=5)

    tk.Label(report_window, text="Outcome:").pack(pady=5)
    outcome_var = tk.StringVar()
    outcome_menu = tk.OptionMenu(report_window, outcome_var, "Resolved", "Pending", "Escalated")
    outcome_menu.pack(pady=5)

    def escalate():
        output_box.insert("end", "Issue escalated to higher-level support\n")
        report_window.destroy()

    tk.Button(report_window, text="Escalate", command=escalate).pack(pady=10)

    def save_report_with_info():
        folder = os.path.join(os.path.dirname(os.path.abspath(_file_)), "Reports")
        if not os.path.exists(folder):
            os.makedirs(folder)
        filename = os.path.join(folder, f"IT_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        with open(filename, "w") as file:
            file.write("==== IT SUPPORT TOOL REPORT ====\n\n")
            file.write(f"Generated: {datetime.now()}\n\n")
            file.write(f"Location: {location_var.get()}\n")
            file.write(f"Outcome: {outcome_var.get()}\n")
            file.write("Actions Taken:\n")
            file.write(actions_text.get("1.0", "end").strip() + "\n\n")
            file.write("Tests Results:\n")
            for test, status, fix in results:
                file.write(f"Test: {test}\nStatus: {status}\n\n")
        output_box.insert("end", f"Report saved to Reports folder\n")
        report_window.destroy()

    tk.Button(report_window, text="Save Report", command=save_report_with_info).pack(pady=5)

# -----------------------------
# Layout Frames
# -----------------------------
system_frame = tk.LabelFrame(window, text="System Health", padx=10, pady=10)
system_frame.pack(fill="x", padx=10, pady=5)

security_frame = tk.LabelFrame(window, text="Security & Drivers", padx=10, pady=10)
security_frame.pack(fill="x", padx=10, pady=5)

report_frame = tk.LabelFrame(window, text="Reports", padx=10, pady=10)
report_frame.pack(fill="x", padx=10, pady=5)

# -----------------------------
# Buttons in System Frame
# -----------------------------
tk.Button(system_frame, text="Check CPU", width=15, command=lambda: run_test(check_cpu)).grid(row=0, column=0, padx=5, pady=5)
tk.Button(system_frame, text="Check RAM", width=15, command=lambda: run_test(check_ram)).grid(row=0, column=1, padx=5, pady=5)
tk.Button(system_frame, text="Check Disk", width=15, command=lambda: run_test(check_disk)).grid(row=0, column=2, padx=5, pady=5)
tk.Button(system_frame, text="Check Network", width=15, command=lambda: run_test(check_network)).grid(row=0, column=3, padx=5, pady=5)

# -----------------------------
# Buttons in Security Frame
# -----------------------------
tk.Button(security_frame, text="Check Antivirus", width=15, command=lambda: run_test(check_antivirus)).grid(row=0, column=0, padx=5, pady=5)
fix_button_antivirus = tk.Button(security_frame, text="Open Antivirus", command=open_antivirus, state="disabled")
fix_button_antivirus.grid(row=1, column=0, padx=5, pady=5)

tk.Button(security_frame, text="Check Updates", width=15, command=lambda: run_test(check_updates)).grid(row=0, column=1, padx=5, pady=5)
fix_button_update = tk.Button(security_frame, text="Open Windows Update", command=open_windows_update, state="disabled")
fix_button_update.grid(row=1, column=1, padx=5, pady=5)

tk.Button(security_frame, text="Check Drivers", width=15, command=lambda: run_test(check_drivers)).grid(row=0, column=2, padx=5, pady=5)
fix_button_drivers = tk.Button(security_frame, text="Open Device Manager", command=open_device_manager, state="disabled")
fix_button_drivers.grid(row=1, column=2, padx=5, pady=5)

# -----------------------------
# Report Frame
# -----------------------------
tk.Button(report_frame, text="Finalize Report", width=25, command=open_report_window).pack(pady=5)

# -----------------------------
# Run the app
# -----------------------------
window.mainloop()