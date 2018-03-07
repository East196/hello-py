#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from images2gif import writeGif

reload(sys)
sys.setdefaultencoding('utf-8')

import os

from appJar import gui

app = gui()
root_path = u"e:/backup/Downloads/mzitu"
gif_path = u"e:/backup/Downloads/mzitugif"


def func(btn):
    print btn, app.getEntry("关键词")
    global sub_pics
    sub_pics = [pic for pic in pics if app.getEntry("关键词") in pic]
    app.updateListBox("列表", sub_pics)


def show(listbox):
    print listbox
    app.reloadImage("clickme", sub_pics[0])


def change_ren(listbox):
    print listbox
    print app.getListItems("列表")
    pic = app.getListItems("列表")[0]
    app.reloadImage("clickme", pic)


def start():
    global pics
    pics = [gif_path + "/" + pic for pic in os.listdir(gif_path)]
    print pics

    app.addLabelEntry("关键词")
    app.addButton("搜索", func)
    app.enableEnter(func)

    app.addListBox("列表", [])
    func("列表")
    app.setListBoxChangeFunction("列表", change_ren)

    app.addImage("clickme", pics[0])
    app.go()


def to_gif():
    from PIL import Image
    # http://blog.csdn.net/yangalbert/article/details/7603338

    dirs = os.listdir(root_path)
    for dir in dirs:
        pics = ["%s/%s/%s" % (root_path, dir, pic) for pic in os.listdir(root_path + "/" + dir)]

        min_x, min_y = 0, 0
        iml = []
        for key in pics:
            # print key
            img = Image.open(key)
            # print img
            iml.append(img)
            x, y = img.size
            min_x = min(x, min_x)
            min_y = min(y, min_y)

        niml = []
        for img in iml:
            half_the_width = img.size[0] / 2
            half_the_height = img.size[1] / 2
            # 获得最大的正方形
            min_size = min(half_the_width, half_the_height)
            img4 = img.crop(
                (
                    half_the_width - min_size,
                    half_the_height - min_size,
                    half_the_width + min_size,
                    half_the_height + min_size
                )
            )
            # 缩放
            img4.thumbnail((250, 250))
            # print img4.size
            niml.append(img4)
        # TODO 根据长宽和颜色对niml分割

        gifd = root_path + 'gif/'
        gif_name = gifd + dir + ".gif"
        for nim in niml:
            nim.info["duration"] = 200
        print niml[0].info
        # writeGif(gif_name, niml)
        niml[0].save(gif_name, save_all=True, append_images=niml[1:])
        # imageio.mimsave(gif_name, niml, 'GIF', duration=0.1)
        # create_gif(pics, gif_name)


if __name__ == '__main__':
    if not os.path.exists(gif_path):
        os.makedirs(gif_path)
    # to_gif()
    start()
