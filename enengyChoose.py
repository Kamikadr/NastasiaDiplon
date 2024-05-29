
def chooseEnergy(data, needIndex):
    result = []
    for search_block in data:
        if len(search_block) == 1 or search_block[0]["j2"] != needIndex:
            continue

        k = search_block[0]["j2"]
        applied_blocks = []
        second_priority_blocks = []
        for content_block in search_block[1:]:
            if content_block[0]["j2"] == k:
                applied_blocks.append(content_block)
            else:
                second_priority_blocks.append(content_block)
        
        if len(applied_blocks) == 1:
            result.append(createBlockItem(applied_blocks[0], search_block))
            continue

        if len(applied_blocks) > 1:
            block = findMinIntensityBlock(applied_blocks)
            result.append(createBlockItem(block, search_block))
        else:
            block = findMinIntensityBlock(second_priority_blocks)
            result.append(createBlockItem(block, search_block))

    return result

def findMinIntensityBlock(blocks):
    min_intensity_diff_block = blocks[0]
    min_intensity_diff = blocks[0][0]["intensity"]
    for block in blocks:
        intensityDiff = abs(block[0]["intensity"] - block[-1]["intensity"])
        if min_intensity_diff > intensityDiff:
            min_intensity_diff = intensityDiff
            min_intensity_diff_block = block
    return min_intensity_diff_block


def createBlockItem(block, search_block):
    return f"  {search_block[0]['V']}  {getAverageEnergy(block):.5f}    {getWeigth(block)}          J=  {search_block[0]['j1']}  {search_block[0]['j2']}  {search_block[0]['j3']}   001"

def getWeigth(block):
    intensityDiff = abs(block[0]["intensity"] - block[-1]["intensity"])
    if intensityDiff > 20:
        return 0
    elif intensityDiff < 15:
        return 100
    else:
        return 50
    
def getAverageEnergy(block):
    sum = 0
    for line in block:
        sum += line["level_energy"]
    average = sum / len(block)
    return round(average, 5)
