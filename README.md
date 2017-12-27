# wymusic
如何优雅地收听网易云音乐每日推荐
---
### Disc  
一个偶然的想法, 作为一个懒得打开网易云音乐的人, 只想随手播放每日推荐曲目  
简单易用, 基于*Python3.5*, 音乐播放使用的mpg123  
拉取当天的每日歌单保存到数据库中(使用sqlite3), 同一天不会重复拉取, 首次使用需要进行登陆

#### 依赖包
> requests

### Installation  
```shell
git clone https://github.com/XDfield/wymusic.git
cd wymusic
python setup.py install
```  
**(必做)**: 将mpg123.exe文件目录添加到PATH环境变量中

### How To Use
```shell
$ wymusic
```  
随机播放一首每日歌曲  

> 参数说明:  
> -l: 循环播放每日歌单

### log  
* 2017/11/19 添加循环播放每日歌曲功能
* 2017/11/18 创建项目  

### Bug
* 由于不携带Cookie,每天播放的曲子不会统计到用户数据中,会导致每日歌曲总是那几首,需要再考虑一个新的方案


### Todo
* 优化界面
* 读取数据库中某天数据进行播放
* 播放指定id专辑
