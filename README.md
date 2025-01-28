# Windows Write Blocker

A Python-based GUI tool for enabling and disabling write protection on Windows devices and external removable devices. An executable (.exe) version of the tool is also provided for ease of use, so users without Python installed can run the application directly.

## Features
- **Device List**: Displays all available devices (internal and external drives) for selection.
- **Enable Write Protection**: Protect selected devices from being modified by enabling write protection.
- **Disable Write Protection**: Remove write protection from selected devices.
- **Log System**: Tracks actions performed within the tool with detailed timestamps.
- **Export Logs**: Allows exporting logs for documentation and auditing purposes.
- **Modern GUI**: Built using ttkbootstrap for a clean and professional look.

## Requirements

### For Python Script
- **Operating System**: Windows 10/11 (Admin privileges required).
- **Python Version**: Python 3.7 or higher.
- **Dependencies**:
    - `ttkbootstrap`
    - `psutil`

- **Install dependencies**:
  ```bash
  pip install ttkbootstrap psutil
### For .exe File
- **Operating System**: Windows 10/11 (Admin privileges required).
- **No Python Required**: Simply double-click the `.exe` file to run the application.

## How to Use

### Option 1: Using the .exe File
1. Navigate to the folder containing `Windows_Write_Blocker.exe`.
2. Right-click on the `.exe` file and choose **Run as Administrator** (required for device modification).
3. Follow the on-screen instructions to enable/disable write protection and view logs.

### Option 2: Using the Python Script
1. Ensure Python is installed on your system.
2. Clone the repository or download the `Windows WriteBlocker.py` file.
3. Install the required dependencies (see above).
4. Run the script with Python:
   ```bash
   python Windows WriteBlocker.py
## How It Works

### Device Detection
The application lists all storage devices connected to the system.

### Enable/Disable Write Protection
- **For removable devices**: Write protection is managed via the Windows registry.
- **For internal drives**: Write protection is applied using diskpart commands.

### Logging
All actions (e.g., enabling/disabling write protection) are logged with timestamps in the application interface.

### Log Export
Users can export the logs to a `.txt` file for auditing or documentation purposes.



## File Structure
- **Windows_Write_Blocker/**
- **│**
- **├── Windows_Write_Blocker.py     # Main Python script**
- **├── Windows_Write_Blocker.exe    # Standalone executable version**
- **├── Windows_Write_Blocker.ico    # Icon file (optional)**
- **└── README.md                    # Project documentation**

## Important Notes
- **Admin Privileges**: Both the script and `.exe` require administrator privileges to function properly.
- **Diskpart Script**: The tool uses temporary diskpart scripts for enabling/disabling write protection on internal drives.
- **Removable Device Write Protection**: Registry changes may require a restart to take effect in some cases.
- **Executable Build**: The `.exe` file was created using pyinstaller or a similar tool, ensuring compatibility with systems without Python installed.
- **External Device**: You may need to remove or plug in the device again after using the write protection feature.

## Known Issues
- **Diskpart Execution**: Ensure diskpart is accessible from the command line.
- **Removable Device Write Protection**: Registry changes may require a restart to take effect in some cases.


## License
This project is licensed under the MIT License. Feel free to modify and use it as needed.
