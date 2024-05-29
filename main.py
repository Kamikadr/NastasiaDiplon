import re
import jkj_jk1j as matGenerator
import filter
import enengyChoose
import subprocess
import os

# Открываем файл для чтения
path = input("Enter OBFULEXT.RES path: ")
file_path = path + '/OBFULEXT.RES'
with open(file_path, 'r') as file:
    content = file.readlines()

# Регулярные выражения для поиска данных
iteration_re = re.compile(r'iteration')
j_v_matrix_re = re.compile(r'J=\s*(\d+)\s*(\d+)\s*matrix')
v_j_values_re = re.compile(r'(\d+)\s+V=\s*\d+\s*J=\s*(\d+)\s*(\d+)\s*(\d+)\s*(\d+)\s*([\d.]+(?:E[+-]?\d+)?)\s*')

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
        line = {
             "V": int(v_j_values_match.group(1)),
             "j1":int(v_j_values_match.group(2)),
             "j2":int(v_j_values_match.group(3)),
             "j3":int(v_j_values_match.group(4)),
             "energy":float(v_j_values_match.group(5) + v_j_values_match.group(6))
        }
        data.append(line)
    


# Выводим первые несколько строк данных на экран
for row in data[:5]:
    print(row)

k1 = int(input('Enter Ka1: '))
j = int(input('Enter J0: '))
jn = int(input('Enter Jn: '))
header = ""
controlFile = input("Enter Control file: ")
header += f"{controlFile}     <- ground level file\n"
spectrumFile = input("Enter Spectrum file: ")
header += f"{spectrumFile}       <- spectrum\n"
rangeValue = input("Enter Range: ")
header += f"{rangeValue} <- range\n"
accuracy   = input("Enter Accuracy: ")
header += f"{accuracy} <- accuracy\n"

chousen_blocks = []
for line in data:
    if line["j1"] < j or line["j1"] > jn:
        continue
    if line["j3"] != line["j1"] - k1:
        continue
    if line["j2"] == k1:
        matrix = matGenerator.generateMatrix(line["j2"], line["j1"], line["j1"] - line["j2"])
        block = [line, matrix]
        chousen_blocks.append(block)
    if line["j2"] == k1 + 1:
        matrix = matGenerator.generateMatrix(line["j2"], line["j1"], line["j1"] - line["j2"] + 1)
        block = [line, matrix]
        chousen_blocks.append(block)

APP_PATH = input("Enter search.exe file path: ")
file_path = APP_PATH + "\p"
with open(file_path, 'w') as file:
        file.write(header)
        for line in chousen_blocks:    
            file.write(str(line[0]["energy"]) + '\t' + str(line[0]["j1"]) + " " + str(line[0]["j2"]) + " " + str(line[0]["j3"]) + '\n' + line[1] + '\n')


pIntrisics = subprocess.Popen([os.path.join(APP_PATH, "SEARCH.exe")], cwd=APP_PATH, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = pIntrisics.communicate()
stdout_decoded = stdout.decode('cp1251')
stderr_decoded = stderr.decode('cp1251')
pIntrisics.wait()


with open(APP_PATH + "\search", 'r', encoding='utf-8') as file:
        inputData = file.readlines()
data = filter.format_content(inputData, chousen_blocks)
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


chousen_blocks = enengyChoose.chooseEnergy(filtered_data, 0)
output_file_path = path + "\OBFULEXT.EXP"
with open(output_file_path, 'w', encoding='windows-1251') as file:
     file.write(f"J ЌЂ—.     {j}   J ЉЋЌ.   {jn}  ЉЋ‹ ‹€Ќ€‰  {len(chousen_blocks)}\n")
     for line in chousen_blocks:
          file.write(line + '\n')

input("Press enter to exit;")