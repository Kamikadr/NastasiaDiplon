import re
import csv

# Открываем файл для чтения
path = input()
file_path = path + '/OBFULEXT — копия.RES.txt'
with open(file_path, 'r') as file:
    content = file.readlines()

# Регулярные выражения для поиска данных
iteration_re = re.compile(r'iteration')
j_v_matrix_re = re.compile(r'J=\s*(\d+)\s*(\d+)\s*matrix')
v_j_values_re = re.compile(r'V=\s*(\d+)\s*J=\s*(\d+)\s*(\d+)\s*(\d+)\s*(\d+)\s*([\d.]+E[+-]?\d+)\s*\S*')

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
        V = int(v_j_values_match.group(1))
        J1 = int(v_j_values_match.group(2))
        J2 = int(v_j_values_match.group(3))
        J3 = int(v_j_values_match.group(4))
        value = float(v_j_values_match.group(6))
        data.append((current_j, V, J1, J2, J3, value))

# Записываем данные в CSV файл
output_file_path = path + '/parsed_quantum_numbers.csv'
with open(output_file_path, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    # Записываем заголовок
    csv_writer.writerow(['J', 'V', 'J1', 'J2', 'J3', 'Value', 'Label'])
    # Записываем строки данных
    for row in data:
        csv_writer.writerow(row)

# Выводим первые несколько строк данных на экран
for row in data[:5]:
    print(row)

