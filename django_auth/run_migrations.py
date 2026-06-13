import subprocess
import sys
import os

def run():
    # Ensure we are in the correct directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    print("Running makemigrations...")
    res1 = subprocess.run([sys.executable, "manage.py", "makemigrations"], capture_output=True, text=True)
    print("STDOUT:")
    print(res1.stdout)
    print("STDERR:")
    print(res1.stderr)
    
    print("Running migrate...")
    res2 = subprocess.run([sys.executable, "manage.py", "migrate"], capture_output=True, text=True)
    print("STDOUT:")
    print(res2.stdout)
    print("STDERR:")
    print(res2.stderr)

if __name__ == "__main__":
    run()
