
import subprocess
import sys
import time
import threading
import re

def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='#'):
    """
    Call in a loop to create terminal progress bar
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} [{bar}] {percent}% {suffix}')
    sys.stdout.flush()

def run_buildozer():
    print("Starting Buildozer Android Debug Build...")
    
    # Define milestones to estimate progress (more granular)
    milestones = [
        ("Check configuration tokens", 2),
        ("Prepare build", 5),
        ("Check requirements for android", 8),
        ("Install platform", 12),
        ("Apache ANT found", 15),
        ("Android SDK found", 18),
        ("Android NDK found", 22),
        ("Check application requirements", 25),
        ("Compile platform", 30),
        ("Compile hostpython3", 35),
        ("Compile setuptools", 40),
        ("Compile kivy", 50),
        ("Compile plyer", 55),
        ("Compile openssl", 60),
        ("Building package", 70),
        ("Copying libraries", 75),
        ("Packaging", 80),
        ("Generate APK", 85),
        ("Sign APK", 90),
        ("Align APK", 95),
        ("Build finished successfully", 100)
    ]
    
    current_progress = 0
    print_progress_bar(0, 100, prefix='Progress:', suffix='Starting...', length=20)

    log_file = "build_full_log.txt"
    print(f"Full log will be saved to: {log_file}")
    
    try:
        with open(log_file, "w", encoding="utf-8") as log_f:
            log_f.write(f"--- Build started at {time.ctime()} ---\n")
            
            # Run buildozer command
            process = subprocess.Popen(
                ["buildozer", "android", "debug"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
    
            # Read output line by line
            for line in iter(process.stdout.readline, ''):
                log_f.write(line)
                log_f.flush()
                line = line.strip()
                if not line:
                    continue
                
                # Check for milestones
                for msg, progress in milestones:
                    if msg.lower() in line.lower():
                        if progress > current_progress:
                            current_progress = progress
                            print_progress_bar(current_progress, 100, prefix='Progress:', suffix=f"{msg[:25]:<25}", length=30)
                        break
                
                # If error, print it immediately
                if "error" in line.lower() or "failed" in line.lower() or "exception" in line.lower():
                    # Check if it's a real exit error or just a log message
                    if "stderr:" in line.lower() or "command failed" in line.lower():
                        sys.stdout.write(f"\n[CRITICAL] {line}\n")
    
            process.wait()
            
            if process.returncode == 0:
                print_progress_bar(100, 100, prefix='Progress:', suffix='Complete!                 ', length=30)
                print("\n\nBuild Successful! APK should be in the bin directory.")
            else:
                print(f"\n\nBuild Failed (Exit Code: {process.returncode}).")
                print(f"Check the last lines of {log_file} for details.")
            
    except FileNotFoundError:
        print("\nError: 'buildozer' command not found. Make sure it is installed and in your PATH.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    run_buildozer()
