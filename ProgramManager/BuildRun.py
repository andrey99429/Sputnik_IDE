import os
from subprocess import Popen, PIPE


class BuildRun:
    def __init__(self, file_path, exec_path):
        # program: Program
        self.file_path = file_path
        self.exec_path = exec_path

    def build(self):
        process = Popen(args='gcc -o {} {} -lstdc++'.format(self.exec_path, self.file_path),
                        stdout=PIPE,
                        stderr=PIPE,
                        universal_newlines=True,
                        shell=True)
        out, err = process.communicate()
        return out, err

    def run(self):
        process = Popen(args='{}'.format(self.exec_path),
                        stdin=PIPE,
                        stdout=PIPE,
                        stderr=PIPE,
                        universal_newlines=True,
                        shell=True)
        # process.stdin.write('')
        out, err = process.communicate()
        return out, err


"""
'''
Ex: Dialog (2-way) with a Popen()
'''

p = subprocess.Popen('Your Command Here',
                 stdout=subprocess.PIPE,
                 stderr=subprocess.STDOUT,
                 stdin=PIPE,
                 shell=True,
                 bufsize=0)
p.stdin.write('START\n')
out = p.stdout.readline()
while out:
  line = out
  line = line.rstrip("\n")

  if "WHATEVER1" in line:
      pr = 1
      p.stdin.write('DO 1\n')
      out = p.stdout.readline()
      continue

  if "WHATEVER2" in line:
      pr = 2
      p.stdin.write('DO 2\n')
      out = p.stdout.readline()
      continue
'''
.......
'''

out = p.stdout.readline()

p.wait()
"""