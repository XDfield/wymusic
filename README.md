# wymusic
如何优雅地收听网易云音乐每日推荐
---
### Disc  
一个偶然的想法, 作为一个懒得打开网易云音乐的人, 只想随手播放每日推荐曲目  
简单易用, 基于*Python3.5*, 音乐播放使用的mpg123  
一运行就拉取当天的每日歌单保存到数据库中(使用sqlite3), 同一天不会重复拉取, 首次使用需要进行登陆

> Requried Python Pakage:  
> requests

### Installation  
```shell
git clone https://github.com/XDfield/wymusic.git
cd wymusic
python setup.py install
```

### How To Use
```shell
$ wymusic
```  
现阶段实现了随机播放一首每日歌曲

### log  
* 2017/11/18 创建项目  

### Todo
* 循环播放
* 优化界面
* 读取数据库中某天数据进行播放
