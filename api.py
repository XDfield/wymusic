"""
项目中用到的API
"""
import os
import sys
import re
import json
import hashlib
import base64
import sqlite3
import random
import requests

from lxml import etree
from datetime import datetime, timedelta
from Crypto.Cipher import AES
from CONST import *


# -----------------------------------------------------------------
# 信息获取相关
# -----------------------------------------------------------------
def getDataById(songId):
    """
    通过歌曲ID返回真实链接
    id: 歌曲id(可以是id的列表或者单个id)
    return: 歌曲信息(dict)
            {'songId':{
                'status':True/False,
                'url': music_url(if success),
                'msg': some info
                }
            }
    """
    d = {
        'ids': '[{}]'.format(songId),
        'br': 128000,
        'csrf_token': ''
    }
    res = encryptAndPost(d, 'id2url')
    json_res = res.json()
    music_url = json_res['data'][0]['url']
    result = dict()
    result[str(songId)] = {
        'status': True,
        'url': music_url,
        'msg': 'success'
    }
    return result


def getDailyInfos():
    """
    返回当天每日推荐歌曲信息
    return: 歌曲信息(list)
    [
        {
            'name': songName,
            'id': songId,
            'time': songTime,
            'author': songAuthor,
            'album': songAlbum
        }
    ]
    """
    result = list()
    data = {
        'csrf_token': '',
        'limit': "20",
        'offset': '0',
        'total': 'true'
    }
    res = encryptAndPost(data, 'daily')
    recommends = res.json()['recommend']
    for i in recommends:
        item = dict()
        item['name'] = i['name']
        item['id'] = i['id']
        item['time'] = i['duration']  # 毫秒数
        item['author'] = i['artists'][0]['name']
        item['album'] = i['album']['name']
        result.append(item)
    return result


# -----------------------------------------------------------------
# 常用api
# -----------------------------------------------------------------
def log(msg, mode=''):
    """
    彩色输出信息
    msg: 待输出信息
    mode: 信息类别
    """
    print(msg)


def encryptAndPost(data, mode):
    """
    加密并发送信息
    data: 待发送信息(dict)
    mode: 发送类别
    return: response
    """
    # 先将待发送信息dumps为字符串
    data = json.dumps(data, ensure_ascii=False)
    encText = aesEncrypt(aesEncrypt(data, NONCE), 16 * 'F')
    encSecKey = ENCSECKEY
    postData = {
        'params': encText,
        'encSecKey': encSecKey
    }
    url = URLS[mode]
    with requests.Session() as s:
        cookie = getCookie() if mode in LOGINNEEDED else None
        res = s.post(url=url, headers=HEADERS, data=postData, cookies=cookie)
    return res


# ------------------------------------------------------------------
# 数据库相关
# ------------------------------------------------------------------
def loadDaily():
    """
    读取今日推荐曲单
    :return:
    """
    today = getDate()
    if os.path.exists(DAILYTEMP):
        with open(DAILYTEMP, 'r', encoding='utf-8') as f:
            json_temp = json.loads(f.read())
        if today not in json_temp.keys():
            os.remove(DAILYTEMP)
            if os.path.exists(PLAYEDTEMP):
                os.remove(PLAYEDTEMP)
        else:
            return json_temp[today]
    songData = getDailyInfos()
    save2DB(songData, today)
    with open(DAILYTEMP, 'w', encoding='utf-8') as f:
        f.write(json.dumps({today: songData}, ensure_ascii=False))
    return songData


