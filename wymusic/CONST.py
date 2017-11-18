"""
项目中用到的常量
"""
import os


# 加密相关
PUBKEY = '010001'
MODULUS = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
NONCE = '0CoJUm6Qyw8W8jud'
ENCSECKEY = '257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c'
IV = '0102030405060708'
# 登陆相关
HEADERS = {
    'Referer': 'http://music.163.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded'
}
URLS = {
    'login_phone': 'http://music.163.com/weapi/login/cellphone',
    'id2url': 'http://music.163.com/weapi/song/enhance/player/url?csrf_token=',
    'daily': 'http://music.163.com/weapi/v2/discovery/recommend/songs?csrf_token='
}
LOGINNEEDED = ['daily']
# 文件相关
COOKIE = 'login.cookie'
DATEBASE = 'music.db'
DAILYTEMP = 'daily.temp'
PLAYEDTEMP = 'played.temp'
MPG123 = 'mpg123.exe'
BASEPATH = os.path.split(os.path.realpath(__file__))[0]
