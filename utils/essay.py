def get_length_penalty(info_string, length):
    info_list = info_string.split(",")
    for min_length, max_length, penalty in info_list:
        if min_length <= length <= max_length:
            return penalty