import os

def bianli(dir_path):
    """
    get all file under the data dir
    """
    file_list = []
    for root,dirs,files in os.walk(dir_path):
        for file in files:
            if(".c" in file):
                file_list.append(os.path.join(root,file))
        for dir in dirs:
            bianli(dir)
    return file_list

if __name__=="__main__":
    c= bianli("data/real_dataset/gzip-1.3.5")
    print(c)
    print(len(c))