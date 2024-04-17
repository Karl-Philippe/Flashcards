import subprocess
import sys

def main():
    # Create a virtual environment
    subprocess.run([sys.executable, '-m', 'venv', 'venv'])

    # Activate the virtual environment
    activate_script = './venv/Scripts/activate.bat' if sys.platform == 'win32' else './venv/bin/activate'
    subprocess.run([activate_script], shell=True)

    # Install dependencies
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])

    print("Virtual environment setup completed.")

if __name__ == "__main__":
    main()
