from math import log
import re
import BMM
import BMM_optimized
Train_File='data/hmm/all.txt'
dict_path='data/hmm/dic(2).txt'

bmm_dict_path = 'data/dic.txt'
word_dict = {}  # 保存 词 上一个词 两个词对出现的频率
word_freg = {'BOS':0}  # 保存 词 词频,先把头储存进去
wordnum = 0
pattern = r'(\d-*)+$'

class createDict:
    @ staticmethod
    def gen_bi_dict(train=Train_File):
        global word_freg, wordnum, word_dict
        with open(train,'r',encoding='utf-8')as f:
            lines=f.readlines()
        for line in lines:
            if line=='\n':
                continue
            line=line[23:len(line)-1]
            #划分词
            seg_line=line.split()
            wordnum += len(seg_line)
            seg_line.append('EOS/ ')
            seg_line.insert(0, 'BOS')
            for idx,word in enumerate(seg_line):
                if word=='BOS':
                    word_freg[word] += 1
                    continue #第一个词不计入二元词典
                else:
                    word=word[1 if word[0]=='[' else 0:word.index('/')]
                    seg_line[idx]=word
                    #加入词频表
                    if word in word_freg:
                        word_freg[word] += 1
                    else:
                        word_freg[word] = 1
                    #加入二元词频表
                    if word not in word_dict.keys():
                        word_dict[word] = {}
                    if seg_line[idx-1] not in word_dict[word]:
                        word_dict[word][seg_line[idx-1]]=0
                    word_dict[word][seg_line[idx-1]] += 1
        word_freg = {k: word_freg[k] for k in sorted(word_freg.keys())}
        word_dict = {k: word_dict[k] for k in sorted(word_dict.keys())}
        with open(dict_path, 'w', encoding='utf-8') as f:
            for word in word_dict:
                for pre in word_dict[word]:
                    f.write(word + ' ' + pre + ' ' + str(word_dict[word][pre]) + '\n')
        # print(wordnum)
        # print(word_freg)

    @staticmethod
    def probaliy(pre_word, word):
        pre_num = word_freg.get(pre_word, 0)  # 前词词频
        pairnum = word_dict.get(word, {}).get(pre_word, 0)  # 词对出现的频率
        p = log(pairnum + 1) - log(pre_num + wordnum)
        return p

    @staticmethod
    def get_DAG(sentence):
        DAG = {0:[3]}  # 无环有向图
        N = len(sentence)
        for k in range(3, N):
            templist = []
            i = k
            frag = sentence[k]
            while i<N:
                if frag in word_freg:
                    templist.append(i)
                i += 1
                frag = sentence[k:i+1]
            if not templist:
                templist.append(k)
            DAG[k] = templist
        # print(DAG)
        return DAG

    @staticmethod
    def get_dag(sentence):
        DAG = {'BOS': {}}  # 无环有向图
        N = len(sentence) - 3
        for k in range(3, N):
            templist = {}
            i = k
            frag = sentence[k]
            while i < N:
                if frag in word_freg:
                    templist[i] = createDict.probaliy()
                i += 1
                frag = sentence[k:i + 1]
            if not templist:
                templist.append(k)
            DAG[k] = templist
        return DAG

    @staticmethod
    def calc_line(line, dag):
        n = len(line) - 3
        start = 3
        pre_graph = {'BOS': {}}  # 关键字为前词，值为对应的词和对数概率
        word_graph = {}  # 每个词节点存有上一个相连词的词图
        for x in dag[3]:  # 初始化前词为BOS的情况
            pre_graph['BOS'][(3, x + 1)] = createDict.probaliy('BOS', line[3:x + 1])
        while start < n:  # 对每一个字可能的词生成下一个词的词典
            for idx in dag[start]:  # 遍历dag[start]中的每一个结束节点
                pre_word = line[start:idx + 1]
                temp = {}
                for next_end in dag[idx + 1]:
                    last_word = line[idx + 1:next_end + 1]
                    if line[idx + 1:next_end + 3] == 'EOS':
                        temp['EOS'] = createDict.probaliy(pre_word, 'EOS')
                    else:
                        temp[(idx + 1, next_end + 1)] = createDict.probaliy(pre_word, last_word)
                pre_graph[(start, idx + 1)] = temp  # 每一个以start开始的词都建立一个关于下一个词的词典
            start += 1
        pre_words = list(pre_graph.keys())  # 表示所有的前面的一个词
        for pre_word in pre_words:  # word_graph表示关键字对应的值为关键字的前词列表
            for word in pre_graph[pre_word].keys():
                word_graph[word] = word_graph.get(word, list())
                word_graph[word].append(pre_word)
        pre_words.append('EOS')
        return pre_graph, word_graph

