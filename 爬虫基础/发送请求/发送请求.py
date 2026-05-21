import requests #引入resquest库
response = requests.get('https://www.bequke.com/') #设置响应对象并用get方法请求
print(response.status_code)
# print(response.text)#获取响应文本-输出HTML源码
print(response.headers)#打印请求头
print(response.content)#获取响应内容-一般用于处理图片与二进制数据
print(response.encoding)#获取编码信息，这个在保存数据中会很有用，可令response.encoding=f"{response.encoding}",然后再跟，print(response.text)就没有乱码了
