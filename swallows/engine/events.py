# coding=utf-8
import random
import sys


# 用语：
# 使用通行证的艺术时，他们的记忆中没有一个项目，他们看到
# -戏剧反讽将是非常好的，但很难拔出。嗯，某个
# 量自然发生的现在，角色POV。但还可以做更多的事情。
# ”3章。_in鲍伯隐藏偷来的珠宝在信箱里，etc_”
# 即章总结——这有点太花哨的希望，但
# 足够聪明的编辑就可以了

# EVENTS 事件 #

class Event(object):
    def __init__(self,
                 phrase,  # 措辞，对事件的描述
                 participants,  # 参与者列表
                 excl=False,  # 感叹号
                 previous_location=None,  # 上一个地址
                 speaker=None,  # 说话者
                 addressed_to=None,  # 到达地址
                 exciting=False):  # 令人激动的
        """
        participants[0]一直作为发起人, 并且记录事件发生的位置.
        现在，我们假设这样的事件可以：
        -每个角色在那个位置观察
        -只影响该位置的角色

        在未来，我们可能拥有：
        -主动参与者和被动参与者
        -积极参与者必须在场
        -被动参与者不必
        （可能通过传递n个数字：第一个n）
        参与者应该被认为是积极的）

        说话者和addressed_to应用于对话。
        如果说话者为None，则意味着叙述者在说话。
        如果addressed_to为None，这意味着读者在听。
        """
        self.phrase = phrase
        self.participants = participants
        self.location = participants[0].location
        self._previous_location = previous_location
        self.excl = excl
        self.speaker = speaker
        self.addressed_to = addressed_to
        self.exciting = exciting

    # 改述
    def rephrase(self, new_phrase):
        """
        不修改事件。返回一个新副本。
        返回不可变变量
        """
        return Event(new_phrase, self.participants, excl=self.excl)

    # 发起者
    def initiator(self):
        return self.participants[0]

    # 上个位置
    def previous_location(self):
        return self._previous_location

    # 渲染文中的变量
    def render(self):
        phrase = self.phrase
        i = 0
        for participant in self.participants:
            phrase = phrase.replace('<%d>' % (i + 1), participant.render(event=self))
            phrase = phrase.replace('<indef-%d>' % (i + 1), participant.indefinite())
            phrase = phrase.replace('<his-%d>' % (i + 1), participant.possessive())
            phrase = phrase.replace('<him-%d>' % (i + 1), participant.accusative())
            phrase = phrase.replace('<he-%d>' % (i + 1), participant.pronoun())
            phrase = phrase.replace('<was-%d>' % (i + 1), participant.was())
            phrase = phrase.replace('<is-%d>' % (i + 1), participant.is_())
            i += 1
        return phrase

    # 事件的全量描述
    def __str__(self):
        phrase = self.render()
        # 是否值得惊叹。。。
        if self.excl:
            phrase += '!\n'
        else:
            phrase += '.\n'
        # 首字母大写
        return phrase[0].upper() + phrase[1:]


# 集合事件
class AggregateEvent(Event):
    """
    尝试将多个事件组合成单个事件的方法
    句子。每个构成事件必须具有相同的启动器。
    这绝对不是它所能做到的那样好。
    """

    def __init__(self,
                 template,  # 模板
                 events,  # 事件列表
                 excl=False):  # 感叹号
        self.template = template
        self.events = events
        self.excl = excl
        self.phrase = '请看子事件'
        self._initiator = self.events[0].initiator()  # 使用第一事件的发起人作为集合事件发起人
        # 确定所有事件的发起人是同一人
        for event in self.events:
            assert event.initiator() == self._initiator
        self.location = self._initiator.location

    def rephrase(self, new_phrase):
        # raise NotImplementedError
        return self

    def initiator(self):
        return self._initiator

    def previous_location(self):
        return self.events[0].previous_location()

    def __str__(self):
        phrase = self.template % tuple([x.render() for x in self.events])
        if self.excl:
            phrase += '!\n'
        else:
            phrase += '.\n'
        return phrase[0].upper() + phrase[1:]


