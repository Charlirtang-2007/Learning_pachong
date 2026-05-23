# Python 网络请求示例集

本目录包含多个使用 `requests` 库发送 HTTP 请求的 Python 示例脚本，涵盖了基础请求、随机 User-Agent、代理使用、代理池轮换、Session 与 Cookies 管理、超时与异常处理等常见场景。

## 环境依赖

安装所需依赖：

```bash
pip install requests fake-useragent
```

> 注：`fake-useragent` 用于随机生成浏览器 User-Agent，若无需此功能可移除相关代码。

## 文件说明

### 1. `发送请求.py`
最基本的 GET 请求示例。

- 发送请求到 `https://www.bequke.com/`
- 打印状态码、响应头、响应二进制内容、编码信息

```bash
python 发送请求.py
```

### 2. `发送请求（添加伪装01）.py`
添加随机 User-Agent 伪装浏览器。

- 使用 `fake_useragent` 随机生成 UA
- 发送 GET 请求

```bash
python 发送请求（添加伪装01）.py
```

### 3. `发送请求（添加伪装02）.py`
使用 `requests.Session()` 管理 Cookies，演示多次请求自动携带 Cookie。

- 创建 Session 对象
- 设置随机 UA
- 发送两次请求，观察 Session 中累积的 Cookie

```bash
python 发送请求（添加伪装02）.py
```

### 4. `发送请求（代理服务器）.py`
通过单一代理服务器发送请求，并验证出口 IP。

- 需手动修改 `proxies` 字典中的代理地址（示例为 HTTP 代理）
- 使用 Session + 随机 UA
- 请求 `httpbin.io/ip` 查看当前出口 IP

```bash
python 发送请求（代理服务器）.py
```

> 注意：示例中的代理地址 `8.130.74.114:9080` 可能已失效，请替换为实际可用代理。

### 5. `发送请求（代理服务器，ip池轮换）.py`
维护一个代理 IP 池，循环尝试直到找到第一个可用的代理并发送请求。

- 代理池列表 `proxies_list`（请替换为真实可用代理）
- 遍历代理，构造 `proxies` 字典
- 请求 `httpbin.io/ip` 和目标网站
- 成功则跳出循环并打印响应内容

```bash
python 发送请求（代理服务器，ip池轮换）.py
```

### 6. `发送请求（网络异常与超时设置）.py`
设置连接超时和读取超时，并捕获常见的网络异常。

- 超时设置：`(2, 3)` 表示连接超时 2 秒，读取超时 3 秒
- 捕获 `Timeout`、`ConnectionError`、`HTTPError` 等异常
- 使用 `response.raise_for_status()` 检查 HTTP 状态码

```bash
python 发送请求（网络异常与超时设置）.py
```

## 注意事项

1. **代理地址可用性**：所有脚本中的代理 IP 可能随时失效，请替换为你自己可用的代理（或使用付费代理服务）。
2. **目标网站**：示例中使用的 `https://www.bequke.com/` 可能因网络或反爬措施无法访问，建议替换为测试网址如 `http://httpbin.org/get`。
3. **法律合规**：请勿使用这些脚本对任何网站进行高频请求或绕过访问限制，仅用于学习和测试目的。
4. **异常处理**：生产环境中建议对 `requests` 异常进行更细致的捕获和重试处理。

## 扩展建议

- 如需更多并发请求，可结合 `concurrent.futures` 或 `asyncio`。
- 若需要更完整的代理轮换和失败重试机制，推荐使用 `requests` 搭配 `retrying` 或 `tenacity` 库。
- 对于更复杂的爬虫场景，建议使用 `Scrapy` 或 `Playwright`。

---

如果你在使用过程中遇到问题，欢迎补充说明。