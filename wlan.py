import subprocess
import re
from collections import defaultdict

def get_name_strength_map():
    ret = defaultdict(set)
    proc1 = subprocess.Popen(['sudo', 'iwlist', 'scan'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc2 = subprocess.Popen(['grep', 'ESSID\|Signal level'], stdin=proc1.stdout, stdout = subprocess.PIPE, stderr= subprocess.PIPE)
    proc1.stdout.close()
    quality = 0
    signal_level = -1
    while True:
        line = proc2.stdout.readline()
        if not line:
            break
        line = line.decode("utf-8").strip()
        match = re.search('ESSID:"(.*)"', line)
        if match is not None:
            # if match.group(1) is not "":
            ret[match.group(1)].add((quality, signal_level))
            continue 
        
        match = re.search('Quality=(.*) Signal level=(.*) dBm', line)
        if match is not None:
            quality = match.group(1).strip()
            signal_level = match.group(2).strip()

    return ret

if __name__ == "__main__":
    print(get_name_strength_map())
