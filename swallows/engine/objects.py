# coding=utf-8
import random

from swallows.engine.events import Event


# ## TOPICS主题 ## #

# 主题是人物最近说的事情.  也可以是其他角色做的任何事。

class Topic(object):
    def __init__(self, originator, subject=None):
        self.originator = originator
        self.subject = subject


# 打招呼
class GreetTopic(Topic):
    pass


# 演讲
class SpeechTopic(Topic):
    pass


# 提问，议题
class QuestionTopic(Topic):
    pass


# ## BELIEFS 信念 ## #
#
# 信仰是一个栩栩如生的相信。它们有几种类型：
#
# -一个信念，一个对象的某个地方
# -因为他们在那里看到了它（记忆）
# 因为其他角色告诉他们这是那里
# -认为他们应该做些什么（目标），具有亚型：
# -一个信念，一个对象是可取的和他们应该得到它
# -一个信念，应该做点什么事（平淡，一般）
# -相信另一个动画相信的东西
#
# 当然，任何特定的信仰可能不是真的
#
# 真的是抱有一个信念。。。
# 这是个抽象类
class Belief(object):
    # 所有子类的构造函数应该接受这类
    # 称只有一个参数，一个事方便排序
    # 为beliefset.get和去除，这真的不在乎任何事情
    # 关于信仰的除了它的类和它的主题。
    # 虽然，通常，你想传递多个参数时
    # 制作通过beliefset.add真正的信仰。（像泥一样干净，对吧？）
    def __init__(self, subject):  # kind of silly for an ABC to have a
        assert isinstance(subject, Actor)  # constructor, but it is to emphasize
        self.subject = subject  # that all beliefs have a subject,
        # which is the thing we believe
        # something about

    def __str__(self):
        raise NotImplementedError


class ItemLocation(Belief):  # 从前的“记忆”
    def __init__(self, subject, location=None, informant=None, concealer=None):
        assert isinstance(subject, Actor)
        assert isinstance(location, Actor) or location is None
        self.subject = subject  # 东西我们认为在某个地方
        self.location = location  # 我们认为在某个地方
        self.informant = informant  # 报告者，告诉我们的角色
        self.concealer = concealer  # 隐藏者，隐藏物品的角色

    def __str__(self):
        s = "%s 在 %s 里" % (
            self.subject.render(),
            self.location.render()
        )

        # 遮住
        if self.concealer:
            s += " (被 %s 藏起来了)" % self.concealer.render()
        # 告密
        if self.informant:
            s += " (%s 告诉我说)" % self.informant.render()
        return s


# 目标
class Goal(Belief):
    def __init__(self, subject, phrase=None):
        assert isinstance(subject, Actor)
        self.subject = subject  # 我们想做的事情
        self.phrase = phrase  # 人类可读的描述

    def __str__(self):
        return "我应该 %s %s" % (
            self.phrase,
            self.subject.render()
        )


# 欲望
class Desire(Goal):
    def __init__(self, subject):
        assert isinstance(subject, Actor)
        self.subject = subject  # 我们想要获得的东西

    def __str__(self):
        return "我想要 %s" % (
            self.subject.render()
        )


# oh dear 坚信的信念
class BeliefsBelief(Belief):
    def __init__(self, subject, belief_set=None):
        assert isinstance(subject, Animate)
        self.subject = subject  # 保持信念的驱动
        if belief_set is None:
            belief_set = BeliefSet()
        assert isinstance(belief_set, BeliefSet)
        self.belief_set = belief_set  # 持有的信念

    def __str__(self):
        return "%s 坚信 { %s }" % (
            self.subject.render(),
            self.belief_set
        )


