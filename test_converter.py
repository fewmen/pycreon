import inspect
import os, io

RES_FILE_PATH = 'C:\\eBest\\xingAPI\\Res\\'
FILE_LIST = os.listdir(RES_FILE_PATH)
field = io.open("fields.txt", mode="a", encoding="utf-8")

filename = "CDPCQ04700.res"
# for filename in FILE_LIST:
with open(RES_FILE_PATH+filename) as fp:
    InBlock_begin_idx = 0
    InBlock_end_idx = 0
    OutBlock_begin_idx = []
    OutBlock_end_idx = []
    for i, line in enumerate(fp):
        splited_word = line.replace(';', '').split(',')
        cnt = len(splited_word)
        if cnt >= 3 and cnt < 5:
            if splited_word.find("InBlock") != -1:
                    InBlock_begin_idx = i+1
            elif splited_word.find("output") != -1:
                    OutBlock_begin_idx.append(i+1)
                    InBlock_end_idx = i - 1
        elif cnt == 1:
            if splited_word[0].strip().replace('\t','') == "end" \
            and i > InBlock_end_idx \
            and InBlock_begin_idx < InBlock_end_idx:
                OutBlock_end_idx.append(i)
            else:
                continue
fp.close

with open(RES_FILE_PATH+filename) as fp:
    file_lines = enumerate(fp)
    print(file_lines)
    
    fp.close()
field.close()

