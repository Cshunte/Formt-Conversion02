import os
del_dir="F:/20220601_Dataset/person/person3.0/YOLO_txt"           #要处理文件的目录
filelist=os.listdir(del_dir)       #提取文件名存放在filelist中
for file in filelist:               #遍历文件名
    del_file=del_dir+'\\'+file       #程序和文件不在同一目录下要用绝对路径
    lines=[a for a in open(del_file,"r") if((a.find("ball")==-1) )]
    # and (a.find("5678")==-1)  and  (a.find("abcd")==-1))]       #注意这里要用and
#把文件中含有1234、5678和abcd的行删掉
    fd=open(del_file,"w")
    fd.writelines(lines)
    fd.close