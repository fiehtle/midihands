#!/usr/bin/env python3
import os
import sys
import subprocess

def main():
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the virtual environment Python
    venv_python = os.path.join(script_dir, 'venv', 'bin', 'python')
    
    # Path to the main script
    main_script = os.path.join(script_dir, 'src', 'main.py')
    
    # Check if venv exists
    if not os.path.exists(venv_python):
        print("Virtual environment not found. Setting up...")
        subprocess.run([sys.executable, '-m', 'venv', 'venv'], cwd=script_dir)
        subprocess.run([venv_python, '-m', 'pip', 'install', '-r', 'requirements.txt'], cwd=script_dir)
    
    # Run the main script using the venv Python
    os.execv(venv_python, [venv_python, main_script])

if __name__ == '__main__':
    main() 