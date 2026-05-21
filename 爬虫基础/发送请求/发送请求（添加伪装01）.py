import requests
from fake_useragent import UserAgent #可以使用 fake-useragent 库随机生成不同浏览器的 UA
url = "https://www.bequke.com/"#这里设置一个，url对象，方便后续使用
ua = UserAgent() #设置ua对象
headers = {'User-Agent': ua.random}  # 每次随机一个 UA
response = requests.get(url= url,headers=headers)
# print(response.status_code) #测试代码
# print(response.headers)

