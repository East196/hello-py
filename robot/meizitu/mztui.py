#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import os
import imageio


def create_gif(image_list, gif_name):
    frames = []
    for image_name in image_list:
        frames.append(imageio.imread(image_name))

    # Save them as frames into a gif
    imageio.mimsave(gif_name, frames, 'GIF', duration=0.1)
    return


from appJar import gui

app = gui()
root_path = u"e:/backup/mzitu"
gif_path = u"e:/backup/mzitugif"


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
    pic = app.getListItems("列表")[0]
    app.reloadImage("clickme", pic)


def start():
    global pics
    pics = [gif_path + "/" + pic for pic in os.listdir(gif_path)]

    app.addLabelEntry("关键词")
    app.addButton("搜索", func)
    app.enableEnter(func)

    app.addListBox("列表", [])
    app.setListBoxChangeFunction("列表", change_ren)
    func("列表")

    app.addImage("clickme", pics[0])
    app.go()


def to_gif():
    from PIL import Image
    from images2gif import writeGif

    dirs = os.listdir(root_path)
    for dir in dirs:
        pics = ["%s/%s/%s" % (root_path, dir, pic) for pic in os.listdir(root_path + "/" + dir)]

        min_x, min_y = 0, 0
        iml = []
        for key in pics:
            print key
            img = Image.open(key)
            print img
            iml.append(img)
            x, y = img.size
            min_x = min(x, min_x)
            min_y = min(y, min_y)

        niml = []
        for img in iml:
            half_the_width = img.size[0] / 2
            half_the_height = img.size[1] / 2
            min_size = min(half_the_width, half_the_height)
            img4 = img.crop(
                (
                    half_the_width - min_size,
                    half_the_height - min_size,
                    half_the_width + min_size,
                    half_the_height + min_size
                )
            )

            img4.thumbnail((250, 250))
            print img4.size
            niml.append(img4)

        gifd = root_path + 'gif/'
        gif_name = gifd + dir + ".gif"
        print niml
        niml[0].save(gif_name, save_all=True, append_images=niml[1:])
        # imageio.mimsave(gif_name, niml, 'GIF', duration=0.1)
        # create_gif(pics, gif_name)


if __name__ == '__main__':
    if not os.path.exists(gif_path):
        os.mkdir(gif_path)
        to_gif()
    start()
