#```````普通表单发送post请求，````````#
# import requests
# url='https://www.bequke.com/login'
# payload={
# 'username':'',
# 'password':'',
# 'action':'login',
# 'jumpurl':'/bookcase',
# 'submit':'',
# }
# headers = {'user-agent':
# 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36'}
# r=requests.post(url,data=payload,headers=headers)
# print(r.text)
#```````````保持对话session````````````#
import requests
from parsel import Selector
url='https://www.bequke.com/login'
payload={
'username':'',
'password':'',
'action':'login',
'jumpurl':'/bookcase',
'submit':'',
}
headers = {'user-agent':
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36'}
#创建对话对象Session
session = requests.session()
#发送登录请求
r=session.post(url,data=payload,headers=headers)
#利用session保持对话提取数据
r1=session.get(url='https://www.bequke.com/bookcase',headers=headers)
selector = Selector(r1.text)
name=selector.xpath('//*[@id="wrapper"]/div[1]/div/div/h4/text()').get()
print(name)
session.close()
