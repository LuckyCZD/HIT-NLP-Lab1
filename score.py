import re
#计算list各元素的和
def sum_list(l):
    len_l=len(l)
    count=0
    for i in range(len_l):
        count=count+l[i]
    return count

def calculate_score(calculate_path,human_path,score_path):
    # 首先计算正确的分词数
    calculate_file = open(calculate_path, 'r', encoding='utf-8')
    human_file = open(human_path, 'r', encoding='utf-8')

    numcs = 0 # 机器分词数
    numhuman = 0 # 正确分词数
    # 具体的分词结果
    resultcs = []
    resulthuman = []
    #机器分词结果
    for line in calculate_file:
        if line=='\n' or line == '/ \n':
            continue
        l = line.split('/ ')
        if '\n' in l:
            l.pop(l.index('\n'))
        resultcs.append(l)
        numcs +=len(l)
    print(numcs)

    #人工分词结果
    for line in human_file:
        #去除空行
        if line=='\n':
            continue
        #去除空格和标记的词性
        l = re.sub(r'\s*|[a-zA-Z]*|\[|\]','',line)
        #去除换行符
        if l.count('\n')>0:
            l.remove('\n')
        #分词
        l = l.split('/')
        l.pop()#最后有一个额外的/作为结尾
        resulthuman.append(l)
        numhuman +=len(l)
    print(numhuman)

    count = 0
    for i in range(len(resultcs)):
        # 记录每句分词的位置
        temp1=[]
        start = 0
        for j in range(len(resultcs[i])):
            end = start + len(resultcs[i][j])
            temp1.append((start,end))
            start = end

        temp2 = []
        start = 0
        for j in range(len(resulthuman[i])):
            end = start + len(resulthuman[i][j])
            temp2.append((start, end))
            start = end

        temp_set = set(temp1) & set(temp2)
        # print(len(temp_set))
        count = count + len(temp_set)
    print(count)
    precision = count / numcs
    recall = count / numhuman
    F = 2 * precision * recall / (precision + recall)
    print(precision, recall, F)
    # 0.9455949553453616 0.9547290765173354
    # 0.9488889505271808 0.959495359491503 0.9541626808854644