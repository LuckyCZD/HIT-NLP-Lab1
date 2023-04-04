
import re

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

def in_dict(word):
    return word in word_list

def check_digital(check_str):
    if len(check_str) <=19 and re.match(pattern, check_str) is not None:
        return True
    if re.match(pattern2, check_str) is not None:
        return True
    return False

def FMM(sent_path, FMM_path, max_len):
    with open(sent_path, 'r', encoding='utf-8') as sent_file:
        lines = sent_file.readlines()
    with open(FMM_path, 'w', encoding='utf-8') as seg_file:
        for line in lines:
            result = []
            if line == '\n':
                continue
            i = 0
            while i < len(line) - 1:
                if i + max_len < len(line):
                    j = i + max_len
                else:
                    j = len(line)
                while j > i:
                    if in_dict(line[i:j]):
                        result.append(line[i:j])
                        i = j
                    if check_digital(line[i:j]):
                        result.append(line[i:j])
                        i = j

                    if j == i + 1 and not (in_dict(line[i:j])):
                        result.append(line[i:j])
                        i = j
                    else:
                        j = j - 1
            str1 = '/ '.join(result)
            str1 = str1.replace('\n', '')
            print(str1)
            seg_file.write(str1+'/ '+'\n')

