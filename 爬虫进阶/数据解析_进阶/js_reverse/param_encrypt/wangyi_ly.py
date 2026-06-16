import requests
import execjs
import json

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,en-GB;q=0.6',
    'content-type': 'application/x-www-form-urlencoded',
    'dnt': '1',
    'origin': 'https://music.163.com',
    'priority': 'u=1, i',
    'referer': 'https://music.163.com/song?id=3314385057',
    'sec-ch-ua': '"Microsoft Edge";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 Edg/149.0.0.0',
    }
# d='{"id":"3314385057","lv":-1,"tv":-1,"csrf_token":""}'
d='{"id":"3382908505","lv":-1,"tv":-1,"csrf_token":""}'#只有歌曲id在改变
e='010001'
p='00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7';
g='0CoJUm6Qyw8W8jud'
with open('wangyi.js') as f:
    file=f.read()
s=execjs.compile(file).call('KO',d,e,p,g)#转换并调用函数
params = {
    'csrf_token': '',
}

data = {
    'params':s['encText'] ,
    'encSecKey': s['encSecKey']}

response = requests.post('https://music.163.com/weapi/song/lyric', params=params,  headers=headers, data=data)
da=json.loads(response.text)
l=da['lrc']['lyric']
print(l)