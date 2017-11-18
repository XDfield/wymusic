# -*- coding: utf-8 -*-
# Created by DoSun on 2017/11/18
from setuptools import setup

setup(
    name='wymusic',
    version='1.0.0',
    author='DoSun',
    author_email='chenxuan958864951@qq.com',
    description='play daily recommend music in cloudmusic.',
    packages=['wymusic'],
    package_data={
        'wymusic': ['*.exe']
    },
    url='https://github.com/XDfield/wymusic',
    zip_safe=False,
    install_requires=[
        'requests',
    ],
    entry_points={
      'console_scripts': [
          'wymusic=wymusic.wymusic:main'
        ],
    })
