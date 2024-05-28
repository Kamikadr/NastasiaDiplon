# Прочитаем содержимое обоих файлов
import re


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

def format_content(input_content):
    pattern = re.compile(r'(\d+)\s+(\d+)\s+(\d+)\s+(\d+\.\d{5})?\s*(\d+\.\d+)\s+(\d+\.\d+)')
    search_pattern = re.compile(r' Searching\s+(\d+)\s+(\d+)\s+(\d+)\s+near\s+(\d+\.\d+)')
    formatted_content = []
    search_block = []
    content_block = []
    for line in input_content:
        if "No" in line:
            continue
        if line.startswith('Range') or line.startswith('Accuracy') or line.startswith('Control file') or line.startswith('Spectrum file'):
            # Add search lines directly
            formatted_content.append(line.strip() + '\n')
        elif line.startswith(' Searching'):
            if len(search_block) != 0:
                formatted_content.append(search_block) 
            search_block = []
            search_pattern_value = search_pattern.search(line)
            line_data = {
                "j1": int(search_pattern_value.group(1)),
                "j2": int(search_pattern_value.group(2)),
                "j3": int(search_pattern_value.group(3)),
                "energy": float(search_pattern_value.group(4))
            }
            search_block.append(line_data)
        else:
            matches = pattern.findall(line)
            if len(matches) == 1 and line[0] == ' ':
                line_data = {
                        "j1": int(matches[0][0]),
                        "j2": int(matches[0][1]),
                        "j3": int(matches[0][2]),
                        "level_energy": float(matches[0][3]),
                        "intensity": float(matches[0][4]),
                        "energy": float(matches[0][5])
                    }
                content_block.append(line_data)
            else:
                if len(content_block) != 0:
                    search_block.append(content_block)
                content_block = []
                for match in matches:
                    line_data = {
                        "j1": int(match[0]),
                        "j2": int(match[1]),
                        "j3": int(match[2]),
                        "level_energy": float(match[3]),
                        "intensity": float(match[4]),
                        "energy": float(match[5])
                    }
                    content_block.append(line_data)


    search_block.append(content_block)
    formatted_content.append(search_block)
    return formatted_content

def filterEnergy(data):
    filtered_data = []
    for searching_block in data:
        item = searching_block[0]["j1"]
        filtered_searching_block = []
        filtered_searching_block.append(searching_block[0])
        
        for content_block in searching_block[1:]:
            filtered_content_block = []
            pair = []
            for line in content_block:
                if len(pair) == 1 and line["j1"] == item and line["j2"] == pair[0]["j2"]:
                    pair.append(line)
                    continue
                if (len(pair) == 2 or len(pair) == 1) and line["j1"] == item + 1 and line["j2"] == pair[0]["j2"]:
                    pair.append(line)
                    for filteredLine in pair:
                        filtered_content_block.append(filteredLine)
                    pair = []
                    continue
                else:
                    pair = []

                if len(pair) == 0 and line["j1"] == item - 1:
                    pair.append(line)
                    continue
            if len(filtered_content_block) != 0:
                filtered_searching_block.append(filtered_content_block)
        
        filtered_data.append(filtered_searching_block)
    return filtered_data
            


if __name__ == "__main__":
    input_file_path = input("Enter file path need to filter: ")
    output_file_path = input("Enter output file path: ")
    # Чтение файлов
    input_content = read_file(input_file_path)

    # Форматирование содержимого
    formatted_content = format_content(input_content)

    # Запись отформатированного содержимого в новый файл
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for i in range(4):
            file.write(formatted_content[i] + '\n')
        for search_content in formatted_content[4:]:
            file.write("Searching " + str(search_content[0]["j1"])  + ' ' + str(search_content[0]["j2"]) + ' ' + str(search_content[0]["j3"]) + " near" + ' ' + str(search_content[0]["energy"]) + '\n')
            file.write('\n')
            for block_content in search_content[1:]:
                for line in block_content:
                    file.write(str(line["j1"]) + ' ' + str(line["j2"]) + ' ' + str(line["j3"]) + ' ' + str(line["level_energy"]) + ' ' + str(line["intensity"]) + ' ' + str(line["energy"]))
                    file.write('\n')
                file.write('\n')
    print(f"Formatted content written to {output_file_path}")

    filteredData = filterEnergy(formatted_content[4:])

    output_file_path = input("Enter output filtered file path: ")
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for i in range(4):
            file.write(formatted_content[i] + '\n')
        for search_content in filteredData:
            file.write("Searching " + str(search_content[0]["j1"])  + ' ' + str(search_content[0]["j2"]) + ' ' + str(search_content[0]["j3"]) + " near" + ' ' + str(search_content[0]["energy"]) + '\n')
            file.write('\n') 
            for block_content in search_content[1:]:
                for line in block_content:
                    file.write(str(line["j1"]) + ' ' + str(line["j2"]) + ' ' + str(line["j3"]) + ' ' + str(line["level_energy"]) + ' ' + str(line["intensity"]) + ' ' + str(line["energy"]))
                    file.write('\n')
                file.write('\n')

