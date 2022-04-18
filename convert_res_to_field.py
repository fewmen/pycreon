import inspect
import os, io

RES_FILE_PATH = 'C:\\eBest\\xingAPI\\Res\\'
FILE_LIST = os.listdir(RES_FILE_PATH)
field = io.open("fields.txt", mode="a", encoding="utf-8")

for filename in FILE_LIST:
    with open(RES_FILE_PATH+filename) as fp:
        InBlock_begin_idx = 0
        InBlock_end_idx = 0
        OutBlock_begin_idx = []
        OutBlock_end_idx = []
        for i, line in enumerate(fp):
            splited_word = line.replace(';', '').split(',')
            cnt = len(splited_word)
            if cnt >= 3 and cnt < 5:
                for w in splited_word:
                    if w.find("InBlock") != -1:
                        InBlock_begin_idx = i+1
                    elif w.find("output") != -1:
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
        cidx = 0
        for i, line in enumerate(fp):
            splited_word = line.replace(';','').split(',')
            cnt = len(splited_word)
            if cnt > 4:
                if cnt == 6 and i == 1:
                    field.write(filename.split('.')[0])
                    field.write(" = {\n")
                
                elif cnt == 5 and i == 1:
                    field.write(filename.split('.')[0])
                    field.write(" = {\n")
                
                elif cnt == 5 and i != 1:
                    if splited_word[1].find("shcode") != -1 or splited_word[1].find("upcode") != -1 or splited_word[1].find("futcode") != -1 \
                        or splited_word[1].find("optcode") != -1:
                        continue
                    field.write('        "')
                    field.write(splited_word[1].strip().replace("\t", ""))
                    field.write('":"')
                    field.write(splited_word[0].strip().replace("\t", ""))
                    field.write('"')
                    field.write(',\n')

            elif cnt >= 3 and cnt < 5:
                for w in splited_word:
                    if w.find("InBlock") != -1:
                        continue

                    elif w.find("OutBlock") != -1:
                        field.write('    "')
                        field.write(filename.split('.')[0])
                        field.write(w.strip().replace("\t", ""))
                        field.write('":{\n')
            
            elif cnt == 1:
                if len(OutBlock_end_idx) == 1 and OutBlock_end_idx[cidx] == i \
                    and splited_word[0].find("end") != -1:
                    field.write("    }\n")
                elif len(OutBlock_end_idx) > 1 and OutBlock_end_idx[cidx] == i \
                    and splited_word[0].find("end") != -1:
                    if OutBlock_end_idx[-1] != i:
                        cidx += 1
                        field.write("    },\n")
                elif splited_word[0].find("END_DATA_MAP") != -1:
                        field.write("}\n\n")
                else:
                    continue

        cidx = 0
        fp.close()
field.close()

