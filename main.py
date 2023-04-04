import numpy as np
from dict import *
import time


def test_create_dict():
    max_len, word_list = create_dict(all_path, dict_path)
    # print(max_len)
    # max_len = 26

def test_FMM():
    from FMM import read_dict, FMM
    read_dict(dict_path)
    time_start = time.time()
    FMM(sent_path, FMM_path, 26)
    time_end = time.time()
    time_c = time_end - time_start
    print('time cost', time_c, 's')  # 41.22s

def test_BMM():
    from BMM import read_dict, BMM
    read_dict(dict_path)
    BMM(sent_path, BMM_path, 26)

def test_score():
    from score import calculate_score
    # Score(test_fmm_path, test_seg_path, test_score_path)
    calculate_score(calculate_path = 'data/seg_out_bi_hmm.txt', human_path = 'data/hmm/test.txt', score_path = 'data/test_score.txt')

def test_FMM_optimize():
    from FMM_optimize import read_dict, FMM
    read_dict(dict_path)
    time_start = time.time()
    FMM(sent_path, FMM_path)
    time_end = time.time()
    time_c = time_end - time_start
    print('time cost', time_c, 's')  # 22.00s  Trie树

def test_BMM_optimize():
    from BMM_optimized import read_dict, BMM
    from hmm import TRAIN, HMM
    read_dict(dict_path)
    TRAIN.tag_txt(hmm_train_path)
    BMM(hmm_sent_path, BMM_path, 26)

def test_Bigram():
    '''
    测试二元文法分词
    '''
    from Bigram import bigram_seg
    bigram_seg(hmm_sent_path, result_path)

def test_HMM():
    from hmm import TRAIN, HMM
    '''可以输入被切分成单字的未登录词，格式同199801_sent'''
    line3 = "唏/ 嘘/ ，/ 耄/ 耋/ "
    TRAIN.tag_txt(hmm_train_path)
    new_line = HMM.hmm_line(line3)
    print(new_line)

def test_Bigram_and_HMM():
    from hmm import TRAIN
    from Bigram_and_HMM import bigram_seg
    TRAIN.tag_txt(all_path)
    bigram_seg(hmm_sent_path, result_path_2)

if __name__ == '__main__':
    '''文件均采用utf-8编码'''
    '''划分训练集和测试集'''
    # create_doc()
    '''生成词典'''
    # test_create_dict()
    '''正反向最大匹配分词及速度优化'''
    # test_FMM()
    # test_BMM()
    # test_FMM_optimize()
    # test_BMM_optimize()
    '''评价程序'''
    # test_score()
    # --------------------
    '''
    二元文法分词
    测试时更改输入文件路径即可
    '''
    test_Bigram()
    '''未登录词识别模块'''
    # test_HMM()
    '''实现未登录词识别的二元文法分词'''
    # test_Bigram_and_HMM()







