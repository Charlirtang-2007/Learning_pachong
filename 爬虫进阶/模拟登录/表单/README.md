此代码介绍了，post请求模拟登录，session保持对话

目标网址：
````
start_url:'https://www.bequke.com/login'
````
核心代码解析：
```
r=requests.post(url,data=payload,headers=headers)
发送post请求，携带data参数，以字典的形式，传输

#创建对话对象Session
session = requests.session()
#发送登录请求
r=session.post(url,data=payload,headers=headers)
#利用session保持对话提取数据
r1=session.get(url='https://www.bequke.com/bookcase',headers=headers)
#关闭session
session.close()
```