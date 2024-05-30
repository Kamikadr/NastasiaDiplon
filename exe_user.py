import os
import subprocess

def UseOBFULEXTS(path):
    pIntrisics = subprocess.Popen([os.path.join(path, "OBFULEXTS.exe")], cwd=path,stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    first_input = "1\n"
    pIntrisics.stdin.write(first_input.encode('cp1251'))
    pIntrisics.stdin.flush()
    pIntrisics.stdin.write("\n".encode('cp1251'))
    pIntrisics.stdin.flush()

    pIntrisics.stdin.close()
    stdout, stderr = pIntrisics.communicate()
    stdout_decoded = stdout.decode('cp1251')
    stderr_decoded = stderr.decode('cp1251')
    print(f"OBFULEXTS output:\n{stdout_decoded}\n")
    print(f"OBFULEXTS errors:\n{stderr_decoded}\n")


def UseSEARCH(path):
    pIntrisics = subprocess.Popen([os.path.join(path, "SEARCH.exe")], cwd=path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = pIntrisics.communicate()
    stdout_decoded = stdout.decode('cp1251')
    stderr_decoded = stderr.decode('cp1251')
    print(f"SEARCH output:\n{stdout_decoded}\n")
    print(f"SEARCH errors:\n{stderr_decoded}\n")
    pIntrisics.wait()