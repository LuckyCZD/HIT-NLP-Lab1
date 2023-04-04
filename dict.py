seg_path = 'data/199801_seg&pos.txt'
sent_path = 'data/199801_sent.txt'
dict_path = 'data/dic.txt'
FMM_path = 'data/seg_FMM.txt'
BMM_path = 'data/seg_BMM.txt'

result_path = 'data/seg_LM.txt'
result_path_2 = 'data/seg_out_bi_hmm.txt'

all_path = 'data/hmm/all.txt'
hmm_train_path = 'data/hmm/train.txt'
hmm_test_path = 'data/hmm/test.txt'
hmm_sent_path = 'data/hmm/test_sent.txt'

def create_dict(data_path, dict_path):
    maxlen = 0
    word_set = set()
    with open(data_path, 'r', encoding='utf-8') as seg_file:
        lines = seg_file.readlines()
    with open(dict_path, 'w', encoding='utf-8') as dic_file:
        for line in lines:
            for word in line.split():
                if '/m' in word:
                    continue
                if word[0] == '[':
                    word = word[1:word.index('/')]
                else:
                    word = word[0:word.index('/')]
                word_set.add(word)
                maxlen = len(word) if len(word) > maxlen else maxlen
        word_list = list(word_set)
        word_list.sort()
        dic_file.write('\n'.join(word_list))
    return maxlen, word_list

def create_doc(all = 'data/hmm/all.txt', hmm_train = 'data/hmm/train.txt', hmm_test = 'data/hmm/test.txt'):
    count = 0
    with open(all, 'r', encoding='utf-8') as seg_file:
        lines = seg_file.readlines()  # 读取训练文本
    train_file = open(hmm_train, 'w', encoding='utf-8')
    test_file = open(hmm_test, 'w', encoding='utf-8')
    for line in lines:
        if line == '\n':
            continue
        else:
            if count % 10 == 0:
                test_file.write(line)
                count += 1
            else:
                train_file.write(line)
                count += 1

def create_sent(hmm_test = 'data/hmm/test.txt', hmm_sent = 'data/hmm/test_sent.txt'):
    with open(hmm_test, 'r', encoding='utf-8') as seg_file:
        lines = seg_file.readlines()  # 读取训练文本
    test_file = open(hmm_sent, 'w', encoding='utf-8')
    for line in lines:
        sentline = ''
        for word in line.split():
            if word[0] == '[':
                word = word[1:word.index('/')]
            else:
                word = word[0:word.index('/')]
            sentline = sentline + word
        test_file.write(sentline + '\n')