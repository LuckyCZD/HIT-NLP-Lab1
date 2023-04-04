import re
import numpy as np
from math import log

States=['B','M','E','S']    #开始，中间，结尾，单字
A = {}    #状态转移概率矩阵，从某个状态转移到另一个状态的概率，比如B到S，概率为0.1
B = {}    #发射概率矩阵
Pi = {}   #初始状态分布，初始化概率,比如一开始是B的概率为0.5
MIN = -3.14e+100
array_E = {}    #测试集存在的字符，但在训练集中不存在，发射概率矩阵
word_set = set()    #训练数据集中所有字的集合
State_Count = {}  # 保存状态出现次数
line_num = 0    #训练集语句数量

class TRAIN:
    @staticmethod  # 初始化待统计的参数λ并配置所有的词
    def init():
        global line_num, word_set
        line_num = 0
        word_set = set()
        for state in States:
            Pi[state] = 0.0
            State_Count[state] = 0
            B[state], A[state] = {}, {}
            for state_1 in States:
                A[state][state_1] = 0.0  # 由state转换为state_1概率初始化

    @staticmethod  # 将训练得到的参数写入文本文件中，便于以后分析
    def write_prob_array_to_file(pi_path='data/hmm/pi.txt', a_path='data/hmm/a.txt',
                     b_path='data/hmm/b.txt'):
        pi_file = open(pi_path, 'w', encoding='utf-8')
        a_file = open(a_path, 'w', encoding='utf-8')
        b_file = open(b_path, 'w', encoding='utf-8')
        for state in States:  # 将参数写入文本文件中
            pi_file.write(state + ' ' + str(Pi[state]) + '\n')
            a_file.write(state + '\n')
            b_file.write(state + '\n')
            for state_1 in States:
                a_file.write(' ' + state_1 + ' ' + str(A[state][state_1]) + '\n')
            for word in B[state].keys():
                b_file.write(' ' + word + ' ' + str(B[state][word]) + '\n')

    @staticmethod   # 标记一句话的tag
    def tag(wordline):
        line_word = []
        line_wordtag = []
        if wordline == '\n':
            return line_word, line_wordtag
        global line_num, count_dic
        line_num = line_num + 1
        for word in wordline.split():
            word = word[1 if word[0] == '[' else 0:word.index('/')]  # 取出一个词
            line_word.extend(list(word))  # 将这一个词的每个字加到该行的字列表中
            word_set.add(word)  # 将该词保存在Word_Dic中
            if len(word) == 1:
                line_wordtag.append('S')
                State_Count['S'] = State_Count['S'] + 1
            elif len(word) == 2:
                line_wordtag.append('B')
                line_wordtag.append('E')
                State_Count['B'] = State_Count['B'] + 1
                State_Count['E'] = State_Count['E'] + 1
            else:
                line_wordtag.append('B')
                for j in range(len(word) - 2):
                    line_wordtag.append('M')
                    State_Count['M'] = State_Count['M'] + 1
                line_wordtag.append('E')
                State_Count['B'] = State_Count['B'] + 1
                State_Count['E'] = State_Count['E'] + 1
        # print(line_word)
        # print(line_wordtag)
        return line_word, line_wordtag

    @staticmethod
    def tag_txt(train_path):
        TRAIN.init()
        with open(train_path, 'r', encoding='utf-8') as txt_file:
            lines = txt_file.readlines()
        for line in lines:
            if line == '\n':
                continue
            line=line[22:] #去除日期
            line_word, line_tag = TRAIN.tag(line)  # 得到一行标注
            Pi[line_tag[0]] = Pi.get(line_tag[0], 0) + 1
            for i in range(len(line_tag)):
                State_Count[line_tag[i]] += 1  # 计算状态总出现次数
                B[line_tag[i]][line_word[i]] = B[line_tag[i]].get(line_word[i], 0) + 1
                if i > 0:
                    A[line_tag[i - 1]][line_tag[i]] += 1  # 转移概率变化
        for state in States:
            Pi[state] = MIN if Pi[state] == 0 else log(Pi[state] / line_num)
            for state_1 in States:  # 计算状态转移概率
                A[state][state_1] = MIN if A[state][state_1] == 0 else log(
                    A[state][state_1] / State_Count[state])
            for word in B[state].keys():  # 计算发射概率
                B[state][word] = log(B[state][word] / State_Count[state])
        TRAIN.write_prob_array_to_file()

