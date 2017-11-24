# coding=utf-8
# !/usr/bin/env python

# swallows 信以为真的
import sys
from os.path import realpath, dirname, join

# 把 ../src/ 文件夹加入python模块搜索路径
sys.path.insert(0, join(dirname(realpath(sys.argv[0])), '..', 'src'))


from novel.swallows import Publisher

# 在world中构建了整个世界
from novel.swallows import alice, bob, house

# 出发点在于人
# ## 主体 ## #
publisher = Publisher(
    # 两个人
    characters=(alice, bob),
    # house是个元组，代表所有房子
    setting=house,
    # 文章标题
    title="十里坡",
    # 是不是要加入环境和描述等额外的转换器
    friffery=True,
    # debug=True,
    # 章节数
    chapters=1,
    events_per_chapter=200
)
publisher.publish()



