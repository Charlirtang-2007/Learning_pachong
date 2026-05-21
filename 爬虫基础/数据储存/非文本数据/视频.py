import requests

cookies = {
    }

headers = {
    }

response = requests.get(
    'https://fd.aigei.com/src/vdo/mp4/0f/0f4886c48aba481b8112976cd151551f.mp4?e=1778227800&token=P7S2Xpzfz11vAkASLTkfHN7Fw-oOZBecqeJaxypL:62Eo9CMhMCZHLQCgRnSjd3iKCC8=',
    cookies=cookies,
    headers=headers,
)
with open("downloaded_mp4.mp4", "wb") as f:
    f.write(response.content)