# 事件收集器
class EventCollector(object):
    def __init__(self):
        self.events = []

    def collect(self, event):
        # 重复事件
        if self.events and str(event) == str(self.events[-1]):
            raise ValueError('重复事件: %s' % event)
        #
        if event.phrase == '<1> 走到 <2>':
            assert event.previous_location() is not None
            assert event.previous_location() != event.location
        self.events.append(event)


# 不需要, 让 emit() 就可以
class Oblivion(EventCollector):
    def collect(self, event):
        pass


oblivion = Oblivion()


# ## EDITOR AND PUBLISHER 编辑器和发布器 ## #

class Editor(object):
    """
    编辑是在编译的_peephole optimizer_非常相似。
    与其用更有效但语义上等价的指令序列代替指令序列，
    不如用更易读、语义相等的句子序列代替句子序列。
    编辑还负责把句子的顺序分成“合理的”段落。
    （这可能是像一个编译器的代码重写通过插入NOP指令，保证在一个字的边界，或诸如此类的。）
    编辑器还负责挑选要跟随的字符。（我不认为有编译器构造的类比。）
    注意，事件流必须以“角色在某个位置”开头。否则编辑不知道是谁开始的。
    其实他像个编译器
    """

    def __init__(self, collector, main_characters):
        # 事件倒序？
        self.events = list(reversed(collector.events))
        self.main_characters = main_characters
        self.pov_index = 0
        self.transformers = []
        # ( omnisciently 全知全能合理系统) 所有角色的位置
        self.character_location = {}
        # 所有角色的上一位置
        self.last_seen_at = {}
        # 当没有旁白的时候把角色放入事件？
        self.exciting_developments = {}

    def add_transformer(self, transformer):
        self.transformers.append(transformer)

    def publish(self):
        paragraph_num = 1  # 段落编号
        while len(self.events) > 0:
            pov_actor = self.main_characters[self.pov_index]
            # 生成段落事件
            paragraph_events = self.generate_paragraph_events(pov_actor)
            for transformer in self.transformers:
                if paragraph_events:
                    # 段落事件全部转换？
                    paragraph_events = transformer.transform(
                        self, paragraph_events, paragraph_num
                    )
            # 发布段落事件
            self.publish_paragraph(paragraph_events)
            # 下一个角色。。。没有关联的么？如何关联？
            self.pov_index += 1
            if self.pov_index >= len(self.main_characters):
                self.pov_index = 0
            paragraph_num += 1

    def generate_paragraph_events(self, pov_actor):
        # 限定10到25句
        quota = random.randint(10, 25)
        paragraph_events = []
        while len(paragraph_events) < quota and len(self.events) > 0:
            event = self.events.pop()

            if not paragraph_events:
                # 这是段落的第一句
                # 如果读者没有意识到他们在这里，添加一个事件
                # 没有第一句就造个第一句
                if self.last_seen_at.get(pov_actor, None) != event.location:
                    if not ('走到' in event.phrase) and not (event.phrase == '<1> <was-1> 在 <2>'):
                        paragraph_events.append(Event('<1> <was-1> 在 <2>', [pov_actor, event.location]))
                # 如果有令人激动的事件，告诉读者，添加入段落事件并置空自己
                for (obj, loc) in self.exciting_developments.get(pov_actor, []):
                    # 谁在哪发现了谁？
                    paragraph_events.append(Event('<1> 发现 <2> 在 <3>', [pov_actor, obj, loc]))
                self.exciting_developments[pov_actor] = []

            # 更新我们的想法的角色是，即使这些不是我们将倾倒的事件
            # 事件发起者的位置更新
            self.character_location[event.initiator()] = event.location

            if event.location == self.character_location[pov_actor]:
                paragraph_events.append(event)
                # 更新读者知道的角色
                self.last_seen_at[event.initiator()] = event.location
            else:
                if event.exciting:
                    self.exciting_developments.setdefault(event.initiator(), []).append(
                        (event.participants[1], event.participants[2])
                    )

        return paragraph_events

    # 发布段落
    def publish_paragraph(self, paragraph_events):
        for event in paragraph_events:
            sys.stdout.write(str(event) + "  ")


