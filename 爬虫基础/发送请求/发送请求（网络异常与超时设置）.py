import requests
from requests.exceptions import Timeout, ConnectionError, HTTPError
url = 'https://www.bequke.com/'
timeout = (2, 3)   # 连接超时 2 秒，读取超时 3 秒

try:
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()   # 如果状态码不是 2xx，抛出 HTTPError
    print('请求成功', response.text[:100])#显示100个字符

except Timeout:
    print('请求超时')
except ConnectionError:
    print('网络连接失败（DNS 错误、拒绝连接等）')
except HTTPError as e:
    print(f'HTTP 错误：{e.response.status_code}')
except Exception as e:
    print(f'其他异常：{e}')