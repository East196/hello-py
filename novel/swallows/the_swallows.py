# coding=utf-8
#!/usr/bin/env python

import sys
from os.path import realpath, dirname, join

# get the ../src/ directory onto the Python module search path
sys.path.insert(0, join(dirname(realpath(sys.argv[0])), '..', 'src'))

# now we can import things, like:
from novel.swallows import Publisher

# 在world中构建了整个世界
from novel.swallows.story import alice, bob, house

# 出发点在于人
### main ###
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


# TODO 提取蜀山剑侠传中所有的人名、地名、法宝名
# TODO 根据上下文判定人物相性、正邪度