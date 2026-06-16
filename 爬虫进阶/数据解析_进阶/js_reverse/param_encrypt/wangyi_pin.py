import csv
import time
import json
import requests
import execjs

# ========== 固定配置 ==========
headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,en-GB;q=0.6',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    'dnt': '1',
    'origin': 'https://music.163.com',
    'pragma': 'no-cache',
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

e = '010001'
p = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
g = '0CoJUm6Qyw8W8jud'

# 读取并编译 JS（只编译一次）
with open('wangyi.js', 'r', encoding='utf-8') as f:
    js_code = f.read()
ctx = execjs.compile(js_code)


def get_all_comments(song_id, page_size=100):
    """
    获取指定歌曲的全部评论
    :param song_id: 歌曲 ID
    :param page_size: 每页条数，建议 100
    :return: 评论列表（每个评论为原始 dict）
    """
    all_comments = []
    cursor = "-1"#游标默认为-1
    page_no = 1#页码
    total_count = None#评论总数

    while True:
        # 构造请求参数
        d = json.dumps({#转字符串
            "rid": f"R_SO_4_{song_id}",
            "threadId": f"R_SO_4_{song_id}",
            "pageNo": str(page_no),
            "pageSize": str(page_size),#每页显示数
            "cursor": cursor,
            "offset": "0",
            "orderType": "3",          # 时间排序，支持游标翻页
            "csrf_token": ""
        })

        # 加密
        encrypted = ctx.call('KO', d, e, p, g)
        data = {
            'params': encrypted['encText'],
            'encSecKey': encrypted['encSecKey']
        }

        # 发送请求
        resp = requests.post(
            'https://music.163.com/weapi/comment/resource/comments/get',
            headers=headers,
            data=data
        )
        result = resp.json()
        print(result)

        # 检查响应状态
        if result.get('code') != 200:
            print(f"请求失败，code={result.get('code')}")
            break

        # 第一次请求获取总条数
        if total_count is None:
            total_count = result.get('data', {}).get('totalCount', 0)
            print(f"总评论数: {total_count}")

        comments = result.get('data', {}).get('comments', [])
        if not comments:
            print("本页无评论，停止")
            break

        all_comments.extend(comments)#将当前获取评论列表逐个追加到总评论列表
        print(f"已获取 {len(all_comments)} 条评论")

        # ====== 判断是否已获取全部 ======
        if total_count > 0 and len(all_comments) >= total_count:
            print("已获取全部评论")
            break

        # ====== 游标变化检测 ======
        new_cursor = result.get('data', {}).get('cursor')
        if not new_cursor or new_cursor == cursor:
            print("游标无变化，翻页结束")
            break

        # 更新游标和页码
        cursor = new_cursor
        page_no += 1

        # 安全限制
        max_pages = (total_count // page_size) + 5  # 根据总条数计算，多留几页余量
        if page_no > max_pages:
            print("超过计算的最大页数，强制停止")
            break

        time.sleep(0.3)  # 礼貌延时

    return all_comments


def save_comments_to_csv(comments, filename='w_comments.csv'):
    """将评论列表保存为 CSV 文件"""
    fieldnames = ['commentId', 'nickname', 'content', 'timeStr', 'likedCount', 'ipLocation']
    with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for i in comments:
            row = {
                'commentId': i.get('commentId'),
                'nickname': i.get('user', {}).get('nickname', '未知用户'),
                'content': i.get('content', '').replace('\n', ' ').replace(',', '，'),
                'timeStr': i.get('timeStr'),
                'likedCount': i.get('likedCount', 0),
                'ipLocation': i.get('ipLocation', {}).get('location', '未知')
            }
            writer.writerow(row)
    print(f"已保存 {len(comments)} 条评论到 {filename}")


# ========== 主程序 ==========
if __name__ == '__main__':
    song_id = 3382908505  # 你要抓取的歌曲 ID
    page_size = 100       # 每页条数

    print("开始抓取评论...")
    all_comments = get_all_comments(song_id, page_size)
    print(f"共获取 {len(all_comments)} 条评论")

    if all_comments:
        save_comments_to_csv(all_comments)
    else:
        print("未获取到任何评论")