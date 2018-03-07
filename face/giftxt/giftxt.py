#!/usr/bin/env python
# -*- coding: utf-8 -*-



import time

from PIL import Image, ImageSequence, ImageDraw, ImageFont


def txtlayer(base, text="Hello World!", xy=(0, 0), color="#FFFFFF"):
    # make a blank image for the text, initialized to transparent text color
    txt = Image.new('RGBA', base.size, (255, 255, 255, 0))

    # get a font
    fnt = ImageFont.truetype(u'文泉驿微米黑.ttf', 40)
    # get a drawing context
    d = ImageDraw.Draw(txt)

    # draw text, half opacity
    # d.text(xy, text, font=fnt, fill=(255, 255, 255, 255))
    d.text(xy, text, font=fnt, fill=color)
    return txt


def index(i, keys=[]):
    for key in reversed(keys):
        if i >= key:
            return key
    return i


def convert(src='source.gif', textdict={}, xy=(10, 10), color="#FFFFFF"):
    keys = sorted([int(k) for k in textdict.keys()])
    print(keys)
    with Image.open(src) as im:
        if im.is_animated:

            newframes = []
            for i, frame in enumerate(ImageSequence.Iterator(im)):
                # get an image
                base = frame.copy().convert('RGBA')

                key = index(i, keys)
                t = textdict.get(str(key), str(i))
                print(t)
                txt = txtlayer(base, t, xy, color)
                newframes.append(Image.alpha_composite(base, txt).convert("P"))

            # newframes.reverse()  # 内置列表倒序方法
            # 将倒序后的所有帧图像保存下来
            newframes[0].save('%s.out.gif' % src.replace(".gif", ""), save_all=True, append_images=newframes[1:])


def textd(src="source.txt"):
    d = {}
    with open(src) as fp:
        lines = fp.readlines()
        for line in lines:
            i, t = line.split("`")
            d[i] = t
    return d


if __name__ == '__main__':
    from appJar import gui

    app = gui()
    # app.setFont(20)
    app.setGeometry("600x600")


    def select(f):
        a = app.openBox(title="aaa", dirName=None, fileTypes=[('images', '*.gif')], asFile=True, parent=None)
        app.setEntry(u"gif文件名", a.name)
        app.setEntry(u"rule文件名", a.name.replace(".gif", ".txt"))
        im = Image.open(a.name)
        x, y = im.size
        app.setEntry(u"gif文字坐标x", x // 2)
        app.setEntry(u"gif文字坐标y", y - 60 if y > 70 else 10)
        fs = [f for f in ImageSequence.Iterator(im)]
        app.setEntry(u"gif帧数", len(fs))
        print(len(fs))


    app.startLabelFrame("gif_group", hideTitle=True)
    app.addButton(u"选择gif", select)
    app.addLabelEntry(u"gif文件名")
    app.addLabelEntry(u"gif帧数")
    app.addLabelEntry(u"gif文字坐标x")
    app.addLabelEntry(u"gif文字坐标y")
    app.setEntry(u"gif文字坐标x", "10")
    app.setEntry(u"gif文字坐标y", "10")
    app.stopLabelFrame()


    def selectcolor(f):
        color = app.colourBox(colour="#FF0000")
        print(color)
        app.setEntry(u"color", color)

    app.startLabelFrame("color_group",hideTitle=True)
    app.addButton("选择color", selectcolor)

    app.addLabelEntry(u"color")
    app.setEntry(u"color", "#FFFFFF")
    app.stopLabelFrame()

    app.addLabelEntry(u"rule文件名")


    def gene(f):
        print(f)
        giffile = app.getEntry(u"gif文件名")
        txtfile = app.getEntry(u"rule文件名")
        x = app.getEntry(u"gif文字坐标x")
        y = app.getEntry(u"gif文字坐标y")
        xy = (int(x), int(y))
        color = app.getEntry(u"color")
        convert(giffile, textd(txtfile), xy, color)
        app.infoBox("消息", "生成成功")


    app.addButton("生成", gene)

    app.go()
