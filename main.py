import re
import jkj_jk1j as matGenerator
import filter
import enengyChoose
import exe_user
import obfulext_res_parser
import p_data_generator


def create_P_file(header, p_data_blocks, file_path):
    with open(file_path, 'w') as file:
        file.write(header)
        for line in p_data_blocks:    
            file.write(str(line[0]["energy"]) + '\t' + str(line[0]["j1"]) + " " + str(line[0]["j2"]) + " " + str(line[0]["j3"]) + '\n' + line[1] + '\n')

def readFile(file_path):
    with open(file_path, 'r') as file:
        raw_data = file.readlines()
    return raw_data

def create_P_file_header(controlFile, spectrumFile, rangeValue, accuracy):
    header = ""
    header += f"{controlFile}     <- ground level file\n"
    header += f"{spectrumFile}       <- spectrum\n"
    header += f"{rangeValue} <- range\n"
    header += f"{accuracy} <- accuracy\n"
    return header

def create_search_result_file(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
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
    print(f"Formatted SEARCH content written to {file_path}")

def create_filtered_energy_file(header, data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(header)
        for search_content in data:
            file.write("Searching " + str(search_content[0]["j1"])  + ' ' + str(search_content[0]["j2"]) + ' ' + str(search_content[0]["j3"]) + " near" + ' ' + str(search_content[0]["energy"]) + '\n')
            file.write('\n') 
            for block_content in search_content[1:]:
                for line in block_content:
                    file.write(str(line["j1"]) + ' ' + str(line["j2"]) + ' ' + str(line["j3"]) + ' ' + str(line["level_energy"]) + ' ' + str(line["intensity"]) + ' ' + str(line["energy"]))
                    file.write('\n')
                file.write('\n')

def create_obfulext_exp_file(p_data_blocks, file_path):
    with open(file_path, 'w', encoding='windows-1251') as file:
        file.write(f"J ЌЂ—.     {j}   J ЉЋЌ.   {jn}  ЉЋ‹ ‹€Ќ€‰  {len(p_data_blocks)}\n")
        for line in p_data_blocks:
            file.write(line + '\n')


def run_pipeline(path, k1, j, jn, controlFile, spectrumFile, rangeValue, accuracy, APP_PATH, output_search_file_path, output_filtered_file_path, k):


    obfulext_res_file_path = path + '/OBFULEXT.RES'
    raw_data = readFile(obfulext_res_file_path)
    data = obfulext_res_parser.parseFile(raw_data)
    header = create_P_file_header(controlFile, spectrumFile, rangeValue, accuracy)
    p_data_blocks = p_data_generator.generate_P_data(data, j, jn, k1)
    p_file_path = APP_PATH + "\p"
    create_P_file(header, p_data_blocks, p_file_path)
    exe_user.UseSEARCH(APP_PATH)

    raw_data = readFile(APP_PATH + "\search")
    data = filter.format_content(raw_data, p_data_blocks)
    create_search_result_file(data, output_search_file_path)

    header = ""
    for i in range(4):
        header += data[i] + '\n'
    filtered_data = filter.filterEnergy(data[4:])
    create_filtered_energy_file(header, filtered_data, output_filtered_file_path)

    p_data_blocks = enengyChoose.chooseBlock(filtered_data, k)
    obfulext_exp_path = path + "\OBFULEXT.EXP"
    create_obfulext_exp_file(p_data_blocks, obfulext_exp_path)

    exe_user.UseOBFULEXTS(path)





if __name__ == "__main__":

    
    path = input("Enter OBFULEXT.RES path: ")
    k1 = int(input('Enter Ka1: '))
    j = int(input('Enter J0: '))
    jn = int(input('Enter Jn: '))
    controlFile = input("Enter Control file: ")
    spectrumFile = input("Enter Spectrum file: ")
    rangeValue = input("Enter Range: ")
    accuracy   = input("Enter Accuracy: ")
    APP_PATH = input("Enter search.exe file path: ")
    output_search_file_path = input("Enter output file path: ")
    output_filtered_file_path = input("Enter output filtered file path: ")
    k = int(input("Enter k: "))

    flag = "1"
    while flag == "1":
        iteration_count = int(input("Enter count of iteration: "))
        for i in range(0, iteration_count, 1):
            run_pipeline(path, k1, j, jn, controlFile, spectrumFile, rangeValue, accuracy, APP_PATH, output_search_file_path, output_filtered_file_path, k)
        flag = input("Do you want to continue? Enter '1' to continue or anything else to exit: ")

