
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
            block = getMinIntensityBlock(applied_blocks)
            result.append(createBlockItem(block, search_block))
        else:
            block = getMinIntensityBlock(second_priority_blocks)
            result.append(createBlockItem(block, search_block))

    return result

def chooseBlock(data, needIndex):
    result = []
    for search_block in data:
        if len(search_block) == 1 or search_block[0]["j2"] != needIndex:
            continue
        k = search_block[0]["j2"]
        best_search_blocks = []
        for content_block in search_block[1:]:
            maxEnergy = 0
            minEnergy = 10000000
            flag = True
            currentK = 0
            currentSubblock = []
            minDiff = 10000000
            minDiffBlock = content_block[0]
            applied_blocks = []
            for line in content_block:
                if line["intensity"] >= 100:
                    flag = False
                    currentSubblock = []
                    applied_blocks = []
                    break
                
                if currentK != line["j2"]:
                    diff = maxEnergy - minEnergy
                    if diff < 0.001:
                        if len(currentSubblock) is not  0:
                            applied_blocks.append(currentSubblock)
                    if minDiff > diff:
                        minDiff = diff
                        minDiffBlock = currentSubblock
                    currentK = line["j2"]
                    currentSubblock = []
                currentSubblock.append(line)
                if maxEnergy < line["energy"]:
                    maxEnergy = line["energy"]
                if minEnergy > line["energy"]:
                    minEnergy = line["energy"]
            if not flag:
                continue
            diff = maxEnergy - minEnergy
            if diff < 0.001:
                applied_blocks.append(currentSubblock)
    
            if len(applied_blocks) == 0:
                best_search_blocks.append(minDiffBlock)
                continue
            if applied_blocks == 1:
                best_search_blocks.append(applied_blocks[0])
                continue
            else:
                filtered_blocks = []
                for applied_block in applied_blocks:
                    if applied_block[0]["j2"] == k and abs(applied_block[0]["intensity"] - applied_block[-1]["intensity"]) > 20:
                        filtered_blocks.append(applied_block)
                
                if len(filtered_blocks) == 1:
                    best_search_blocks.append(applied_blocks[0])
                    continue
                elif len(filtered_blocks) > 1:
                    best_search_blocks.append(getMostPriorityBlock(filtered_blocks))
                else:    
                    best_search_blocks.append(getMostPriorityBlock(applied_blocks))
        
        if len(best_search_blocks) == 0:
            continue
        elif len(best_search_blocks) == 1:
            result.append(createBlockItem(best_search_blocks[0], search_block, True))
        else:
            first_filtered_blocks = []
            minDiff = 1000000
            minDiffBlock = best_search_blocks[0]
            for block in best_search_blocks:
                maxEnergy = 0
                minEnergy = 10000000
                for line in block:
                    if maxEnergy < line["energy"]:
                        maxEnergy = line["energy"]
                    if minEnergy > line["energy"]:
                        minEnergy = line["energy"]
                diff = maxEnergy - minEnergy
                if diff < 0.001:
                    first_filtered_blocks.append(block)
                elif diff < minDiff:
                    minDiff = diff
                    minDiffBlock = block
            
            if len(first_filtered_blocks) == 0:
                result.append(createBlockItem(minDiffBlock, search_block, True))
            elif len(first_filtered_blocks) == 1:
                result.append(createBlockItem(first_filtered_blocks[0], search_block, False))
            else:
                second_filtered_blocks = []
                for applied_block in first_filtered_blocks:
                    if applied_block[0]["j2"] == k and abs(applied_block[0]["intensity"] - applied_block[-1]["intensity"]) > 20:
                        second_filtered_blocks.append(applied_block)
                
                if len(second_filtered_blocks) == 1:
                    result.append(createBlockItem(second_filtered_blocks[0], search_block, False))
                elif len(second_filtered_blocks) > 1:
                    result.append(createBlockItem(getMostPriorityBlock(second_filtered_blocks), search_block, False))
                else:    
                    result.append(createBlockItem(getMostPriorityBlock(first_filtered_blocks), search_block, False))

    return result


def getMostPriorityBlock(blocks):
    minBlocks = getMinDiffEnergyBlock(blocks)
    if len(minBlocks) > 1:
        return getLongestBlock(minBlocks)
    return minBlocks[0]

def getMinDiffEnergyBlock(blocks):
    minDiff = 10000000
    minDiffBlock = []
    for applied_block in blocks:
        maxEnergy = 0
        minEnergy = 10000000
        for line in applied_block:
            if maxEnergy < line["energy"]:
                maxEnergy = line["energy"]
            if minEnergy > line["energy"]:
                minEnergy = line["energy"]
        diff = maxEnergy - minEnergy
        if diff == minDiff:
            minDiffBlock.append(applied_block)
        if diff < minDiff:
            minDiff = diff
            minDiffBlock = [applied_block]
    return minDiffBlock



def getLongestBlock(blocks):
    for block in blocks:
        if len(block) == 3:
            return block
    return blocks[0]
def getMinIntensityBlock(blocks):
    min_intensity_diff_block = blocks[0]
    min_intensity_diff = blocks[0][0]["intensity"]
    for block in blocks:
        intensityDiff = abs(block[0]["intensity"] - block[-1]["intensity"])
        if min_intensity_diff > intensityDiff:
            min_intensity_diff = intensityDiff
            min_intensity_diff_block = block
    return min_intensity_diff_block


def createBlockItem(block, search_block, isBadBlock):
    return f"  {search_block[0]['V']}  {getAverageEnergy(block):.5f}    {getWeigth(block, isBadBlock)}          J=  {search_block[0]['j1']}  {search_block[0]['j2']}  {search_block[0]['j3']}   001"

def getWeigth(block, isBadBlock):
    intensityDiff = abs(block[0]["intensity"] - block[-1]["intensity"])
    result = 100
    if isBadBlock:
        result -= 50
    if intensityDiff > 25:
        return result - 50
    else:
        return result
    
def getAverageEnergy(block):
    sum = 0
    for line in block:
        sum += line["energy"]
    average = sum / len(block)
    return round(average, 5)
