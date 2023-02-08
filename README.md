# PixivImgDownloader

## pixiv图片下载器

<br>
作为一个喜欢收藏好看插画的人，每次用手点保存图片实在是效率低下，
就花了点时间用python写了个能批量下载的程序，
能下载排行榜的图片和画师的作品。用selenium登录一次拿到cookie之后就可以用了。
至于cookie能用多久没测试过，要是下载的图数量不对可以删掉cookie重新获取一次。
<br/>

支持排行榜url所有参数，动图会自动合成为gif，gif合成器方面的代码用的多进程，有空闲时间会改成多线程。
下载动图排行榜的时候如果用多进程稍微有点占内存，可以改下代码。

用法：

```python
from PixivImageDownloader import PixivScheduler

# 要使用多进程要指定multy_process=True，multy_process默认为False
# 还支持图片大小有 ['mini', 'thumb', 'small', 'regular', 'original']，image_size默认为original
# 动图支持的size有 ['src', 'originalSrc']，ugoira_size默认为originalSrc
# 第一次使用请输入用户名，当保存了cookie文件之后就不需要登录了
PS = PixivScheduler(username="Your username",
                    password="Your password",
                    image_size='regular',
                    multy_process=True)
PS.rank_mode()  # 排行榜模式，默认下载当日综合排行榜，参数根据排行榜url输入就行了
# 比如https://www.pixiv.net/ranking.php?mode=daily&content=illust
PS.rank_mode(mode='daily', content='illust')
# 比如https://www.pixiv.net/users/25760573
# 输入字符串或者int都可以
PS.artist_mode(25760573)
```

功能基本已经写好了，想自定义自己的下载器可以看注释，应该都写清楚了。
我好像忘记添加代理功能了，国内用户可以给requests_get添加你自己的代理就可以了。


