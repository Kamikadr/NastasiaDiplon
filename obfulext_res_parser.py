import re
# Регулярные выражения для поиска данных
# Пример строки 10 V= 1  J=  3   0   3      2699.225910      2699.068338  .15757E+02    100                     v3
iteration_re = re.compile(r'(\d+)\s+iteration')
j_v_matrix_re = re.compile(r'J=\s*(\d+)\s*(\d+)\s*matrix')
v_j_values_re = re.compile(r'''
                           (\d+)\s+V=\s*\d+\s*J=\s*(\d+)\s*(\d+)\s*(\d+)\s*     # Начальные значения 10 V= 1  J=  3   0   3
                           (?:([\d.]+)\s+)?                                     # Первое число с плавающей точкой (необязательное) 2699.225910
                           ([\d.]+)\s+                                          # Второе число с плавающей точкой 2699.068338
                           (?:([-+]?\d*\.\d+(?:[eE][-+]?\d+)?)\s+)?                     # Третье число с плавающей точкой или в экспоненциальной нотации (необязательное) .15757E+02
                           (?:([\d.]+)\s+)?                                     # Четвертое число с возможной плавающей точкой (необязательное) 100
                           v3                                                   # v3
                           ''', re.VERBOSE)
def parseFile(raw_data, neededIteration):
    header = ""
    data = []
    line_counter = 0
    need_parce = False
    for line in raw_data:
        
        iteration_re_match = iteration_re.search(line)
        if iteration_re_match:
            if int(iteration_re_match.group(1)) == neededIteration:
                need_parce = True
            continue  # Пропускаем строки с 'iteration'
        if need_parce:
            if line_counter < 10:
                header += line
                line_counter += 1
                continue


            j_v_matrix_match = j_v_matrix_re.search(line)
            if j_v_matrix_match:
                continue
            v_j_values_match = v_j_values_re.search(line)
            
            if v_j_values_match:
                #for group_num, group in enumerate(v_j_values_match.groups(), 1):
                 #   print(f"Group {group_num}: {group}")
                line = {
                    "V": int(v_j_values_match.group(1)),
                    "j1":int(v_j_values_match.group(2)),
                    "j2":int(v_j_values_match.group(3)),
                    "j3":int(v_j_values_match.group(4)),
                    "energy":float(v_j_values_match.group(6)),
                    "diff": v_j_values_match.group(7)
                }
                data.append(line)

    # Выводим первые несколько строк данных на экран
    #for row in data[:5]:
        #print(row)
    data.append(header)
    return data
