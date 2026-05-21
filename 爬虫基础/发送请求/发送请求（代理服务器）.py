import requests
from fake_useragent import UserAgent #可以使用 fake-useragent 库随机生成不同浏览器的 UA
url = "https://www.bequke.com/"#这里设置一个，url对象，方便后续使用
proxies = {
    'http': 'http://8.130.74.114:9080'
    'https://8.130.74.114:9080',
    # 'http': 'socks5://8.222.165.198:1100'
}
ua = UserAgent() #设置ua对象
# 创建 Session 对象
s = requests.Session()
headers = {'User-Agent': ua.random}  # 每次随机一个 UA
# 设置随机 User-Agent 并更新到 session 的 headers 中
s.headers.update(headers)
response = s.get(url= url,headers=headers,proxies=proxies)#通过Session对象发送get请求
print(response.status_code) #测试代码
# print(response.elapsed) #响应时间
ip = requests.get('https://httpbin.io/ip', proxies=proxies).text
print(f"当前出口 IP: {ip}")