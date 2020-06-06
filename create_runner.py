import os
import sys
import bz2
import base64
import hashlib

def load_binary_into_string(binaryfile):
    with open(binaryfile, 'rb') as _file:
        data = _file.read()
    print(hashlib.md5(data).hexdigest())
    return base64.b64encode(bz2.compress(data)).decode('utf-8')
    

def main():
    runner_file = """
import os
import bz2
import base64
import tempfile
import subprocess
import threading

# This is an auto generated file that will run a series of binaries from memory.

class DataRunner(threading.Thread):
    def __init__(self, base64data):
        self.stdout = None
        self.stderr = None
        self.base64data = base64data
        self.binPid = None
        threading.Thread.__init__(self)
    
    def run(self):
        data = bz2.decompress(base64.b64decode(self.base64data.encode('utf-8')))
        fd, path = tempfile.mkstemp(suffix='.exe')
        os.write(fd, data)
        os.close(fd)
        p = subprocess.Popen(path, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.stdout, self.stderr = p.communicate()
"""
    filenames = []
    files_to_execute = []
    for i in sys.argv[1:]:
        files_to_execute.append(load_binary_into_string(i))
        filenames.append(i)
    runner_file += f"""
filenames = {filenames}
files_to_execute = {files_to_execute}

threads = list()
for x,i in zip(filenames, files_to_execute):
    threads.append(DataRunner(i))

for thr in threads:
    thr.start()

for thr in threads:
    thr.join()

for thr in threads:
    print(thr.stdout)

"""
    with open('runner_script.py', 'w') as _file:
        _file.write(runner_file)
    print("Compiled binaries into : runner_script.exe")

if __name__ == "__main__":
    main()
