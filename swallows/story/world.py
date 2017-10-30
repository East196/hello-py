# coding=utf-8

import random

from swallows.engine.objects import (
    Location, ProperLocation, Treasure, PluralTreasure,
    Container, ProperContainer,
    Item, Weapon, Horror
)
from swallows.story.characters import MaleCharacter, FemaleCharacter

# TODO

# World:
# more reacting to the dead body:
# - if they *agree*, take one of the courses of action
# after agreement:
# - calling the police (do they have a landline?  it might be entertaining
#   if they share one mobile phone between the both of them)
#   - i'll have to introduce a new character... the detective.  yow.
# - trying to dispose of it... they try to drag it to... the garden?
#   i'll have to add a garden.  and a shovel.
# an unspeakable thing in the basement!  (don't they have enough excitement
#   in their lives?)
# bullets for the revolver

### world ###
# 角色
alice = FemaleCharacter('店家')
bob = MaleCharacter('武松')

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

# when making alice and bob, we let them recognize certain important
# objects in their world
# 默认这两个角色都知道关键事件
for c in (alice, bob):
    c.configure_objects(
        revolver=revolver,
        brandy=brandy,
        dead_body=dead_body,
    )

ALL_ITEMS = (falcon, jewels, revolver, brandy)
