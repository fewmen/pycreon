import os, io

RES_FILE_PATH = 'C:\\eBest\\xingAPI\\Res\\'
FILE_LIST = os.listdir(RES_FILE_PATH)
field = io.open("fields.txt", mode="a", encoding="utf-8")


# open_file = io.open(RES_FILE_PATH+FILE_LIST[0], mode="r", encoding="cp949")
with open(RES_FILE_PATH+FILE_LIST[0]) as fp:
    for i, line in enumerate(fp):
        begin_idx = 0
        end_idx = 0
        line = line.replace(';', '')
        splited_word = line.split(',')
        cnt = len(splited_word)
        if cnt == 6:
            print('6')
            field.write(splited_word[2].strip())
            field.write(" = {\n")
        elif cnt == 3:
            print('3')

            if "OutBlock" in splited_word:
                print("OutBlcok in 3")
                field.write('    "')
                field.write(FILE_LIST[0].split('.')+splited_word[0].strip().replace("\t", ""))
                field.write('":{\n')
        elif cnt == 5:
            print('5')

            field.write('        "')
            field.write(splited_word[1].strip().replace("\t", ""))
            field.write('":"')
            field.write(splited_word[0].strip().replace("\t", ""))
            field.write('"')
            field.write(',\n')
        elif cnt == 1:
            print('1')

            if "END_DATA_MAP" in splited_word:
                print("END_DATA_MAP in 1")
                field.write('}')
        
field.close()
fp.close()
