# 使用 Session 和 Cookies
# 如果需要登录或保持会话，用 requests.Session() 可以自动管理 cookies。
import requests
from fake_useragent import UserAgent #可以使用 fake-useragent 库随机生成不同浏览器的 UA
url = "https://www.bequke.com/"#这里设置一个，url对象，方便后续使用
ua = UserAgent() #设置ua对象
# 创建 Session 对象
s = requests.Session()
headers = {'User-Agent': ua.random}  # 每次随机一个 UA
# 设置随机 User-Agent 并更新到 session 的 headers 中
s.headers.update(headers)
# response1 = s.get(url= url,headers=headers)#通过Session对象发送get请求
# print(response.status_code) #测试代码
# print(response.headers)
# print(response1.cookies)
# 再次发送 GET，会自动携带之前设置的 Cookie
# response2 = s.get(url= url,headers=headers)
# print(response2.cookies)   # 会看到 {"cookies": {"name": "value"}}
# 第一次请求
response1 = s.get(url)
print("第一次响应新设置的 Cookie:", response1.cookies.get_dict())
print("Session 中累积的 Cookie:", s.cookies.get_dict())

# 第二次请求
response2 = s.get(url)
print("第二次响应新设置的 Cookie:", response2.cookies.get_dict())
print("Session 中累积的 Cookie:", s.cookies.get_dict())