def save2DB(songData, today):
    """
    保存今日数据到数据库
    :param songData: 曲单列表
    :param today: 今日日期
    :return:
    """
    conn = sqlite3.connect(DATEBASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE '{}' 
            (ID INT PRIMARY KEY NOT NULL,
            songName TEXT NOT NULL,
            songId TEXT NOT NULL,
            author TEXT NOT NULL,
            album TEXT NOT NULL,
            songTime INT NOT NULL);'''.format(today))
    for index, i in enumerate(songData):
        cursor.execute('''INSERT INTO '{}' 
        (ID, songName, songId, author, album, songTime) VALUES 
        (?, ?, ?, ?, ?, ?)
        '''.format(today), (index, i['name'], i['id'], i['author'], i['album'], i['time']))
    conn.commit()
    conn.close()


def getDate():
    """
    返回当前时刻的日期(每日曲单早上6点更新)
    :return: 日期(str) 2017-11-18
    """
    now = datetime.now()
    if now.hour < 6:
        now = now + timedelta(days=-1)
    return '{}-{}-{}'.format(now.year, now.month, now.day)


# ------------------------------------------------------------------
# 播放相关
# ------------------------------------------------------------------

def playById(item):
    """
    通过id播放音乐
    :param item: 歌曲信息字典
    """
    log('Playing: {}'.format(item['name']))
    try:
        data = getDataById(item['id'])
        os.system('mpg123 -q --utf8 {}'.format(data[str(item['id'])]['url']))
    except KeyboardInterrupt:
        log('finish')


def playDaily():
    """
    随机播放每日推荐
    :return:
    """
    songData = loadDaily()
    length = len(songData)
    if length == 0:
        log('爬取不到数据')
        sys.exit()
    while True:
        item = songData[random.randint(0, length-1)]
        if not havePlayed(item['id'], length):
            break
    playById(item)


def havePlayed(songId, length):
    """
    返回今日是否播放过(True/False)
    :param songId: 歌曲id
    :param length: 今日曲单长度
    :return:
    """
    if not os.path.exists(PLAYEDTEMP):
        with open(PLAYEDTEMP, 'w', encoding='utf-8') as f:
            f.write('{}\n'.format(songId))
        return False
    with open(PLAYEDTEMP, 'r', encoding='utf-8') as f:
        temp = f.readlines()
    if '{}\n'.format(songId) not in temp:
        return False
    else:
        if len(temp) >= length:
            return False
        return True


# ------------------------------------------------------------------
# 登陆相关
# ------------------------------------------------------------------
def login(user, pwd):
    """
    登陆方法(手机号登陆)
    user: 用户名
    pwd: 密码
    return: cookies
    """
    d = {
        'csrf_token': '',
        'password': hashlib.md5(pwd.encode()).hexdigest(),
        'phone': str(user),
        'rememberLogin': 'true'
    }
    res = encryptAndPost(d, 'login_phone')
    return dict(res.cookies)


def getCookie():
    """
    读取本地Cookie, 若没有则需登录
    return: cookie
    """
    filename = os.path.join(BASEPATH, COOKIE)
    if not os.path.exists(filename):
        # 创建cookie
        log('请登陆网易云')
        user = input('username: ')
        pwd = input('password: ')
        cookie = login(user, pwd)
        saveCookie(json.dumps(cookie, ensure_ascii=False), filename)
    else:
        with open(filename, 'r', encoding='utf-8') as f:
            cookie = json.loads(f.read())
    return cookie


def saveCookie(cookie, path):
    """
    保存cookie到本地
    cookie: cookie(字符串类型)
    path: 保存位置
    """
    if os.path.exists(path):
        os.remove(path)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(cookie)


# ------------------------------------------------------------------
# 加密函数(AES, RSA)
# ------------------------------------------------------------------


def aesEncrypt(text, key):
    """
    AES加密
    text: 明文
    key: 密钥
    return: 密文
    """
    # 保证明文长度为16整数倍
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    cryptor = AES.new(key, AES.MODE_CBC, IV)
    # 返回字符串类型的密文
    return str(base64.b64encode(cryptor.encrypt(text)))[2:-1]


def rsaEncrypt(text, pubKey, modulus):
    """
    RSA加密
    text: 明文
    pubKey: 公钥
    modulus: 模
    return: 密文
    """
    pass