# 转换器
class Transformer(object):
    pass


class DeduplicateTransformer(Transformer):
    # 检查逐字重复。
    # 这可能是“危险的”，
    # 如果你有两个字符，Bob Jones和Bob Smith，两个都被命名为“鲍勃”，
    # 它们实际上是两个不同的事件…但…现在，这是一个边缘案例。
    def transform(self, editor, incoming_events, paragraph_num):
        events = []
        for event in incoming_events:
            if events:
                if str(event) == str(events[-1]):
                    events[-1].phrase = event.phrase + ', 两次'
                elif str(event.rephrase(event.phrase + ', 两次')) == str(events[-1]):
                    events[-1].phrase = event.phrase + ', 很多次'
                elif str(event.rephrase(event.phrase + ', 很多次')) == str(events[-1]):
                    pass
                else:
                    events.append(event)
            else:
                events.append(event)
        return events


# 使用代词转换器
class UsePronounsTransformer(Transformer):
    # 用代词取代重复的专有名词
    def transform(self, editor, incoming_events, paragraph_num):
        events = []
        for event in incoming_events:
            if events:
                if event.initiator() == events[-1].initiator():
                    event.phrase = event.phrase.replace('<1>', '<he-1>')
                events.append(event)
            else:
                events.append(event)
        return events


# 导航
class MadeTheirWayToTransformer(Transformer):
    def transform(self, editor, incoming_events, paragraph_num):
        events = []
        for event in incoming_events:
            if events and event.initiator() == events[-1].initiator():
                if (events[-1].phrase in ('<1> 走到 <2>',) and
                            event.phrase == '<1> 走到 <2>'):
                    assert event.location == event.participants[1]
                    assert events[-1].previous_location() is not None
                    assert events[-1].location == events[-1].participants[1]
                    events[-1].phrase = '<1> 找到去 <2> 的路'
                    events[-1].participants[1] = event.participants[1]
                    events[-1].location = event.participants[1]
                elif (events[-1].phrase in ('<1> 找到去 <2> 的路',) and
                              event.phrase == '<1> 走到 <2>'):
                    assert event.location == event.participants[1]
                    assert events[-1].previous_location() is not None
                    assert events[-1].location == events[-1].participants[1]
                    events[-1].phrase = '<1> 找到去 <2> 的路'
                    events[-1].participants[1] = event.participants[1]
                    events[-1].location = event.participants[1]
                else:
                    events.append(event)
            else:
                events.append(event)
        return events


# well well well
from swallows.engine.objects import Actor

weather = Actor('天气')


# 添加天气的转换器
class AddWeatherFrifferyTransformer(Transformer):
    def transform(self, editor, incoming_events, paragraph_num):
        events = []
        if paragraph_num == 1:
            choice = random.randint(0, 3)
            if choice == 0:
                events.append(Event("下雨了！！！", [weather]))
            if choice == 1:
                events.append(Event("雪花飘飘", [weather]))
            if choice == 2:
                events.append(Event("阳光四射", [weather]))
            if choice == 3:
                events.append(Event("天空阴沉", [weather]))
        return events + incoming_events


# 添加段落开始转换器
class AddParagraphStartFrifferyTransformer(Transformer):
    def transform(self, editor, incoming_events, paragraph_num):
        first_event = incoming_events[0]
        if paragraph_num == 1:
            return incoming_events
        if str(first_event).startswith("'"):
            return incoming_events
        if " 已经找到了 " in str(first_event):
            return incoming_events
        if " 刚刚在 " in str(first_event):
            return incoming_events
        choice = random.randint(0, 8)
        if choice == 0:
            first_event = first_event.rephrase(
                "过了一会儿, " + first_event.phrase
            )
        if choice == 1:
            first_event = first_event.rephrase(
                "突然, " + first_event.phrase
            )
        if choice == 2:
            first_event = first_event.rephrase(
                "考虑了一会儿, " + first_event.phrase
            )
        if choice == 3:
            first_event = first_event.rephrase(
                "有点焦急, " + first_event.phrase
            )
        return [first_event] + incoming_events[1:]


