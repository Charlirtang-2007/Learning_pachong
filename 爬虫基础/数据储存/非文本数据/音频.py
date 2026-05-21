import requests

headers = {

}

response = requests.get(
    'https://er-sycdn.kuwo.cn/4696d62d683039be3d3346ff74c3d781/69fd8523/resource/30106/trackmedia/M500004XePmv4CsaEq.mp3?bitrate$128&from=vip',
    headers=headers,
)
#wb写入，格式为MP3

with open('download.mp3', 'wb') as f:
    f.write(response.content)

