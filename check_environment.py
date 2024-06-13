import sys
import platform
import subprocess
import os

required_python_version = (3, 12)  # Replace with your minimum required version
required_libraries = ["tkinter", "pandas"]  # Replace with your libraries from requirements.txt
venv_activation_scripts = {
    "posix": ["bin/activate"],
    "nt": ["Scripts\\activate.bat", "Scripts\\Activate.ps1"]
}

def check_python_version():
  if sys.version_info >= required_python_version:
    print(f"You have Python {sys.version}, which is compatible.")
  else:
    print(f"Your Python version {sys.version} is not compatible.")
    print(f"Minimum required version is Python {required_python_version[0]}.{required_python_version[1]}.")
    print("Please upgrade your Python version or use a virtual environment with the required version.")

def check_libraries():
  missing_libraries = []
  for library in required_libraries:
    try:
      subprocess.run(["pip", "show", library], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
      missing_libraries.append(library)
  if missing_libraries:
    print(f"The following libraries seem to be missing: {', '.join(missing_libraries)}")
    print("Please install them using `pip install` in your virtual environment.")
    
def activate_venv(script_path):
    try:
        if os.name == 'posix':
            subprocess.run(['source', script_path], shell=True, check=True, executable='/bin/bash')
        elif os.name == 'nt':
            subprocess.run([script_path], shell=True, check=True)
        print("Virtual environment activated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to activate the virtual environment: {e}")
    

def check_venv_activation_scripts():
    system_type = os.name
    possible_venv_dirs = ["venv", "."]  # Check 'venv' directory first, then current directory

    if system_type in venv_activation_scripts:
        for venv_dir in possible_venv_dirs:
            missing_scripts = []
            for script in venv_activation_scripts[system_type]:
                script_path = os.path.join(venv_dir, script)
                if not os.path.exists(script_path):
                    missing_scripts.append(script)
            if not missing_scripts:
                print(f"All necessary virtual environment activation scripts are present in '{venv_dir}'.")
                return
        print(f"The following virtual environment activation scripts are missing: {', '.join(missing_scripts)}")
        print("Please ensure your virtual environment is correctly set up.")
    else:
        print(f"Unsupported OS type: {system_type}. Cannot check for activation scripts.")

def main():
  check_python_version()
  check_libraries()
  check_venv_activation_scripts()

if __name__ == "__main__":
  main()