# 组合事件的转换器
class AggregateEventsTransformer(Transformer):
    # 简单衔接
    def transform(self, editor, incoming_events, paragraph_num):
        events = []
        for event in incoming_events:
            if events:
                if (event.initiator() == events[-1].initiator() and
                            events[-1].phrase in ('<1> 走向 <2>',) and
                            event.phrase in ('<1> 看到 <2>',)):
                    event.phrase = event.phrase.replace('<1>', '<he-1>')
                    events[-1] = AggregateEvent(
                        "%s, 当 %s 的时候", [events[-1], event],
                        excl=event.excl)
                else:
                    events.append(event)
            else:
                events.append(event)
        return events


# 侦查闲逛
class DetectWanderingTransformer(Transformer):
    # 还没用到
    # 导航到原地...
    def transform(self, editor, incoming_events, paragraph_num):
        events = []
        for event in incoming_events:
            if event.phrase == '<1> 找到去 <2> 的路' and event.location == event.previous_location():
                event.phrase = '<1> 在附近转了转, 然后回到 <2>'
            events.append(event)
        return events


# 发布器
class Publisher(object):
    def __init__(self,
                 characters=(),
                 setting=(),
                 friffery=False,
                 debug=False,
                 title='无标题',
                 chapters=18,
                 events_per_chapter=810):  # 每章默认810个事件
        self.characters = characters
        self.setting = setting
        self.friffery = friffery
        self.debug = debug
        self.title = title
        self.chapters = chapters
        self.events_per_chapter = events_per_chapter

    def publish_chapter(self, chapter_num):
        # 构造事件收集器
        collector = EventCollector()

        # 为每个角色初始化
        for character in self.characters:
            character.collector = collector
            # 请不要继续前一章的对话。
            character.topic = None
            character.place_in(random.choice(self.setting))

        while len(collector.events) < self.events_per_chapter:
            for character in self.characters:
                # 生成生活动态？？？出口是？？？
                character.live()
                # print len(collector.events) # , repr([str(e) for e in collector.events])

        if self.debug:
            for character in self.characters:
                print "%s的 EVENTS:" % character.name.upper()
                for event in collector.events:
                    # 第一参与者
                    if event.participants[0] != character:
                        continue
                    print "%s 在 %s: %s" % (
                        [p.render(event=event) for p in event.participants],
                        event.location.render(),
                        event.phrase
                    )
                print
            for character in self.characters:
                print "%s的状态:" % character.name.upper()
                # dump intents？导出意图？
                character.dump_beliefs()
                print
            print "- - - - -"
            print

        editor = Editor(collector, self.characters)
        editor.add_transformer(MadeTheirWayToTransformer())
        editor.add_transformer(DeduplicateTransformer())
        editor.add_transformer(AggregateEventsTransformer())
        editor.add_transformer(DetectWanderingTransformer())
        # 这应该是最后一个，所以现有的转换器器不必担心自己找代词
        editor.add_transformer(UsePronounsTransformer())
        # 当您实例化一个发布服务器时，这应该是配置什么样的转换器使用的问题。
        if self.friffery:
            editor.add_transformer(AddWeatherFrifferyTransformer())
            editor.add_transformer(AddParagraphStartFrifferyTransformer())
        # 编辑器现在已经获得 角色，事件收集器，转换器，生成吧！
        editor.publish()

    def publish(self):
        print self.title
        print "=" * len(self.title)
        print

        # 逐章生成
        for chapter in range(1, self.chapters + 1):
            print "第 %d 章" % chapter
            print "-----------"
            print

            self.publish_chapter(chapter)
