#导入类和模块
from aip import AipOcr
from api_key.api_peizhi import Apikey

class BaiDuOcr:
    def __init__(self):
        # 获取密钥
        keys = Apikey()
        self.client = AipOcr(keys.app_id, keys.api_key, keys.secret_key)

    def ocr_image(self, image_input):
        """识别本地图片中的文字，返回所有识别的文本列表"""
        #判断是否是，base64编码
        if isinstance(image_input, bytes):
            image = image_input
        else:
            with open(image_input, 'rb') as f:
                image = f.read()
        # 调用高精度识别接口（basicAccurate）
        result = self.client.basicAccurate(image)
        # 提取文字
        words = [item['words'] for item in result.get('words_result', [])]
        return words

    def ocr_url(self, url):
        """识别网络图片（URL），返回文字列表"""
        result = self.client.webImage(url=url)
        return [item['words'] for item in result.get('words_result', [])]

# 使用示例
if __name__ == '__main__':
    ocr = BaiDuOcr()
    texts = ocr.ocr_image('code.png')
    for text in texts:
        print(text)