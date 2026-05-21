import requests
import random #引入随机
from fake_useragent import UserAgent #可以使用 fake-useragent 库随机生成不同浏览器的 UA
url = "https://www.bequke.com/"#这里设置一个，url对象，方便后续使用
ua = UserAgent() #设置ua对象
# 创建 Session 对象
s = requests.Session()
headers = {'User-Agent': ua.random}  # 每次随机一个 UA
#设置代理池
proxies_list=[
'8.209.249.96:8181'
'39.102.210.176:8888',
'123.54.197.50:22819',
'123.54.197.19:23595',
'8.215.12.103:8888',
'123.54.197.52:21267',
'47.92.143.92:82',
'120.26.123.95:8010',
'8.148.22.214:9098',
'117.159.239.49:22222',
'47.105.122.72:3129',
'47.99.112.148:80',
'39.104.62.128:5000',
'58.220.95.12:11032',
'101.71.143.237:8092']
#for循环
success_flag = False  # 标记是否找到可用代理
for proxy in proxies_list:
    try:
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
        # 设置随机 User-Agent 并更新到 session 的 headers 中
        s.headers.update(headers)
        ip = requests.get('http://httpbin.io/ip', proxies=proxies).text
        # print(f"当前出口 IP: {ip}")
        response = s.get(url= url,headers=headers,proxies=proxies)#通过Session对象发送get请求
        print(response.status_code) #测试代码
        print(response.text)
        # 标记为成功，并跳出循环
        success_flag = True
        break  # 关键：跳出for循环，停止后续代理测试
    except Exception as e:
        print(e)

