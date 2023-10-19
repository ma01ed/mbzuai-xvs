import os
import subprocess

# Define the name of the virtual environment
venv_name = "xvs_env"

# Create the virtual environment
subprocess.run(["python3", "-m", "venv", venv_name])

# Activate the virtual environment
if os.name == "nt":  # For Windows
    activate_path = os.path.join(venv_name, "Scripts", "activate.bat")
else:  # For Unix-based systems
    activate_path = os.path.join(venv_name, "bin", "activate")
subprocess.run(["source", activate_path])

# Install packages from requirements.txt
subprocess.run(["pip3", "install", "-r", "requirements.txt"])