def dag_sp(W, s, t, d):
    if s == t:
        return 0
    if s not in d:
        d[s] = -65536
        for v in W[s]:
            if W[s][v] + dag_sp(W, v, t, d) > d[s]:
                d[s] = W[s][v] + dag_sp(W, v, t, d)
    return d[s]

def bigram(line, distance, pre_graph, word_graph):
    route = []
    pre_graph['EOS'] = 0
    seg_line = ''
    position = 'EOS'
    start = 0
    i = 0
    count = 0
    minn = 0.001
    while True:
        if position == 'BOS':
            break
        for index, w in enumerate(word_graph[position]) :
            count += 1
            if count > len(word_graph[position]):
                minn = 2 * i
            if len(word_graph[position]) == 1:
                route.append(w)
                start = distance[w]
                position = w
                i = i + 2
                break
            if w in word_graph.keys():
                if distance[w] - start - pre_graph[w][position] <= minn:
                    route.append(w)
                    start = distance[w]
                    position = w
                    i = i + 2
                    break
                if index == len(word_graph[position]) - 1:
                    route.append(w)
                    start = distance[w]
                    position = w
                    i = i + 2
                    break
    route.remove('BOS')
    #print(route)
    for tup in route:
        seg_line = line[tup[0]:tup[1]] + '/ ' + seg_line
    #print(seg_line)
    return seg_line

def check_digital(check_str):
    if len(check_str) <=19 and re.match(pattern, check_str) is not None:
        return True
    return False

def bigram_seg(sent_path, result_path):
    createDict.gen_bi_dict()
    BMM.read_dict(bmm_dict_path)
    with open(sent_path, 'r', encoding='utf-8') as sent_file:
        lines = sent_file.readlines()
    with open(result_path, 'w', encoding='utf-8') as seg_file:
        for line in lines:
            if line == '\n':
                continue
            j = 0
            for index, word in enumerate(line):
                if ('0' <= line[index] <= '9') or line[index] == '-':
                    continue
                else:
                    j = index
                    break
            number = line[0:j]
            i = len(line) - 1
            line_list = re.split(r"(。)", line[j:i])
            seg_line = ''
            for index, single_line in enumerate(line_list):
                if len(line_list) == 1:
                    temp_line = 'BOS' + single_line + 'EOS'
                    dag = createDict.get_DAG(temp_line)
                    tmp_pre_graph, tmp_word_graph = createDict.calc_line(temp_line, dag)
                    # print(tmp_pre_graph)
                    d = {}
                    dag_sp(tmp_pre_graph, 'BOS', 'EOS', d)
                    try:
                        seg_line = seg_line + bigram(temp_line, d, tmp_pre_graph, tmp_word_graph)
                    except KeyError:
                        seg_line = seg_line + BMM_optimized.BMM_line(temp_line[3:], 15)
                    break
                else:
                    if len(single_line) == 1:
                        continue
                    if index < len(line_list) - 1:
                        temp_line = 'BOS' + single_line + line_list[index + 1] + 'EOS'
                        dag = createDict.get_DAG(temp_line)
                        tmp_pre_graph, tmp_word_graph = createDict.calc_line(temp_line, dag)
                        # print(tmp_pre_graph)
                        d = {}
                        dag_sp(tmp_pre_graph, 'BOS', 'EOS', d)
                        try:
                            seg_line = seg_line + bigram(temp_line, d, tmp_pre_graph, tmp_word_graph)
                        except KeyError:
                            seg_line = seg_line + BMM_optimized.BMM_line(temp_line[3:], 15)
            seg_file.write(number + '/ ' + seg_line + '\n')
            print(number + '/ ' + seg_line)




