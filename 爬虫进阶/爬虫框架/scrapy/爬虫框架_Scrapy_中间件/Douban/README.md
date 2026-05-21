## DoubanSpider（豆列内容爬取）
目标：爬取豆瓣豆列 https://www.douban.com/doulist/45012218/ 中每个条目指向的详情页，并进一步提取隐藏链接中的资源标题。

## 爬取流程：
```
parse：提取豆列页中所有 div.bd.doulist-subject div.title a 的 href 属性，得到每个条目的详情页 URL。

aftert_parse：进入详情页后，通过 XPath 定位 //form[@id="sec"]/input[@id="red"]/@value，获得一个隐藏的跳转链接。

text_parse：访问该跳转链接，输出目标页面的标题（<title> 标签内容）。

```
代码示意：
```
python
class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["douban.com"]
    start_urls = ["https://www.douban.com/doulist/45012218/"]

    def parse(self, response):
        for a in response.css("div.bd.doulist-subject div.title a"):
            url = a.css('::attr(href)').get()
            if url:
                yield response.follow(url, callback=self.aftert_parse)

    def aftert_parse(self, response):
        link = response.xpath('//form[@id="sec"]/input[@id="red"]/@value').get()
        if link:
            yield response.follow(link, callback=self.text_parse)

    def text_parse(self, response):
        print(response.css("title::text").get())
```
## 配置详解（settings.py）
```
基础配置
python
BOT_NAME = "Douban"
SPIDER_MODULES = ["Douban.spiders"]
ROBOTSTXT_OBEY = False          # 不遵守 robots.txt（部分站点会限制爬虫）
LOG_LEVEL = "WARNING"           # 仅输出警告及以上级别日志
COOKIES_ENABLED = True          # 启用 Cookies 中间件（模拟登录需要）
并发与延迟策略（降低请求频率，减少被封）
python
CONCURRENT_REQUESTS = 3                 # 全局并发数
CONCURRENT_REQUESTS_PER_DOMAIN = 1      # 同一域名下仅 1 个并发
DOWNLOAD_DELAY = 1.5                    # 请求间隔 1.5 秒
为什么这样设置？
豆瓣反爬较严格，高并发或短间隔易触发封 IP。降低并发并增加延迟可模拟人类浏览行为。
自动限速（AutoThrottle）
python
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1.0          # 初始延迟
AUTOTHROTTLE_MAX_DELAY = 10.0           # 最大延迟
AUTOTHROTTLE_TARGET_CONCURRENCY = 0.5   # 目标平均并发数（较低值更保守）
AUTOTHROTTLE_DEBUG = True               # 调试输出限速信息
作用：根据服务器响应时间动态调整请求延迟，响应慢时自动降速，避免对目标服务器造成压力。

默认请求头
python
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Referer': 'https://www.douban.com/',
}
为什么设置 Referer？
豆瓣部分页面会校验 Referer，伪造为豆瓣首页可提高请求成功率。

代理列表（PROXY_LIST）
python
PROXY_LIST = [
    '113.204.79.230:9091',
    '120.26.123.95:8010',
    # ... 共 15 个代理
]
作用：当 IP 被封锁时，可轮换使用不同代理继续爬取。列表中的代理应定期测试有效性。
```
## 中间件详解（middlewares.py）

1.FakeUserAgentMiddleware – 随机 User‑Agent
目的：每次请求使用不同的 Chrome 版本 UA，避免被识别为爬虫。

实现：

使用 fake_useragent 库动态生成 UA（UserAgent().chrome）。

在 process_request() 中设置请求头的 User-Agent 字段。
```
python
class FakeUserAgentMiddleware:
    ua = UserAgent()   # 类变量，仅加载一次，提高效率

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', self.ua.chrome)
        spider.logger.debug(f'请求头: {request.headers}')
为什么放在中间件？
可以统一管理 UA 设置，无需在每个爬虫中重复代码。且中间件可全局生效。
```

2. RandomProxyMiddleware – 随机代理
目的：每个请求随机选择一个代理 IP，降低 IP 被封风险。

实现：

从 settings.PROXY_LIST 中读取代理列表。

process_request() 中随机选择一个代理，拼接 http:// 前缀（若无），存入 request.meta['proxy']。
```
python
class RandomProxyMiddleware:
    def __init__(self, proxy_list):
        self.proxy_list = proxy_list

    @classmethod
    def from_crawler(cls, crawler):
        proxy_list = crawler.settings.getlist('PROXY_LIST')
        return cls(proxy_list)

    def process_request(self, request, spider):
        proxy = random.choice(self.proxy_list)
        if not proxy.startswith(('http://', 'https://')):
            proxy = 'http://' + proxy
        request.meta['proxy'] = proxy
        spider.logger.debug(f'使用代理: {proxy}')
```
为什么不在爬虫中直接写？
中间件可自动为每个请求分配代理，且支持动态更换，代码更简洁。

中间件启用顺序（settings.py）
python
DOWNLOADER_MIDDLEWARES = {
    "Douban.middlewares.FakeUserAgentMiddleware": 542,
    "Douban.middlewares.RandomProxyMiddleware": 543,
    "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,  # 禁用默认 UA 中间件
}
数字越小越靠近引擎，越先处理请求。此处 542 < 543，所以先设置 UA，再设置代理。

禁用默认 UA 中间件，避免冲突。

运行说明
环境依赖
bash
pip install scrapy fake-useragent
启动爬虫
bash
## 进入项目根目录（包含 scrapy.cfg 的目录）
scrapy crawl douban          # 运行豆瓣豆列爬虫
调试技巧
将 LOG_LEVEL 改为 "DEBUG" 可查看详细请求日志。

设置 AUTOTHROTTLE_DEBUG = True 观察限速动态。

测试代理是否可用：可临时在 RandomProxyMiddleware 中添加 print(proxy) 输出使用的代理。

注意事项：

代理有效性：PROXY_LIST 中的代理可能随时失效，建议搭配代理检测脚本定期更换。

遵守法律法规：爬取豆瓣等网站时请控制请求频率，不要对目标服务器造成压力，并尊重网站的 robots.txt（本例已关闭，但道德上仍建议合理爬取）。

数据提取健壮性：DoubanSpider 中 XPath 路径 //form[@id="sec"]/input[@id="red"] 依赖页面结构，网站改版后需及时调整。

结束语：本项目展示了 Scrapy 中常见的反爬对抗手段（随机 UA、代理、延迟、限速、Cookies/模拟登录）。可根据实际目标网站灵活组合使用。