class HMM:
    @staticmethod
    def viterbi(line):
        A1 = np.array([[A['B']['B'], A['B']['M'], A['B']['E'], A['B']['S']],
                       [A['M']['B'], A['M']['M'], A['M']['E'], A['M']['S']],
                       [A['E']['B'], A['E']['M'], A['E']['E'], A['E']['S']],
                       [A['S']['B'], A['S']['M'], A['S']['E'], A['S']['S']]])
        pi = np.array([Pi['B'], Pi['M'], Pi['E'], Pi['S']])
        line_word = []
        line_word.extend(list(line))
        # 初始化 维比特矩阵viterbi 它的维度为[状态数, 序列长度]
        # 其中viterbi[i, j]表示标注序列的第j个标注为i的所有单个序列(i_1, i_2, ..i_j)出现的概率最大值
        seq_len = len(line)
        viterbi = np.zeros(shape=(4, seq_len), dtype=float)
        # backpointer是跟viterbi一样大小的矩阵
        # backpointer[i, j]存储的是标注序列的第j个标注为i时，第j-1个标注的id
        # 等解码的时候，我们用backpointer进行回溯，以求出最优路径
        backpointer = np.zeros(shape=(4, seq_len), dtype=float)
        # 如果字不再字典里，则假设状态的概率分布是均匀的
        b = np.ones(shape=4, dtype=float)
        if line_word[0] in word_set:
            for index, state in enumerate(States):
                b[index] = B[state].get(line_word[0], MIN)
        viterbi[:, 0] = pi.T + b.T
        backpointer[:, 0] = -1
        # 递推公式：viterbi[tag_id, step] = max(viterbi[:, step-1]* A.t()[tag_id] * Bt[word])
        for step in range(1, seq_len):
            word = line_word[step]
            # 处理字不在字典中的情况
            if word not in word_set:
                bt = np.log(np.ones(shape=4, dtype=float) / 4)
            else:
                bt = np.log(np.ones(shape=4, dtype=float) / 4)  # 否则从观测概率矩阵中取bt
                for index, state in enumerate(States):
                    bt[index] = B[state].get(word, MIN)

            for index, state in enumerate(States):
                max_prob = np.max(a=viterbi[:, step - 1] + A1[:, index], axis=0)
                max_id = np.argmax(a=viterbi[:, step - 1] + A1[:, index], axis=0)
                viterbi[index, step] = max_prob + bt[index]
                backpointer[index, step] = max_id
        # 终止， t=seq_len 即 viterbi[:, seq_len]中的最大概率，就是最优路径的概率
        best_path_pointer = np.argmax(a=viterbi[:, seq_len - 1], axis=0)
        # 回溯，求最优路径
        best_path_pointer = int(best_path_pointer)
        best_path = [best_path_pointer]
        for back_step in range(seq_len - 1, 0, -1):
            best_path_pointer = backpointer[best_path_pointer, back_step]
            best_path_pointer = int(best_path_pointer)
            best_path.append(best_path_pointer)
        best_path.reverse()
        path = []
        for state in best_path:
            if state == 0:
                path.append('B')
            if state == 1:
                path.append('M')
            if state == 2:
                path.append('E')
            if state == 3:
                path.append('S')
        # print(path)
        return path

    @staticmethod
    def hmm_word(word):
        if len(word) == 1:
            return word
        tag_list = HMM.viterbi(word)
        begin, next_index = 0, 0
        res_word = ''
        for idx, char in enumerate(word):
            tag = tag_list[idx]  # 取一个tag
            if tag == 'B':  # 表示开始
                begin = idx
            elif tag == 'E':  # 表示结束
                res_word += word[begin:idx + 1] + '/ '
                next_index = idx + 1
            elif tag == 'S':
                res_word += char + '/ '
                next_index = idx + 1
        if next_index < len(word):
            res_word += word[next_index:] + '/ '
        return res_word

    @staticmethod
    def hmm_line(line):
        word_list = line[:len(line) - 2].split('/ ')  # 得到所有的词语列表
        seg_line, to_seg_word = '', ''  # 储存连续的单字，用于进一步使用HMM进行未登录词识别
        for index in range(len(word_list)):
            if len(word_list[index]) == 1:

                if word_list[index] in word_set:  # 该单字是词典中的词
                    if to_seg_word:  # 判断是否该词前面为单字
                        seg_line += HMM.hmm_word(to_seg_word)
                        to_seg_word = ''
                    seg_line += word_list[index] + '/ '
                else:
                    to_seg_word += word_list[index]
                    if index + 1 == len(word_list):
                        seg_line += HMM.hmm_word(to_seg_word)
            else:  # 遇到非单字情况
                if to_seg_word:  # 判断是否该词前面为单字
                    seg_line += HMM.hmm_word(to_seg_word)
                    to_seg_word = ''
                seg_line += word_list[index] + '/ '
        # print(seg_line)
        return seg_line

