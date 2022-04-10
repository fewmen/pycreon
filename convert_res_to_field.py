import os

RES_FILE_PATH = 'C:\\eBest\\xingAPI\\Res\\'

FILE_LIST = os.listdir(RES_FILE_PATH)

for filename in FILE_LIST:
    num_lines = sum(1 for line in open(RES_FILE_PATH+filename, "r"))
    print(f"filename : {filename}, line numbers {num_lines}")
    