# 信念的集合
class BeliefSet(object):
    """
    一个beliefset对象像Python set()，但有
    以下限制：
    对于一种特定的信仰，只有一种信仰。
    集合中的项目。
    所以这真的是一个从演员到地图和信仰的地图。
    信念子类。
    但让我们（至少我）把它作为一个集。
    （此外，它可能会改变。）

    """

    def __init__(self):
        self.belief_map = {}

    def add(self, belief):
        assert isinstance(belief, Belief)
        subject = belief.subject
        self.belief_map.setdefault(subject, {})[belief.__class__] = belief

    def remove(self, belief):
        # 特定的信念传递给我们的并不是真正的问题。我们提取类和物体，
        # 返回我们可能任何现有的信念
        assert isinstance(belief, Belief)
        subject = belief.subject
        beliefs = self.belief_map.setdefault(subject, {})
        if belief.__class__ in beliefs:
            del beliefs[belief.__class__]

    def get(self, belief):
        # the particular belief passed to us doesn't really matter.  we extract
        # the class and subject and return any existing belief we may have
        assert isinstance(belief, Belief)
        subject = belief.subject
        return self.belief_map.setdefault(subject, {}).get(
            belief.__class__, None
        )

    def subjects(self):
        for subject in self.belief_map:
            yield subject

    def beliefs_for(self, subject):
        beliefs = self.belief_map.setdefault(subject, {})
        for class_ in beliefs:
            yield beliefs[class_]

    def beliefs_of_class(self, class_):
        for subject in self.subjects():
            for belief in self.beliefs_for(subject):
                if belief.__class__ == class_:
                    yield belief

    def __str__(self):
        l = []
        for subject in self.subjects():
            for belief in self.beliefs_for(subject):
                l.append(str(belief))
        return ', '.join(l)


# ## ACTORS (objects in the world) 角色（世界中的物体） ## #
class Actor(object):
    def __init__(self, name, location=None, owner=None, collector=None):
        self.name = name
        self.collector = collector
        self.contents = set()
        self.enter = ""
        self.owner = owner
        self.location = None
        if location is not None:
            self.move_to(location)

    # 值得注意的
    def notable(self):
        return self.treasure() or self.weapon() or self.animate() or self.horror()

    # 财宝
    def treasure(self):
        return False

    # 武器
    def weapon(self):
        return False

    # 惊骇
    def horror(self):
        return False

    def takeable(self):
        return False

    # 有生命的
    def animate(self):
        return False

    # 容器
    def container(self):
        return False

    # 冠词
    def article(self):
        return '那个'

    # 所有格 possessive
    def possessive(self):
        return "它"

    # 宾格
    def accusative(self):
        return "它"

    #  代词
    def pronoun(self):
        return "它"

    # 过去是
    def was(self):
        return "过去是"

    # 是
    def is_(self):
        return "是"

    # 发出事件
    def emit(self, *args, **kwargs):
        if self.collector:
            self.collector.collect(Event(*args, **kwargs))

    def move_to(self, location):
        if self.location:
            self.location.contents.remove(self)
        self.location = location
        self.location.contents.add(self)

    def render(self, event=None):
        """
        在上下文中返回包含我们称之为这个对象的字符串给定事件（可能是没有），
        以获得一个“通用”描述。
        """
        name = self.name
        repl = None
        if self.owner is not None:
            repl = self.owner.render() + "的"
        if event:
            if event.speaker is self.owner:
                repl = '我'
            elif event.addressed_to is self.owner:
                repl = '你'
            elif event.initiator() is self.owner:
                repl = event.initiator().possessive()
        if repl is not None:
            name = name.replace('<*>', repl)
        article = self.article()
        if not article:
            return name
        return '%s %s' % (article, name)

    def indefinite(self):
        article = '一个'
        return '%s %s' % (article, self.name)


# ## 一些用于 Actors 的mixins  ## #

# 适应性
class ProperMixin(object):
    # 文章
    def article(self):
        return ''


# 复数的
class PluralMixin(object):
    # 主语
    def posessive(self):
        return "他们"

    # 宾语
    def accusative(self):
        return "他们"

    # 代词
    def pronoun(self):
        return "他们"

    # 不定数量
    def indefinite(self):
        article = '一些'
        return '%s %s' % (article, self.name)

    # 是（过去）
    def was(self):
        return "过去是"

    # 是
    def is_(self):
        return "是"


