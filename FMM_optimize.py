import re

pattern = r'(\d-*)+$'
pattern2 = r'(\d+.\d{2})$'

class Trie:

    def __init__(self):
        self.root = {}
        self.END = '/'  # 加入这个是为了区分单词和前缀,如果这一层node里面没有/他就是前缀.不是我们要找的单词.

    def insert(self, word) -> None:
        if word not in self.tree:
            self.tree.append(word)
        return True

    def search(self, word):
        if word in self.tree:
            return True
        else:
            return False

word_list = Trie()

def read_dict(dict_path):
    with open(dict_path, 'r', encoding='utf-8') as dic_file:
        while True:
            line = dic_file.readline()
            if not line:
                break
            line = line.rstrip('\n')
            word_list.insert(line)

def check_digital(check_str):
    if len(check_str) <=19 and re.match(pattern, check_str) is not None:
        return True
    if re.match(pattern2, check_str) is not None:
        return True
    return False

def FMM(sent_path, FMM_path):

    with open(sent_path, 'r', encoding='utf-8') as sent_file:
        lines = sent_file.readlines()
    with open(FMM_path, 'w', encoding='utf-8') as seg_file:
        for line in lines:
            result = []
            if line == '\n':
                continue
            i = 0
            while i < len(line) - 1:
                if '\u4e00' <= line[i] <= '\u9fff':
                    max_len = 12
                else:
                    max_len = 26

                if i + max_len < len(line):
                    j = i + max_len
                else:
                    j = len(line)

                while j > i:
                    if word_list.search(line[i:j]):
                        result.append(line[i:j])
                        i = j
                    if check_digital(line[i:j]):
                        result.append(line[i:j])
                        i = j

                    if j == i + 1 and not (word_list.search(line[i:j])):
                        result.append(line[i:j])
                        i = j
                    else:
                        j = j - 1
            str1 = '/ '.join(result)
            str1 = str1.replace('\n', '')
            print(str1)
            seg_file.write(str1+'/ '+'\n')

