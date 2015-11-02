#-*-coding:utf-8-*-
import os
import os.path

#删除函数实现
def deletefunction():
    for root, dirnames, files in os.walk("/home/vinzor/project2/data/submit/"):
        for name in files:
            pathName = os.path.splitext(os.path.join(root, name))
            if (pathName[1] == '.txt' or pathName[1] == ''):
                os.remove(os.path.join(root, name))
                print(os.path.join(root, name))

#输入要删除文件的目录，删除后缀名为"txt"或没有后缀名的文件
print "本程序只支持删除制定目录下后缀名为'txt'或没有后缀名的文件"

deletefunction()

