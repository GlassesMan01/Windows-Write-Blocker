import os
import psutil
import subprocess
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import ctypes
import sys
import winreg as reg
from datetime import datetime
from tkinter import filedialog


# Check if the script is running as administrator
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Relaunch the script with admin privileges if not already elevated
def ensure_admin():
    if not is_admin():
        print("Attempting to relaunch as admin...")
        try:
            # Relaunch with admin privileges and add an argument to mark the elevated instance
            result = ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, f'"{sys.argv[0]}" --elevated', None, 1
            )
            if result <= 32:  # Error if ShellExecuteW fails
                raise Exception("Failed to relaunch with admin privileges.")
            print("Exiting non-admin process.")
            sys.exit()  # Exit the current non-elevated process
        except Exception as e:
            print(f"Failed to obtain admin privileges: {e}")
            messagebox.showerror("Admin Privileges Required", "This application requires administrative privileges to run.")
            sys.exit()  # Exit if admin privileges cannot be obtained

# Check for the `--elevated` flag to skip re-invoking `ensure_admin`
if "--elevated" not in sys.argv:
    ensure_admin()

# Enable write protection (read-only) for the selected drive
def enable_write_block(device):
    try:
        if not device:
            messagebox.showwarning("Warning", "No device selected!")
            return

        volume_letter = device[0][0]  # Extract the volume letter (e.g., "F")
        is_removable = check_removable(volume_letter)

        if is_removable:
            set_removable_write_protection(True)
        else:
            script_name = generate_diskpart_script(volume_letter, enable=True)
            result = subprocess.run(["diskpart", "/s", script_name], capture_output=True, text=True)

            if result.returncode == 0:
                log_action(f"Write protection enabled on {device}")
                messagebox.showinfo("Success", f"Write protection enabled on {device}")
            else:
                raise Exception(result.stderr.strip())

            # Clean up the script
            os.remove(script_name)
    except Exception as e:
        log_action(f"Error enabling write protection: {str(e)}")
        messagebox.showerror("Error", f"Could not enable write protection: {str(e)}")

# Disable write protection for the selected drive
def disable_write_block(device):
    try:
        if not device:
            messagebox.showwarning("Warning", "No device selected!")
            return

        volume_letter = device[0][0]  # Extract the volume letter (e.g., "F")
        is_removable = check_removable(volume_letter)

        if is_removable:
            set_removable_write_protection(False)
        else:
            script_name = generate_diskpart_script(volume_letter, enable=False)
            result = subprocess.run(["diskpart", "/s", script_name], capture_output=True, text=True)

            if result.returncode == 0:
                log_action(f"Write protection disabled on {device}")
                messagebox.showinfo("Success", f"Write protection disabled on {device}")
            else:
                raise Exception(result.stderr.strip())

            # Clean up the script
            os.remove(script_name)
    except Exception as e:
        log_action(f"Error disabling write protection: {str(e)}")
        messagebox.showerror("Error", f"Could not disable write protection: {str(e)}")

# Set write protection for removable devices using the registry
def set_removable_write_protection(enable=True):
    try:
        key_path = r"SYSTEM\CurrentControlSet\Control\StorageDevicePolicies"
        key = reg.CreateKey(reg.HKEY_LOCAL_MACHINE, key_path)
        reg.SetValueEx(key, "WriteProtect", 0, reg.REG_DWORD, 1 if enable else 0)
        reg.CloseKey(key)
        log_action(f"Registry write protection {'enabled' if enable else 'disabled'} for removable devices.")
        messagebox.showinfo("Success", f"Write protection {'enabled' if enable else 'disabled'} for removable devices.")
    except Exception as e:
        log_action(f"Error setting registry write protection: {str(e)}")
        messagebox.showerror("Error", f"Could not set registry write protection: {str(e)}")

# Generate the diskpart script for enabling/disabling write protection
def generate_diskpart_script(volume_letter, enable=True):
    script_name = f"{'enable' if enable else 'disable'}_{volume_letter}.txt"
    with open(script_name, "w") as script:
        script.write(f"select volume {volume_letter}\n")
        script.write("attributes volume " + ("set readonly\n" if enable else "clear readonly\n"))
    log_action(f"Diskpart script generated: {script_name}")
    return script_name

# Check if the device is removable
def check_removable(volume_letter):
    for disk in psutil.disk_partitions(all=True):
        if disk.device.startswith(volume_letter):
            return 'removable' in disk.opts.lower()
    return False

# Log actions in the GUI
def log_action(action):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_text.insert(tk.END, f"[{timestamp}] {action}\n")
    log_text.see(tk.END)

# Refresh the list of available drives
def refresh_devices():
    device_list.delete(0, tk.END)
    for disk in psutil.disk_partitions():
        device_list.insert(tk.END, (disk.device))
    log_action("Device list refreshed.")

# Execute actions based on user input
def execute_action(action):
    selected = device_list.curselection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a device from the list!")
        return

    device = device_list.get(selected)
    if action == "enable":
        enable_write_block(device)
    elif action == "disable":
        disable_write_block(device)

# Export logs to a file
def export_logs():
    try:
        log_content = log_text.get("1.0", tk.END)
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(log_content)
            messagebox.showinfo("Success", f"Logs exported to {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not export logs: {str(e)}")

# Main GUI
root = tb.Window(themename="darkly")
root.title("Windows Write Blocker")
root.geometry("500x600")

# Set the icon for the window
icon_path = "E:\\Writeblocker\\Windows_Write_Blocker.ico"
root.iconbitmap(icon_path)

# Device Selection
device_frame = tb.LabelFrame(root, text="Devices", bootstyle=PRIMARY)
device_frame.pack(fill="x", padx=10, pady=10)

device_list = tk.Listbox(device_frame, height=6)
device_list.pack(fill="x", padx=5, pady=5)

refresh_button = tb.Button(device_frame, text="Refresh Devices", command=refresh_devices, bootstyle=INFO)
refresh_button.pack(pady=10)

# Action Buttons
action_frame = tb.Frame(root)
action_frame.pack(pady=10)

enable_button = tb.Button(action_frame, text="Enable Write Protection", command=lambda: execute_action("enable"), bootstyle=SUCCESS)
enable_button.grid(row=0, column=0, padx=10)

disable_button = tb.Button(action_frame, text="Disable Write Protection", command=lambda: execute_action("disable"), bootstyle=DANGER)
disable_button.grid(row=0, column=1, padx=10)

# Log Output
log_frame = tb.LabelFrame(root, text="Log", bootstyle=SECONDARY)
log_frame.pack(fill="both", expand=True, padx=10, pady=10)

log_text = tk.Text(log_frame, wrap=tk.WORD, height=10)
log_text.pack(fill="both", expand=True, padx=5, pady=5)

# Export Log Button
export_button = tb.Button(root, text="Export Logs", command=export_logs, bootstyle=SECONDARY)
export_button.pack(pady=15)

# Initialize device list
refresh_devices()

# Run the GUI loop
root.mainloop()
