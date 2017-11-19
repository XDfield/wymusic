# -*- coding: utf-8 -*-
# Created by DoSun on 2017/11/20
# disc: 显示用的各个方法
"""
字颜色:
    30 黑K    31 红R
    32 绿G    33 黄Y
    34 蓝B    35 紫P
    36 青A    37 白W
"""

BEGIN = '\033['
END = '\033[0m'
COLOR = {
    'K': '30m', 'R': '31m',
    'G': '32m', 'Y': '33m',
    'B': '34m', 'P': '35m',
    'A': '36m', 'W': '37m'
}


def displaySongInfo(item):
    """
    显示歌曲信息
    :param item: 歌曲信息对象(dict)
    :return:
    """
    songName = dyeing(cut(item['name'].replace(u'\xa0', u' '), 20), 'G', True)
    author = dyeing(cut(item['author'].replace(u'\xa0', u' '), 20), 'G')
    album = dyeing(cut(item['album'].replace(u'\xa0', u' '), 20), 'G')
    # songTime = dyeing(str(item['time']), 'Y')
    print('{:>10}\t{}'.format(dyeing('Title:', 'R'), songName))
    print('{:>10}\t{}'.format(dyeing('Artist:', 'R'), author))
    print('{:>10}\t{}\n'.format(dyeing('Album:', 'R'), album))


def cut(msg, length=0):
    """
    裁剪信息长度
    :param msg: 待裁剪信息
    :param length: 指定长度
    :return:
    """
    if length <= 0:
        return msg
    msg_length = len(msg)
    if msg_length <= length:
        return msg
    return msg[0:(length-3)] + '...'


def dyeing(msg, color='W', highlight=False):
    """
    信息"染色"
    :param msg: 信息
    :param color: 颜色代码
    :param highlight: 是否高亮
    :return: "染色"信息
    """
    HL = '1;' if highlight else ''
    try:
        CODE = COLOR[color]
    except KeyError:
        CODE = COLOR['W']
    return BEGIN + HL + CODE + msg + END


def changeTime(microSecond):
    """
    毫秒数转正常分秒显示
    :param microSecond: 毫秒数(整数)
    :return: 分秒显示(字符串)
    """
    m, s = divmod(int(microSecond), 3600)
    h, m = divmod(m, 60)
    if h:
        return '{:2}:{:2}:{:2}'.format(h, m, s)
    else:
        return '{:2}:{:2}'.format(m, s)
