# 解决execjs乱码问题
import subprocess
from functools import partial
subprocess.Popen=partial(subprocess.Popen,encoding='utf-8')


import execjs
# with open('测试.js', 'r') as f:#先读取文件
#     file = f.read()
# s=execjs.compile(file).call('solve')#转换并调用solve函数
# print(s['name'])
s="""
    {
        name:"acex",
        age:3,
        gender:"male"
    }
"""
#调用execjs跑一下代码，转换类型方便提取数据
d=execjs.eval(s)
print(d['name'])
print(type(d))#转换成字典了