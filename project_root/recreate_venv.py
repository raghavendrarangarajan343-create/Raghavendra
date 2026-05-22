import os
import shutil
import subprocess
import sys

def main():
    project_root = os.path.dirname(os.path.abspath(__file__))
    venv_path = os.path.join(project_root, "venv")
    venv_old_path = os.path.join(project_root, "venv_old")

    print(f"Project root: {project_root}")
    
    # 1. Backup old venv if it exists and venv_old doesn't already exist
    if os.path.exists(venv_path):
        if os.path.exists(venv_old_path):
            print("venv_old already exists. Removing it first...")
            shutil.rmtree(venv_old_path)
        print("Backing up current broken venv to venv_old...")
        os.rename(venv_path, venv_old_path)
    
    # 2. Recreate virtual environment using current system python
    print("Creating new virtual environment 'venv'...")
    try:
        subprocess.check_call([sys.executable, "-m", "venv", venv_path])
        print("Virtual environment created successfully.")
    except Exception as e:
        print(f"Error creating virtual environment: {e}")
        # Restore backup if failed
        if os.path.exists(venv_old_path) and not os.path.exists(venv_path):
            os.rename(venv_old_path, venv_path)
        sys.exit(1)
        
    # 3. Path to pip in the new venv
    if os.name == "nt":
        pip_exe = os.path.join(venv_path, "Scripts", "pip.exe")
    else:
        pip_exe = os.path.join(venv_path, "bin", "pip")
        
    # 4. Install dependencies
    dependencies = [
        "pytest",
        "pytest-html",
        "python-dotenv",
        "langchain",
        "langchain-openai",
        "langgraph",
        "supabase",
        "pydantic"
    ]
    
    print(f"Installing dependencies into the new virtual environment: {', '.join(dependencies)}")
    try:
        subprocess.check_call([pip_exe, "install", "--upgrade", "pip"])
        subprocess.check_call([pip_exe, "install"] + dependencies)
        print("Dependencies installed successfully.")
    except Exception as e:
        print(f"Error installing dependencies: {e}")
        print("You may need to run 'pip install' manually inside the virtualenv.")

if __name__ == "__main__":
    main()
