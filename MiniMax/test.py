

def old(actionables):
    actionables_list = []
    mask = 0x8000000000000000
    for i in range(64):
        if mask & actionables != 0:
            actionables_list.append(mask)
        mask = mask >> 1
    
    return actionables_list

def new(actionables):
    actionables_list = [1 << i for i in range(actionables.bit_length()) if actionables & (1 << i)]
    return actionables_list


if __name__ == "__main__":
    actionables = 0x0000000000000018
    print(old(actionables))
    print(new(actionables))