# 男
class MasculineMixin(object):
    def posessive(self):
        return "他"

    def accusative(self):
        return "他"

    def pronoun(self):
        return "他"


# 女
class FeminineMixin(object):
    def posessive(self):
        return "她"

    def accusative(self):
        return "她"

    def pronoun(self):
        return "她"


# ## ANIMATE OBJECTS 有生命的物体，动物 ## #
class Animate(Actor):
    def __init__(self, name, location=None, owner=None, collector=None):
        Actor.__init__(
            self, name, location=location, owner=owner, collector=None
        )
        self.topic = None
        self.beliefs = BeliefSet()

    def animate(self):
        return True

    # for debugging，打印信念
    def dump_beliefs(self):
        for subject in self.beliefs.subjects():
            for belief in self.beliefs.beliefs_for(subject):
                print ".oO{ %s }" % belief

    # ##--- 信念的存取修改 ---## #

    # 大多是用于访问BeliefSet的别名.

    def remember_location(self, thing, location, concealer=None):
        """更新这个Animate的信念，包括一个信念，即
        给定的东西位于指定的位置。
        真的只是一个可读的别名believe_location。
        """
        self.believe_location(thing, location, informant=None, concealer=concealer)

    def believe_location(self, thing, location, informant=None, concealer=None):
        """
        更新这个动画的信念，包括一个信念，即给定的东西位于指定的位置。
        他们可能有有人告诉过我。
        """
        self.beliefs.add(ItemLocation(
            thing, location, informant=informant, concealer=concealer
        ))

    def recall_location(self, thing):
        """返回一个itemlocation（信仰）这件事，或者没有。"""
        return self.beliefs.get(ItemLocation(thing))

    def forget_location(self, thing):
        self.beliefs.remove(ItemLocation(thing))

    def desire(self, thing):
        self.beliefs.add(Desire(thing))

    # 终止渴望
    def quench_desire(self, thing):
        # 通常称为当它已经获得
        self.beliefs.remove(Desire(thing))

    def does_desire(self, thing):
        if thing.treasure():
            return True  # omg YES
        if thing.weapon():
            return True  # could come in handy.
        # 动物对财宝和兵器感兴趣...中外一致啊
        # (TODO, sophisticate this?搞复杂点如何？)
        return self.beliefs.get(Desire(thing)) is not None

    def believed_beliefs_of(self, other):
        """
        返回一个这个动物相信其他动物持有的信念集。
        通常你会操纵这beliefset直接添加、删除、获取等。
        """
        assert isinstance(other, Animate)
        # for extra fun, try reading the code of this method out loud!
        beliefs_belief = self.beliefs.get(BeliefsBelief(other))
        if beliefs_belief is None:
            beliefs_belief = BeliefsBelief(other, BeliefSet())
            self.beliefs.add(beliefs_belief)
        return beliefs_belief.belief_set

    ###--- topic stuff ---###

    def address(self, other, topic, phrase, participants=None):
        if participants is None:
            participants = [self, other]
        other.topic = topic
        self.emit(phrase, participants, speaker=self, addressed_to=other)

    def greet(self, other, phrase, participants=None):
        self.address(other, GreetTopic(self), phrase, participants)

    def speak_to(self, other, phrase, participants=None, subject=None):
        self.address(other, SpeechTopic(self, subject=subject), phrase, participants)

    def question(self, other, phrase, participants=None, subject=None):
        self.address(other, QuestionTopic(self, subject=subject), phrase, participants)

    # ##--- generic actions 通用动作 ---## #
    # 出现在某地
    def place_in(self, location):
        """
        像move_to但安静。用于设置场景等。
        """
        if self.location is not None:
            self.location.contents.remove(self)
        self.location = location
        self.location.contents.add(self)
        # 这是必要的，让编辑知道字符开始。
        # 编辑应当清除所有无法提供信息给读者的实例。
        self.emit("<1> <was-1> 在 <2>", [self, self.location])
        # FIXME 下面的代码有个副作用，如果他们开始在一个恐怖位置，他们可能会没有反应。
        for x in self.location.contents:
            if x == self:
                continue
            if x.notable():  # 值得注意的
                self.emit("<1> 注意到 <2>", [self, x])
                self.remember_location(x, self.location)

    # 移动至某地
    def move_to(self, location):
        assert (location != self.location)
        assert (location is not None)
        for x in self.location.contents:
            # 否则我们就会说 Bob看着Bob离开房间，嗯？
            if x is self:
                continue
            if x.animate():
                x.emit("<1> 看到 <2> 离开了 %s" % x.location.noun(), [x, self])
        if self.location is not None:
            self.location.contents.remove(self)
        previous_location = self.location
        self.location = location
        assert self not in self.location.contents
        self.location.contents.add(self)
        self.emit("<1> 进入 <2>", [self, self.location],
                  previous_location=previous_location)

    # 指向
    def point_at(self, other, item):
        # 如果有办法显示左轮手枪为主题，将部分是好的，或以其他方式表明，语境为“枪口”
        assert self.location == other.location
        assert item.location == self
        self.emit("<1> 拿 <3> 指着 <2>",
                  [self, other, item])
        for actor in self.location.contents:
            if actor.animate():
                actor.remember_location(item, self)

    # 放下
    def put_down(self, item):
        assert (item.location == self)
        self.emit("<1> 放下 <2>", [self, item])
        item.move_to(self.location)
        for actor in self.location.contents:
            if actor.animate():
                actor.remember_location(item, self.location)

    # 捡起
    def pick_up(self, item):
        assert (item.location == self.location)
        self.emit("<1> 捡起 <2>", [self, item])
        item.move_to(self)
        for actor in self.location.contents:
            if actor.animate():
                actor.remember_location(item, self)

    # 交给
    def give_to(self, other, item):
        assert (item.location == self)
        assert (self.location == other.location)
        self.emit("<1> 把 <3> 交给 <2>", [self, other, item])
        item.move_to(other)
        for actor in self.location.contents:
            if actor.animate():
                actor.remember_location(item, other)

    # 散步
    def wander(self):
        self.move_to(
            self.location.exits[
                random.randint(0, len(self.location.exits) - 1)
            ]
        )

    #
    def live(self):
        """
        每个回合都会调用一个动画动作。
        你需要实现这个特定的动作。
        """
        raise NotImplementedError(
            '请实现 %s.live()' % self.__class__.__name__
        )


# 男性角色
class Male(MasculineMixin, ProperMixin, Animate):
    pass


# 女性角色
class Female(FeminineMixin, ProperMixin, Animate):
    pass


### LOCATIONS ###

class Location(Actor):
    def __init__(self, name, enter="来到", noun="房间", owner=None):
        self.name = name
        self.enter = enter
        self.contents = set()
        self.exits = []
        self.noun_ = noun
        self.owner = owner

    def noun(self):
        return self.noun_

    def set_exits(self, *exits):
        for exit in exits:
            assert isinstance(exit, Location)
        self.exits = exits


# 特有位置
class ProperLocation(ProperMixin, Location):
    pass


# ## OTHER INANIMATE OBJECTS 静态物品 ## #

# 物品
class Item(Actor):
    def takeable(self):
        return True


# 武器
class Weapon(Item):
    def weapon(self):
        return True


# 容器
class Container(Actor):
    def container(self):
        return True


# 独特的容器
class ProperContainer(ProperMixin, Container):
    pass


# 财宝
class Treasure(Item):
    def treasure(self):
        return True


# 很多财宝
class PluralTreasure(PluralMixin, Treasure):
    pass


# 恐怖的东西
class Horror(Actor):
    def horror(self):
        return True
