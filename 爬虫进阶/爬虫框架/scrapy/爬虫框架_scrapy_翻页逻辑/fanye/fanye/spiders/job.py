import scrapy
import json
from fanye.items import FanyeItem
class JobSpider(scrapy.Spider):
    name = "job"
    allowed_domains = ["163.com"]
    async def start(self):
        # 第一页请求（POST）
        url = "https://hr.163.com/api/hr163/position/queryPage"
        payload = {"currentPage": 1, "pageSize": 10, "workType": "0"}
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Content-Type": "application/json",
            "Referer": "https://hr.163.com/job-list.html",
        }
        yield scrapy.Request(
            url,
            method="POST",
            body=json.dumps(payload),
            headers=self.headers,
            callback=self.parse,
            meta={"payload": payload}  # 将 payload 传下去，方便后续修改页码
        )

    def parse(self, response):
        data_text = response.text
        data = json.loads(data_text)
        job_list = data.get('data', {}).get('list', [])
        # 数据解析
        for job in job_list:
            item = FanyeItem()
            item['name'] = job.get('name')
            # 任职要求
            item['tiaojian'] = job.get('requirement')
            # 职位描述
            item['job'] = job.get('description')
            # 工作地点（可能有多个，用逗号连接）
            item['workPlaceName'] = ', '.join(job.get('workPlaceNameList', []))
            yield item
        if "pages" not in response.meta:
            total_pages = data.get("data", {}).get("pages", 1)
            response.meta["pages"] = total_pages  # 缓存总页数

        current_page = response.meta["payload"]["currentPage"]
        total_pages = response.meta["pages"]

        # 如果当前页不是最后一页，则请求下一页
        if current_page < total_pages:
            next_page = current_page + 1
            payload = response.meta["payload"].copy()#安全创建字典
            payload["currentPage"] = next_page
            yield scrapy.Request(
                response.url,
                method="POST",
                body=json.dumps(payload),
                headers=self.headers,
                callback=self.parse,
                meta={"payload": payload, "pages": total_pages}
            )


