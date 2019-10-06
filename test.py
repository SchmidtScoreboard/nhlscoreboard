import os
import time
import subprocess
import signal

def run(file):
    pid = os.fork()
    if pid == 0:
        #Parent
        print("Parent sleeping")
        time.sleep(10)
        print("Parent waking")
        exit(2)
    else:
        #Child
        time.sleep(1)
        os.kill(os.getppid(), signal.SIGKILL)
        subprocess.run(file) 
        exit(3)

run("hotspot_off.sh")