import requests

headers = {

}
#保存为二进制格式，后缀为jpg
response = requests.get('https://haowallpaper.com/link/common/file/previewFileImg/17222912254725504', headers=headers)
if response.status_code == 200:
    # 以二进制写入模式打开一个本地文件，准备保存内容
    # 使用 with open 可以确保文件最终会被正确关闭
    with open("downloaded_image.png", "wb") as file:
        file.write(response.content)
        print("✅ 图片下载成功！已保存为 downloaded_image.jpg")
else:
    print(f"❌ 请求失败，状态码: {response.status_code}")
