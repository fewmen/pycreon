import os, io

def inblock_idx(RES_FILE_PATH, filename):
    with open(RES_FILE_PATH+filename) as fp1:
            InBlock_begin_idx = 0
            InBlock_end_idx = 0
            
            for i, line in enumerate(fp1):
                splited_word = line.replace(';', '').replace('\t','') \
                                .replace('\n', '').strip().split(',')
                cnt = len(splited_word)
                if cnt >= 3 and cnt < 5:
                    if splited_word[0].find("InBlock") != -1:
                        InBlock_begin_idx = i+1
                    elif splited_word[0].find("OutBlock") != -1:
                        InBlock_end_idx = i - 1
                        break
    fp1.close
    return InBlock_begin_idx, InBlock_end_idx


def outblock_idx(RES_FILE_PATH, filename):
        
    with open(RES_FILE_PATH+filename) as fp2:
            OutBlock_begin_idx = []
            OutBlock_end_idx = []
            for i, line in enumerate(fp2):
                splited_word = line.replace(';', '').replace('\t','') \
                                .replace('\n', '').strip().split(',')
                cnt = len(splited_word)
                if cnt == 1 and i > InBlock_end_idx:
                    if splited_word[0].find("begin") != -1:
                        OutBlock_begin_idx.append(i)
                    elif splited_word[0].find("end") != -1:
                        OutBlock_end_idx.append(i)
    fp2.close
    return OutBlock_begin_idx, OutBlock_end_idx

def write_line(fp, fname, InBlock_end_idx, OutBlock_begin_idx, OutBlock_end_idx, idx):
    field = io.open("fields.py", mode="a", encoding="utf-8")
    for i, line in enumerate(fp):
        splited_word = line.replace(';', '').replace('\t','') \
                            .replace('\n', '').strip().split(',')
        cnt = len(splited_word)
        if i == 1:
                field.write(fname)
                field.write(" = {\n")
        elif cnt > 4 and InBlock_end_idx >= i and i != 1:
            continue
        elif cnt >= 3 and cnt < 5 and InBlock_end_idx < i:
            if splited_word[0].find("OutBlock") != -1:
                field.write('\t"')
                field.write(splited_word[0])
                field.write('":{\n')
        elif cnt >= 5 and InBlock_end_idx < i:
            field.write('\t\t"')
            field.write(splited_word[1].strip())
            field.write('":"')
            field.write(splited_word[0].strip())
            field.write('",\n')
        elif OutBlock_begin_idx[idx] == i:
            continue
        elif OutBlock_end_idx[idx] == i:
            field.write("\t\t}")
            if OutBlock_end_idx[-1] == i:
                field.write("\n\t}\n\n")
                break
            elif len(OutBlock_end_idx) > 1 and OutBlock_end_idx[-1] != i:
                field.write(',\n')
                idx += 1
        else:
            continue
    field.close()
    return None

RES_FILE_PATH = 'C:\\eBest\\xingAPI\\Res\\'
FILE_LIST = os.listdir(RES_FILE_PATH)

for filename in FILE_LIST:
    fp = open(RES_FILE_PATH+filename)
    InBlock_begin_idx, InBlock_end_idx = inblock_idx(RES_FILE_PATH, filename)
    OutBlock_begin_idx, OutBlock_end_idx = outblock_idx(RES_FILE_PATH, filename)
    fidx = filename.find(".")
    fname = filename[:fidx]
    idx = 0
    write_line(fp, fname, InBlock_end_idx=InBlock_end_idx, OutBlock_begin_idx=OutBlock_begin_idx, OutBlock_end_idx=OutBlock_end_idx, idx=idx)
    fp.close()


    

