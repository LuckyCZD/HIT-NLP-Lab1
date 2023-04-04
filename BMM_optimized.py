from dict import *
import re
import hmm
pattern = r'(\d-*)+$'
pattern2 = r'(\d+.\d{2})$'
word_list = []

def read_dict(dict_path):
    with open(dict_path, 'r', encoding='utf-8') as dic_file:
        while True:
            line = dic_file.readline()
            if not line:
                break
            line = line.rstrip('\n')
            word_list.append(line)

def in_dict(lis, data):
    n = len(lis)
    first = 0
    last = n - 1
    while first <= last:
        mid = (last + first) // 2
        if lis[mid] > data:
            last = mid - 1
        elif lis[mid] < data:
            first = mid + 1
        else:
            return True
    return False


def check_digital(check_str):
    if len(check_str) <=19 and re.match(pattern, check_str) is not None:
        return True
    return False

def BMM(sent_path, BMM_path, max_len):
    with open(sent_path, 'r', encoding='utf-8') as sent_file:
        lines = sent_file.readlines()

    with open(BMM_path, 'w', encoding='utf-8') as seg_file:

        for line in lines:
            result = []
            if line == '\n':
                continue
            i = len(line) - 1
            while i > 0:
                if i - max_len > 0:
                    j = i - max_len
                else:
                    j = 0

                while j < i:
                    if in_dict(word_list, line[j:i]):
                        result.insert(0, line[j:i])
                        i = j
                    if check_digital(line[j:i]):
                        result.insert(0, line[j:i])
                        i = j

                    if j == i - 1 and not (in_dict(word_list, line[j:i])):
                        result.insert(0, line[j:i])
                        i = j
                    else:
                        j = j + 1
            str = '/ '.join(result)
            print(str)
            seg_line = str + '/ ' + '\n'

            seg_file.write(str + '/ ' + '\n')

def BMM_line(line, max_len):
    result = []
    i = len(line)-3
    while i > 0:
        if i - max_len > 0:
            j = i - max_len
        else:
            j = 0

        while j < i:
            if in_dict(word_list, line[j:i]):
                result.insert(0, line[j:i])
                i = j
            if check_digital(line[j:i]):
                result.insert(0, line[j:i])
                i = j

            if j == i - 1 and not (in_dict(word_list, line[j:i])):
                result.insert(0, line[j:i])
                i = j
            else:
                j = j + 1
    str = '/ '.join(result)
    seg_line = str + '/ ' + '\n'
    return seg_line
