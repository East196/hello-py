# coding=utf-8

import random

from swallows.engine.objects import (
    Location, ProperLocation, Treasure, PluralTreasure,
    Container, ProperContainer,
    Item, Weapon, Horror
)
from swallows.story.characters import MaleCharacter, FemaleCharacter

# 世界：
# 更多反应的尸体：
# -如果他们同意，采取一对一的行动
# 协议后：
# 呼叫警察（他们有一个座机？这可能是娱乐性的。
# 如果他们共享两者之间的一个移动电话）
# -我要介绍一个新角色…侦探。佑。
# 试图处理它…他们试图把它拖到…花园吗？
# 我要添加一个花园。还有铲子。
# 在地下室一种说不出的东西！（他们没有足够的兴奋吗？
# 他们的生活吗？）
# 子弹的左轮手枪

# ## world ## #
# 角色
alice = FemaleCharacter('爱丽丝')
bob = MaleCharacter('波波')

# 位置
kitchen = Location('厨房')
living_room = Location('客厅')
dining_room = Location('餐厅')
front_hall = Location('前走廊')
driveway = Location('车道', noun="车道")
garage = Location('车库', noun="车库")
path_by_the_shed = Location('去小屋的路', noun="路")
shed = Location('小屋', noun="小屋")
upstairs_hall = Location('楼梯')
study = Location('书房')
bathroom = Location('浴室')

# 特有位置
bobs_bedroom = ProperLocation("<*> 卧室", owner=bob)
alices_bedroom = ProperLocation("<*> 卧室", owner=alice)

# 联通设置
kitchen.set_exits(dining_room, front_hall)
living_room.set_exits(dining_room, front_hall)
dining_room.set_exits(living_room, kitchen)
front_hall.set_exits(kitchen, living_room, driveway, upstairs_hall)
driveway.set_exits(front_hall, garage, path_by_the_shed)
garage.set_exits(driveway)
path_by_the_shed.set_exits(driveway, shed)
shed.set_exits(path_by_the_shed)
upstairs_hall.set_exits(bobs_bedroom, alices_bedroom, front_hall, study, bathroom)
bobs_bedroom.set_exits(upstairs_hall)
alices_bedroom.set_exits(upstairs_hall)
study.set_exits(upstairs_hall)
bathroom.set_exits(upstairs_hall)

# 房屋集合
house = (kitchen, living_room, dining_room, front_hall, driveway, garage,
         upstairs_hall, bobs_bedroom, alices_bedroom, study, bathroom,
         path_by_the_shed, shed)

# 财宝
falcon = Treasure('黄金猎鹰', location=dining_room)
jewels = PluralTreasure('偷来的宝石', location=garage)

# 容器
cupboards = Container('碗柜', location=kitchen)
liquor_cabinet = Container('酒柜', location=dining_room)
mailbox = Container('邮箱', location=driveway)
# 特有容器
bobs_bed = ProperContainer("<*> 床", location=bobs_bedroom, owner=bob)
alices_bed = ProperContainer("<*> 床", location=alices_bedroom, owner=alice)

# 物品 白兰地
brandy = Item('白兰地酒瓶', location=liquor_cabinet)
# 武器 手枪
revolver = Weapon('左轮手枪', location=random.choice([bobs_bed, alices_bed]))
# 吓人的 死尸
dead_body = Horror('死尸', location=bathroom)

# 当创建爱丽丝和鲍伯时，我们让他们认识到他们在世界某些重要的对象
# 默认这两个角色都知道关键事件
for c in (alice, bob):
    c.configure_objects(
        revolver=revolver,
        brandy=brandy,
        dead_body=dead_body,
    )

ALL_ITEMS = (falcon, jewels, revolver, brandy)
