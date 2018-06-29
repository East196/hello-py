#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pip install pydub

from pydub import AudioSegment
import os, re

SECONDS60 = 50 * 1000

if __name__ == '__main__':

    # 循环目录下所有文件
    for each in os.listdir('.'):
        filename = re.findall(r"(.*?)\.mp3", each)  # 取出.mp3后缀的文件名
        if filename:
            mp3 = AudioSegment.from_mp3(filename[0] + '.mp3')  # 打开mp3文件
            num = len(mp3) // SECONDS60 + 1
            for i in range(num):
                mp3[i * SECONDS60:(i + 1) * SECONDS60].export('%s.%s.mp3' % (filename[0], i), format="mp3")
