import subprocess
import time
import sys
import threading
import os

def animated_loading():
    chars = "/—\|" 
    i = 0
    start_time = time.time()
    
    print("\nStarting Buildozer Android Build...")
    print("This process may take several minutes.\n")
    
    # Initial progress bar state
    sys.stdout.write(f"\r[{' ' * 20}] 0% - Initializing...")
    sys.stdout.flush()
    
    return start_time

def format_time(seconds):
    m, s = divmod(seconds, 60)
    return f"{int(m)}m {int(s)}s"

def run_build():
    start_time = animated_loading()
    
    # Start the build process
    process = subprocess.Popen(
        ["buildozer", "android", "debug"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )
    
    # Progress tracking variables
    progress = 0
    max_progress = 100
    
    # Keywords to estimate progress (heuristic)
    stages = {
        "Check configuration tokens": 5,
        "Prepare the build": 10,
        "Check requirements": 15,
        "Install platform": 25,
        "Apache ANT": 30,
        "Android SDK": 35,
        "Android NDK": 40,
        "Compiling": 50,
        "Cython": 60,
        "Packaging": 80,
        "Signing": 90,
        "APK generated": 100
    }
    
    current_stage = "Initializing"
    
    while True:
        line = process.stdout.readline()
        if not line and process.poll() is not None:
            break
            
        if line:
            # Update progress based on keywords
            for key, val in stages.items():
                if key in line:
                    progress = val
                    current_stage = key
                    break
            
            # Calculate elapsed time
            elapsed = time.time() - start_time
            time_str = format_time(elapsed)
            
            # Create progress bar
            bar_length = 20
            filled_length = int(bar_length * progress // 100)
            bar = '#' * filled_length + '-' * (bar_length - filled_length)
            
            # Update display
            sys.stdout.write(f"\r[{bar}] {progress}% - {current_stage} (Time: {time_str})")
            sys.stdout.flush()
            
            # Log full output to file for debugging
            with open("build_log_full.txt", "a") as f:
                f.write(line)

    return_code = process.poll()
    total_time = time.time() - start_time
    
    print("\n")
    if return_code == 0:
        print(f"✅ Build Successful!")
        print(f"⏱️  Total Time: {format_time(total_time)}")
        
        # Find the APK
        bin_dir = os.path.join(os.getcwd(), "bin")
        if os.path.exists(bin_dir):
            apks = [f for f in os.listdir(bin_dir) if f.endswith(".apk")]
            if apks:
                # Get the most recent APK
                latest_apk = max([os.path.join(bin_dir, f) for f in apks], key=os.path.getctime)
                print(f"📦 APK Location: {latest_apk}")
    else:
        print(f"❌ Build Failed! Check 'build_log_full.txt' for details.")

if __name__ == "__main__":
    # Clean previous log
    if os.path.exists("build_log_full.txt"):
        os.remove("build_log_full.txt")
        
    try:
        run_build()
    except KeyboardInterrupt:
        print("\n\nBuild cancelled by user.")
