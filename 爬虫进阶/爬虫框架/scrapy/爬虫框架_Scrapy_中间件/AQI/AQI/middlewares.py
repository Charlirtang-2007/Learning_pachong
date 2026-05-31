# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from anyio import sleep
from scrapy import signals
import time
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from selenium.common.exceptions import TimeoutException
import time
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from fake_useragent import UserAgent

class AqiSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    async def process_start(self, start):
        # Called with an async iterator over the spider start() method or the
        # matching method of an earlier spider middleware.
        async for item_or_request in start:
            yield item_or_request

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

class FakeUserAgentMiddleware:
    ua = UserAgent()  # 类变量，只加载一次
    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', self.ua.chrome)
        spider.logger.debug(f'请求头: {request.headers}')

class AqiSeleniumMiddleware:
    def __init__(self):
        # 1. 指定 ChromeDriver 路径
        driver_path = r"D:\浏览器自动化\chromedriver-win32\chromedriver-win32\chromedriver.exe"

        # 2. 配置 ChromeOptions（无头模式 + 反检测）
        options = Options()
        # 无头模式核心参数
        options.add_argument('--headless')               # 启用无头模式
        options.add_argument('--window-size=1920,1080')  # 必须设置窗口大小
        options.add_argument('--disable-gpu')            # 禁用GPU加速
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        # 可选：禁用图片加速加载（如果只需要文本）
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)

        # 3. 创建 Service 对象
        service = Service(driver_path)

        # 4. 启动浏览器
        self.driver = webdriver.Chrome(service=service, options=options)

        # 5. 应用 selenium-stealth 隐藏指纹
        stealth(self.driver,
                languages=["zh-CN", "zh"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                run_on_insecure_origins=True
                )

    def process_request(self, request, spider):
        # 检查 meta 中是否要求使用 Selenium
        if not request.meta.get('selenium', False):
            return None  # 继续使用默认下载器
        self.driver.get(request.url)
        time.sleep(2)  # 可根据需要改用 WebDriverWait 提高稳定性
        body = self.driver.page_source
        return HtmlResponse(
            url=self.driver.current_url,
            body=body,
            encoding='utf-8',
            request=request
        )

    def __del__(self):
        # 爬虫结束时关闭浏览器
        if hasattr(self, 'driver'):
            self.driver.quit()

class AqiDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
