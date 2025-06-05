def get_length_penalty(info_string, length:int):
    info_list = info_string.split(",")
    for info in info_list:
        min_length, max_length, penalty = info.split()
        if int(min_length) <= length <= int(max_length):
            return penalty