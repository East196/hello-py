#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageFont, ImageFilter

import random

im = Image.open('F:/workspace/python/data/backpink.jpg')
im2 = im.filter(ImageFilter.BLUR)
im2.save('F:/workspace/python/data/backpink_blur.png', 'png')
im2.save('F:/workspace/python/data/backpink_blur.jpg', 'jpeg')


# 随机字母:
def random_char():
    return chr(random.randint(65, 90))


# 随机颜色1:
def random_color():
    return random.randint(64, 255), random.randint(64, 255), random.randint(64, 255)


# 随机颜色2:
def random_color2():
    return random.randint(32, 127), random.randint(32, 127), random.randint(32, 127)


# 240 x 60:
width = 60 * 4
height = 60
image = Image.new('RGB', (width, height), (255, 255, 255))
# 创建Font对象:
font = ImageFont.truetype('C:/Windows/Fonts/Arial.ttf', 36)
# 创建Draw对象:
draw = ImageDraw.Draw(image)
# 填充每个像素:
for x in range(width):
    for y in range(height):
        draw.point((x, y), fill=random_color())
# 输出文字:
for t in range(4):
    draw.text((60 * t + 10, 10), random_char(), font=font, fill=random_color2())
# 模糊:
image = image.filter(ImageFilter.BLUR)
image.save('code.jpg', 'jpeg')
print(image.format, image.size, image.mode)
# image.show()
