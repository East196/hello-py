# coding=utf-8
from jinja2 import Template
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class Entity(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return super(Entity, self).__str__() + " name=%s" % self.name


class ItemType(object):
    WEAPON = 0
    ARMOR = 1
    CONSUMABLE = 2
    ONLY_SEE = 3


class Item(Entity):
    def __init__(self, name, usage=ItemType.ONLY_SEE):
        super(Item, self).__init__(name)
        self.usage = usage


class Actor(Entity):
    def __init__(self, name, force=40, wit=40,speed=40, items=[]):
        super(Actor, self).__init__(name)
        self.name = name
        self.force = force
        self.wit = wit
        self.speed = speed
        self.items = items

    def hero(self):
        return False

    def npc(self):
        return False

    def master(self):
        return False

    def __str__(self):
        return super(Actor, self).__str__() + " name=%s force=%s  wit=%s" % (self.name, self.force, self.wit)


class Hero(Actor):
    def hero(self):
        return True


class Npc(Actor):
    def npc(self):
        return True


class Master(Actor):
    def master(self):
        return True


class Scene(Entity):
    def __init__(self, name, sub_scenes=[], exits=[], persons=[], description=None):
        super(Scene, self).__init__(name)
        self.sub_scenes = sub_scenes
        self.exits = exits
        self.persons = persons
        self.description = description

    def render(self):
        if self.description:
            print self.description

    def set_exits(self, exits=[]):
        for exit in exits:
            assert isinstance(exit, Scene)
        self.exits = exits


class Event(Entity):
    def __init__(self, name, scene, participants=[]):
        super(Event, self).__init__(name)
        self.name = name
        self.scene = scene
        self.participants = participants

    def fire(self):
        return "请实现Event.fire"

    def render(self):
        return "请实现Event.render"


class IntoEvent(Event):
    def __init__(self, name="进入", scene=None, participants=[]):
        super(IntoEvent, self).__init__(name, scene=scene, participants=participants)
        # self.scene.persons.append(participants[0])
        self.render()
        self.fire()

    def fire(self):
        self.meet(self.scene)
        for sub_scene in self.scene.sub_scenes:
            SeeEvent(scene=sub_scene, participants=self.participants)
        if len(self.scene.exits) == 0:
            return
        SeeEvent(scene=self.scene.exits[0], participants=self.participants)

    def meet(self, sub_scene):
        for person in sub_scene.persons:
            if person.npc() or person.master():
                MeetEvent(scene=sub_scene, participants=[self.participants[0], person])

    def render(self):
        print "%s%s%s." % (self.participants[0].name, self.name, self.scene.name)


class SeeEvent(Event):
    def __init__(self, name="望见", scene=None, participants=[]):
        super(SeeEvent, self).__init__(name, scene=scene, participants=participants)
        self.render()
        self.scene.render()
        self.fire()

    def fire(self):
        IntoEvent(scene=self.scene, participants=self.participants)

    def render(self):
        print "%s%s%s." % (self.participants[0].name, self.name, self.scene.name)


class MeetEvent(Event):
    def __init__(self, name="看见", scene=None, participants=[]):
        super(MeetEvent, self).__init__(name, scene=scene, participants=participants)
        self.render()
        self.fire()

    def fire(self):
        if self.participants[1].master():
            BeatEvent(scene=self.scene, participants=self.participants)
        if self.participants[1].npc():
            TalkEvent(scene=self.scene, participants=self.participants, topic=HelloTopic(""))

    def render(self):
        print "%s%s%s." % (self.participants[0].name, self.name, self.participants[1].name)


class BeatEvent(Event):
    def __init__(self, name="vs", scene=None, participants=[]):
        super(BeatEvent, self).__init__(name, scene=scene, participants=participants)
        self.render()
        self.fire()

    def fire(self):
        pass

    def render(self):
        print Template(u"{{ model.participants[1].name }}直扑{{ model.participants[0].name }}而来，").render(model=self)
        has_weapon = lambda item: item.usage == ItemType.WEAPON
        weapon = filter(has_weapon, self.participants[0].items)[0]
        self.weapon = weapon
        if filter(has_weapon, self.participants[0].items):
            print Template(
                u"{{ model.participants[0].name }}拿起{{ model.weapon.name }}，"
                u"狠狠的给了{{ model.participants[1].name }}一击.").render(
                model=self)
        # TODO 英雄之旅
        if self.participants[0].force > self.participants[1].force:
            print "%s%s！" % (self.participants[1].name, "疼的打了个滚，鲜血直流")
        else:
            print Template(u"{{ model.participants[1].name }}毫无知觉!").render(model=self)
        if self.participants[0].force > self.participants[1].force:
            print "%s%s%s." % (self.participants[0].name, "打死了", self.participants[1].name)
        else:
            print Template(u"{{ model.participants[0].name }}被{{ model.participants[1].name }}吃掉了!").render(model=self)


class TalkEvent(Event):
    def __init__(self, name="vs", scene=None, participants=[], topic=None):
        super(TalkEvent, self).__init__(name, scene=scene, participants=participants)
        self.topic = topic
        self.render()
        self.fire()

    def fire(self):
        pass

    def render(self):
        if isinstance(self.topic, HelloTopic):
            print Template(u"'你好，{{ model.participants[1].name }}',{{ model.participants[0].name }}说。").render(
                model=self)


class Topic(Entity):
    pass


class HelloTopic(Topic):
    pass


shaobang = Item("哨棒",usage=ItemType.WEAPON)
stone = Item("石头",usage=ItemType.WEAPON)

laohu = Master("老虎", 90, 20,items=[stone])
xiaoming = Actor("小明",items=[stone])
wusong = Hero("武松", 98, 50, items=[shaobang])
dianjia = Npc("店家")

gangshang = Scene("冈上", persons=[laohu])
jiudian = Scene("酒店", persons=[dianjia], description="门前挑着一面旗，上头写着五个字∶“三碗不过冈。”")
jingyanggang = Scene("景阳冈", sub_scenes=[jiudian], description="那岗威武雄壮！")
jingyanggang.set_exits([gangshang])
path = Scene("路上")
path.set_exits([jingyanggang])

# 加入物品机制
# 加入信念/思考机制
# 加入时间线
# 语义网？
IntoEvent(scene=path, participants=[wusong])
IntoEvent(scene=jingyanggang, participants=[xiaoming])
