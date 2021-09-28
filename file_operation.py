def readfile(path):
    try:
        try:
            with open(path, mode='r', encoding='utf-8')as file:
                file_text, = eval(file.read())# 读取文件内容,并去解包元组，取第一位，
        except:#非元组会出错，出错后直接读取文件
            with open(path, mode='r', encoding='utf-8')as file:
                file_text = file.read()
        filename = path.split('/')[-1]  # 获取文件名
        return filename,file_text
    except Exception as e:
        print("读取文件失败，错误为：",e)
        return -1,-1

def savefile(path,file_text):
    try:
        with open(path, mode='w', encoding='utf-8')as file:
            file.write(str(((file_text),)))
    except Exception as e:
        print("保存文件失败，错误为：",e)
        return -1
    else:
        return 0

if __name__=='__main__':
    file_path = 'C:/Users/zhujianwei/Desktop/zjwmimaxue/数据加密器使用说明.txt'
    print(readfile(file_path))