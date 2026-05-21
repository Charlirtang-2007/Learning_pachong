## JobSpider 采用 POST 方式翻页

``` JobSpider 通过 POST 请求调用网易招聘 API，实现分页获取职位数据 ```

核心代码：
```python
async def start(self):
    url = "https://hr.163.com/api/hr163/position/queryPage"
    payload = {"currentPage": 1, "pageSize": 10, "workType": "0"}
    yield scrapy.Request(
        url,
        method="POST",
        body=json.dumps(payload),
        headers=self.headers,
        callback=self.parse,
        meta={"payload": payload}
    )

def parse(self, response):
    data = json.loads(response.text)
    # 解析职位列表...
    # 翻页：修改 payload 中的 currentPage，继续 POST
```

代码解析：
- 重写 `start` 方法（Scrapy 2.13+ 推荐使用 `start` 替代 `start_requests`），构造第一页的 POST 请求。
- 请求体使用 `json.dumps` 转换字典，并设置 `Content-Type: application/json`。
- 在 `parse` 中解析 JSON 响应，提取职位字段并生成 Item。
- 通过 `meta` 传递 `payload` 和总页数，实现循环翻页：每次判断当前页是否小于总页数，是则构造下一页的 POST 请求继续请求相同 URL。

## ZgcSpider 采用 GET 方法翻页

``` ZgcSpider 通过 GET 请求访问中关村在线笔记本列表页，提取商品链接并自动翻页 ```

核心代码：
```python
def parse(self, response):
    list_box = response.css('div.content div.list-box div.list-item')
    for li in list_box:
        item = ZgcItem()
        item["link"] = response.urljoin(li.css('div.pro-intro h3 a::attr(href)').get())
        item["name"] = li.css('div.pro-intro h3 a::text').get()
        yield item
    # 翻页逻辑
    if response.css('div.page-box div.pagebar a.next::text').get() == "下一页":
        next_url = response.css('div.page-box div.pagebar a.next::attr(href)').get()
        yield response.follow(next_url, self.parse)
        page = response.css('div.page-box div.pagebar span.sel::text').get()
        print("当前页数为" + page)
```

代码解析：
- 使用 `start_urls` 指定第一页 URL，Scrapy 自动发起 GET 请求。
- `parse` 中通过 CSS 选择器提取每个商品的链接和名称，生成 Item。
- 翻页判断：检查“下一页”按钮是否存在，若存在则获取其 `href` 属性，通过 `response.follow` 自动拼接完整 URL 并递归调用 `parse`。
- 同时输出当前页码，便于调试。

## 总结对比

| 爬虫 | 请求方式 | 翻页方式 | 数据来源 |
|------|----------|----------|----------|
| JobSpider   | POST | 修改 body 中的 `currentPage` 字段 | JSON API |
| ZgcSpider   | GET  | 提取下一页链接并使用 `response.follow` | HTML 页面 |
```