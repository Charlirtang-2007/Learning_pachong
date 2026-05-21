spider模块解析

## BzSpider采取的是请求携带固定cookies的登录模式

````
核心代码：
    def start_requests(self) -> Iterable[Any]:
        url=self.start_urls[0]
        temp=""""""
        cookies={data.split('=')[0] :data.split('=')[-1] for data in  temp.split(';')}#改写成字典
        yield scrapy.Request(url=url,cookies=cookies,callback=self.parse)
````
代码解析
```
重写了start_requests函数
temp用来存放自己的cookies
cookies={data.split('=')[0] :data.split('=')[-1] for data in  temp.split(';')}
把temp切成列表for循环，改写成字典
```
## BquSpider 模拟登录爬虫

``` BquSpider 采用先访问首页获取 Cookie，再提交登录表单的模拟登录模式 ```

核心代码：
```python
def start_requests(self):
    yield scrapy.Request(
        url='https://www.bequke.com',
        callback=self.parse,
        errback=self.errback,
    )

def parse(self, response):
    data = {
        'username': '',
        'password': '',
        'action': 'login',
        'jumpurl': '/bookcase',
        'submit': '',
    }
    yield scrapy.FormRequest(url='https://www.bequke.com/login', formdata=data, callback=self.after_login)
def process_request(self, request, spider):
    ua=UserAgent()
    request.headers.setdefault("User-Agent", ua.chrome)
    return None
代码解析：

重写 start_requests 方法，首次请求首页，同时指定 errback 捕获请求异常（如超时、DNS 错误、非 200 响应等）。

parse 方法中构造登录所需表单数据，使用 FormRequest 提交 POST 请求，并指定登录成功后的回调 after_login。

after_login 中可处理登录后的页面内容（如打印状态码、提取标题等）。

注意：需要填写真实的 username 和 password，否则登录会失败；若网站需要验证码或动态参数，需进一步扩展。

写了处理请求的中间件函数，用于处理伪装请求头