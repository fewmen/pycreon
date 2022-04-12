import os, io

RES_FILE_PATH = 'C:\\eBest\\xingAPI\\Res\\'
FILE_LIST = os.listdir(RES_FILE_PATH)
field = io.open("fields.txt", mode="a", encoding="utf-8")


for filename in FILE_LIST:
    open_file = io.open(RES_FILE_PATH+filename, mode="r", encoding="cp949")
    field.write(filename.split('.')[0])
    field.write(' = {\n')
    field.write('    "')
    field.write(filename.split('.')[0])
    field.write('OutBlock":{\n')
    field.write('        ')
    lines = open_file.readlines()
    for line in lines:
        cvt = line.split(',')
        if len(cvt) > 2 and len(cvt) <= 5:
            if cvt[1].strip() != str('입력') and cvt[1].strip() != str('출력') and \
                cvt[1].strip() != str('단축코드') and cvt[1].strip() != str('shcode'):
                field.write('"')
                field.write(cvt[1].strip())
                field.write('":"')
                field.write(cvt[0].strip())
                field.write('",\n')
                field.write('        ')
        else:
            continue
    field.write('}\n    }\n')
field.close()
open_file.close()
