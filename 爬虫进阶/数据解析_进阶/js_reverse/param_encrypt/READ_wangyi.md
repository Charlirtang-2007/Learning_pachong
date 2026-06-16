# 项目：网易云评论与歌词的数据获取


## 技术：js逆向_参数加密逆向，具体表现为：
````
params=Jkw0qw6SHRH%2BTSKyE598iy4sZ0QbV78%2Bk6hbsjfPZvvtHxLv4%2BR2jUFwozfKfkji
encSecKey=8e401d1ee3a3da1fa3c81e1da0aa9bcdf5b6c2088cd1ace3a145904ec2bc5556091006167e99be57effc609710131ba15f58eaf471a39d9bd30eec74c4f368e074bc8ed13fa46821bcb610165d2d9403c4cf02ad0f54403d7bf509b1910e1e744465654fa5490031f3a38efb108434cf6d0b34304b4343662be6d3a5a5802937
````
### 主要文件为：
```
wangyi.js_加密代码
wangyi_ly.py_获取歌词代码
wangyi_pin.py_获取歌曲评论代码
wangyi.md_最初的逆向分析文件

```
### wangyi_pin.py翻页代码解释
```
思路：先从返回数据中获取-total_count（总评论数），并记录当前页面游标（翻页标识时间戳，唯一标识）
“对于游标（data.cursor）：它是服务器单独拎出来的边界标记，它的值恰好等于这一页里最后一条（最旧的那条）评论的时间戳。”

然后通过游标和总评论共同判断是否结束

 ====== 判断是否已获取全部（方式一：总数对比） ======

if total_count > 0 and len(all_comments) >= total_count:
    print("已获取全部评论")
    break

 ====== 判断是否已获取全部（方式二：游标变化检测） ======

new_cursor = result.get('data', {}).get('cursor')
if not new_cursor or new_cursor == cursor:
    print("游标无变化，翻页结束")
    break

 ====== 实现翻页（更新游标和页码） ======

cursor = new_cursor
page_no += 1

另外，在构造请求参数的地方，也用到了当前游标：

d = json.dumps({
    # ... 其他参数 ...
    "cursor": cursor,   # 这里把当前的游标值传给服务器
    # ...
})
```