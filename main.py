import re
import csv
import jkj_jk1j as matGenerator
import filter
import subprocess
import os

# Открываем файл для чтения
path = input("Enter OBFULEXT — копия.RES.txt path: ")
file_path = path + '/OBFULEXT — копия.RES.txt'
with open(file_path, 'r') as file:
    content = file.readlines()

# Регулярные выражения для поиска данных
iteration_re = re.compile(r'iteration')
j_v_matrix_re = re.compile(r'J=\s*(\d+)\s*(\d+)\s*matrix')
v_j_values_re = re.compile(r'V=\s*(\d+)\s*J=\s*(\d+)\s*(\d+)\s*(\d+)\s*(\d+)\s*([\d.]+(?:E[+-]?\d+)?)\s*')

data = []
current_j = None

for line in content:
    if iteration_re.search(line):
        continue  # Пропускаем строки с 'iteration'
    j_v_matrix_match = j_v_matrix_re.search(line)
    if j_v_matrix_match:
        current_j = int(j_v_matrix_match.group(1))
        continue
    v_j_values_match = v_j_values_re.search(line)
    if v_j_values_match:
        J1 = int(v_j_values_match.group(2))
        J2 = int(v_j_values_match.group(3))
        J3 = int(v_j_values_match.group(4))
        value = float(v_j_values_match.group(5) + v_j_values_match.group(6))
        line = [J1, J2, J3, value]
        data.append(line)
    


# Выводим первые несколько строк данных на экран
for row in data[:5]:
    print(row)

k1 = int(input('Enter Ka1: '))
j = int(input('Enter J0: '))
jn = int(input('Enter Jn: '))
result = ""
controlFile = input("Enter Control file: ")
result += f"{controlFile}     <- ground level file\n"
spectrumFile = input("Enter Spectrum file: ")
result += f"{spectrumFile}       <- spectrum\n"
rangeValue = input("Enter Range: ")
result += f"{rangeValue} <- range\n"
accuracy   = input("Enter Accuracy: ")
result += f"{accuracy} <- accuracy\n"

for line in data:
    if line[0] < j or line[0] > jn:
        continue
    if line[2] != line[0] - k1:
        continue
    if line[1] == k1:
        matrix = matGenerator.generateMatrix(line[1], line[0], line[0] - line[1])
        block = str(line[3]) + '\t' + str(line[0]) + " " + str(line[1]) + " " + str(line[2]) + '\n' + matrix
        print(block)
        result += block + '\n'
    if line[1] == k1 + 1:
        matrix = matGenerator.generateMatrix(line[1], line[0], line[0] - line[1] + 1)
        block = str(line[3]) + '\t' + str(line[0]) + " " + str(line[1]) + " " + str(line[2]) + '\n' + matrix
        print(block)
        result += block + '\n'

APP_PATH = input("Enter search.exe file path: ")
file_path = APP_PATH + "\p"
with open(file_path, 'w') as file:
            file.write(result)


pIntrisics = subprocess.Popen([os.path.join(APP_PATH, "SEARCH.exe")], cwd=APP_PATH, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = pIntrisics.communicate()
stdout_decoded = stdout.decode('cp1251')
stderr_decoded = stderr.decode('cp1251')
pIntrisics.wait()


with open(APP_PATH + "\search", 'r', encoding='utf-8') as file:
        inputData = file.readlines()
data = filter.format_content(inputData)
output_file_path = input("Enter output file path: ")
# Запись отформатированного содержимого в новый файл
with open(output_file_path, 'w', encoding='utf-8') as file:
    for i in range(4):
        file.write(data[i] + '\n')
    for search_content in data[4:]:
        file.write("Searching " + str(search_content[0]["j1"])  + ' ' + str(search_content[0]["j2"]) + ' ' + str(search_content[0]["j3"]) + " near" + ' ' + str(search_content[0]["energy"]) + '\n')
        file.write('\n')
        for block_content in search_content[1:]:
            for line in block_content:
                file.write(str(line["j1"]) + ' ' + str(line["j2"]) + ' ' + str(line["j3"]) + ' ' + str(line["level_energy"]) + ' ' + str(line["intensity"]) + ' ' + str(line["energy"]))
                file.write('\n')
            file.write('\n')
print(f"Formatted content written to {output_file_path}")


filtered_data = filter.filterEnergy(data[4:])
output_file_path = input("Enter output filtered file path: ")
with open(output_file_path, 'w', encoding='utf-8') as file:
        for i in range(4):
            file.write(data[i] + '\n')
        for search_content in filtered_data:
            file.write("Searching " + str(search_content[0]["j1"])  + ' ' + str(search_content[0]["j2"]) + ' ' + str(search_content[0]["j3"]) + " near" + ' ' + str(search_content[0]["energy"]) + '\n')
            file.write('\n') 
            for block_content in search_content[1:]:
                for line in block_content:
                    file.write(str(line["j1"]) + ' ' + str(line["j2"]) + ' ' + str(line["j3"]) + ' ' + str(line["level_energy"]) + ' ' + str(line["intensity"]) + ' ' + str(line["energy"]))
                    file.write('\n')
                file.write('\n')
input("Press enter to exit;")