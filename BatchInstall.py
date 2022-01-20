import os
'''
需要的第三方库在requires.txt里
该脚本可以重复使用
只需在requies.txt里的增加你想安装的第三方库，每行只能有一个库名
'''
fo=open("requires.txt","r",encoding="utf-8")
libs=fo.readlines()
fo.close

#国内镜像库,可修改成其他镜像库
url = "https://pypi.tuna.tsinghua.edu.cn/simple"#清华大学镜像库

try:
    for lib in libs:
        os.system("pip install "+lib+"-i"+url)
    print("Successful")        
except:
    print("Failed Somehow")
