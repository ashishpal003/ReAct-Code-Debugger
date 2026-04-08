"""
Sandbox system for safe execution.

This is CRITICAL:
- Prevents breaking your system
- Isolates dependencies
- Allows repeatable debugging
"""

import os
import shutil
import subprocess
import uuid

class Sandbox:
    def __init__(self, source_path: str, root_dir: str):
        self.source_path = source_path
        self.root_dir = root_dir

        # Unique run ID
        self.id = str(uuid.uuid4())[:8]

        # Sandbix directory
        self.path = os.path.join(root_dir, f"run_{self.id}")


        # Virtual environment path
        self.venv_path = os.path.join(self.path, "venv")


    # -------------------------
    # Setup Methods
    # -------------------------

    def create(self):
        """
        Create sandbox and copy project files
        """
        os.makedirs(self.path, exist_ok=True)

        if os.path.isdir(self.source_path):
            shutil.copytree(self.source_path, self.path, dirs_exist_ok=True)
        else:
            shutil.copy(self.source_path, self.path)
        
    def create_venv(self):
        """
        Create isolate virtual environment
        """
        subprocess.run(
            ["python3", "-m", "venv", self.venv_path],
            check=True
        )

    def pip_install(self, args):
        """
        Run pip inside virtual environment
        """
        pip_path = os.path.join(self.venv_path, "bin", "pip")

        subprocess.run(
            [pip_path] + args,
            cwd=self.path,
            check=False,  # don't crash, let agent handle errors
        )

    def install_dependencies(self):
        """
        Install dependencies from project files
        """
        requirements = os.path.join(self.path, "requirements.txt")
        pyproject = os.path.join(self.path, "pyproject.toml")

        if os.path.exists(requirements):
            print("📦 Installing requirements.txt...")
            self.pip_install(["install", "-r", "requirements.txt"])

        elif os.path.exists(pyproject):
            print("📦 Installing from pyproject.toml...")
            self.pip_install(["install", "."])

    def setup(self):
        """
        Full sandbox setup pipeline
        """
        print(f"🚧 Creating sandbox: {self.path}")

        self.create()
        self.create_venv()
        self.install_dependencies()