import subprocess
import os

def check_access(directory):
    test_file = os.path.join(directory, 'access_test.tmp')
    try:
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        return True
    except Exception as e:
        return False

APP_PATH = input("Enter search.exe file path: ").strip()
path = os.path.join(APP_PATH, "SEARCH.exe")

# Проверка существования и прав доступа к исполняемому файлу
if not os.path.exists(path):
    print(f"The file {path} does not exist.")
    exit(1)

if not os.access(path, os.X_OK):
    print(f"Execute permission denied for {path}.")
    exit(1)

# Проверка прав доступа к директории
if not check_access(APP_PATH):
    print(f"Access to directory {APP_PATH} denied.")
    exit(1)

try:
    # Запуск исполняемого файла
    pIntrisics = subprocess.Popen([path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=APP_PATH)
    stdout, stderr = pIntrisics.communicate()
    
    # Попробуем декодировать вывод с использованием кодировки cp1251
    try:
        stdout_decoded = stdout.decode('cp1251')
        stderr_decoded = stderr.decode('cp1251')
    except UnicodeDecodeError:
        # Если декодирование с cp1251 не удается, используем латинскую кодировку
        stdout_decoded = stdout.decode('latin1')
        stderr_decoded = stderr.decode('latin1')

    # Печать вывода и ошибок
    print("Standard Output:\n", stdout_decoded)
    print("Standard Error:\n", stderr_decoded)
    
    if pIntrisics.returncode != 0:
        print(f"SEARCH.exe exited with code {pIntrisics.returncode}")
        exit(1)
except Exception as e:
    print(f"Error running SEARCH.exe: {e}")
    exit(1)
