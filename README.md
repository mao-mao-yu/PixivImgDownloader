# PixivImgDownloader

## pixiv图片下载器  

### This code is provided for learning and research purposes only and is not intended for illegal activities.  
### 代码仅供学习和研究使用，严禁用于非法活动。  
<br>
请勿干扰服务器的运行，请添加1-5秒的sleep。  
作为一个喜欢收藏好看插画的人，每次用手点保存图片实在是效率低下，
就花了点时间用python写了个能批量下载的程序，顺便加深一下理解。

主要功能为：下载排行榜的图片和画师的作品。用selenium登录一次拿到cookie之后就可以用了。
至于cookie能用多久没测试过，要是下载的图数量不对可以删掉cookie重新获取一次。
<br/>

支持排行榜url所有参数，动图会自动合成为gif，gif合成器方面的代码用的多进程，有空闲时间会改成多线程。
下载动图排行榜的时候如果用多进程稍微有点占内存，可以改下代码。

新增了搜索模式。

用法：

```python
from PixivImageDownloader import PixivScheduler, DownloadQueue

# 要使用多进程要指定multy_process=True，multy_process默认为False
# 还支持图片大小有 ['mini', 'thumb', 'small', 'regular', 'original']，image_size默认为original
# 动图支持的size有 ['src', 'originalSrc']，ugoira_size默认为originalSrc
# 第一次使用请输入用户名，保存了cookie文件之后就不需要登录了
PS = PixivScheduler(username="Your username",
                    password="Your password",
                    image_size='regular',
                    multy_process=True)
Q = DownloadQueue()

# 排行榜模式
params_li = PS.rank_mode()  # 排行榜模式，默认下载当日综合排行榜，参数根据排行榜url输入就行了
Q.add_task(params_li)  # 添加参数到下载队列
# https://www.pixiv.net/ranking.php?mode=daily&content=illust
params_li = PS.rank_mode(mode='daily', content='illust')
Q.add_task(params_li)  # 添加参数到下载队列

# 画师模式
# https://www.pixiv.net/users/画师ID
# 画师ID输入字符串或者int都可以
params_li = PS.artist_mode('画师ID', content='illust')  # 画师模式
Q.add_task(params_li)  # 添加参数到下载队列

# 搜索模式
# https://www.pixiv.net/tags/{搜索关键字}/illustrations?order=popular_d&mode=safe&scd=2023-01-10&s_mode=s_tag&type=illust
# order默认为popular_d mode默认safe scd默认为空 s_mode模式为s_tag type默认为illust
# 然后还默认搜索1000x1000以上像素的图 ,也可以设置blt bgt参数设置被收藏数的区间
# 还有更多其他参数详见ImageDataGetter.search_data注释
# 比如上面这个url我只需要传入scd的参数就行了，或者你想搜索别的也可以改参数
params_li = PS.search_mode("オリジナル", scd='2023-01-10')
Q.add_task(params_li)
# 如果只传入搜索关键词则默认以以下参数搜索
params_li = PS.search_mode("初音ミク")
params = {
    "order": "popular_d",
    'mode': 'safe',
    's_mode': 's_tag',
    'type': 'illust',
    'p': '1',
    'hlt': '1000',
    'wlt': '1000',
}
Q.run()
```

基本功能已经写好了，想自定义自己的下载器可以看各个类的注释。后续随缘完善功能和GUI界面


