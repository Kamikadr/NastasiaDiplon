import jkj_jk1j as matGenerator
def generate_P_data(data,j, jn, k1):
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
    return chousen_blocks