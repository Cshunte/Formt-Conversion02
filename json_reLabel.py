# University: Guangzhou University
# College: School of Electronic and Communication Engineering
# Editor: 李啟津
import os
import json
from ipdb import set_trace

json_dir = 'C:/Users/Czhannb/Desktop/JSON'
json_files = os.listdir(json_dir)


json_dict = {}
# 需要修改的新名称
new_name = 'person'

for json_file in json_files:

    jsonfile = json_dir + '/' + json_file
    # 读单个json文件
    with open(jsonfile, 'r', encoding='utf-8') as jf:

        info = json.load(jf)
        # print(type(info))
        # 找到位置进行修改
        '''
        ###################  已修改，加入if函数，判断'label'是否为球，不为球才往下执行命令   ####################
        ###################  已修改，加入if函数，判断'label'是否为球，不为球才往下执行命令   ####################
        ###################  已修改，加入if函数，判断'label'是否为球，不为球才往下执行命令   ####################
        #####################已修改，加入if函数，判断'label'是否为球，不为球才往下执行命令#######################
        ###################  已修改，加入if函数，判断'label'是否为球，不为球才往下执行命令   ####################
        ###################  已修改，加入if函数，判断'label'是否为球，不为球才往下执行命令   ####################
        ###################  已修改，加入if函数，判断'label'是否为球，不为球才往下执行命令   ####################
        '''



        for i, label in enumerate(info['shapes']):
            # if info['shapes'][i]['label'] != 'ball':
            info['shapes'][i]['label'] = new_name

        # 使用新字典替换修改后的字典
        json_dict = info
        print(json_dict)
        # set_trace()
    # 将替换后的内容写入原文件
    with open(jsonfile, 'w') as new_jf:
        json.dump(json_dict, new_jf)

print('change name over!')