import inspect
import os, io
from re import I

RES_FILE_PATH = 'C:\\eBest\\xingAPI\\Res\\'
FILE_LIST = os.listdir(RES_FILE_PATH)
field = io.open("fields.txt", mode="a", encoding="utf-8")

for filename in FILE_LIST:
    with open(RES_FILE_PATH+filename) as fp:
        InBlock_begin_idx = 0
        InBlock_end_idx = 0
        for i, line in enumerate(fp):
            splited_word = line.replace(';', '').split(',')
            cnt = len(splited_word)
            if cnt >= 3 and cnt < 5:
                if splited_word[0].find("InBlock") != -1:
                    InBlock_begin_idx = i+1
                elif splited_word[0].find("OutBlock") != -1:
                    InBlock_end_idx = i - 1
                    break
    fp.close

    with open(RES_FILE_PATH+filename) as fp:
        for i, line in enumerate(fp):
            # print("filename = {}\nInBlockBeginIdx = {}\n InBlockEndIdx = {}\n\n".format(filename,InBlock_begin_idx, InBlock_end_idx))
            splited_word = line.replace(';','').split(',')
            cnt = len(splited_word)
            if i == 1:
                    field.write(splited_word[2])
                    field.write(" = {\n")
                
            elif cnt > 4 and InBlock_end_idx >= i:
                continue

            elif cnt >= 5 and InBlock_end_idx < i:
                # if splited_word[1].find("shcode") != -1 or splited_word[1].find("upcode") != -1 or splited_word[1].find("futcode") != -1 \
                #     or splited_word[1].find("optcode") != -1:
                #     continue
                field.write('        "')
                field.write(splited_word[1].strip())
                field.write('":"')
                field.write(splited_word[0].strip())
                field.write('"')
                field.write(',\n')

            elif cnt >= 3 and InBlock_end_idx < i:
                if splited_word[0].find("OutBlock") != -1:
                    field.write('    "')
                    field.write(splited_word[0].strip())
                    field.write('":{\n')
        
            elif cnt == 1 and InBlock_end_idx < i:
                if splited_word[0].find("begin") != -1:
                    continue
                if splited_word[0].find("end") != -1:
                    field.write("    }")
                elif splited_word[0].find("END_DATA_MAP") != -1:
                    field.write("\n}\n\n")
                    
                else:
                    continue
        fp.close()
field.close()

