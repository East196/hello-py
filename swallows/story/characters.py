# coding=utf-8

import random

from swallows.engine.objects import (
    Animate, ProperMixin, MasculineMixin, FeminineMixin,
    Topic,
    GreetTopic, SpeechTopic, QuestionTopic,
    Belief, ItemLocation, Goal,
)


# 各种点子...
# 他们可以隐藏的东西，然后看到其他携带它，然后检查
# 它仍然是隐藏的，而感到惊讶，它不再有。
# “你好，爱丽丝，”鲍伯说。“你好，鲍伯，”爱丽丝回答。永远不会变老
# 他们应该总是尖叫看见尸体时。尖叫声应该
# 是整个房子和院子听到。
# …他们检查白兰地仍在白酒类柜。这是
# 真的必要吗？
# 某些东西不能带，但可以拖（如身体）
# 路径查找任意两个房间之间——不太难，即使它
# 会更好实现。
# “美极了”--实际上*有*回忆的地点，和感情
# （好的/坏的，0个10之类的）回忆
# 焦虑记忆=一个他们最近的恐慌
# 记忆是否左轮装他们最后一次看到它
# 电话恫吓
# 在逃跑时，在枪口下（或试图分散他们的注意力，
# 掴了枪，争夺它，等）
# 左轮手枪可能堵塞，当他们试图把它（也许应该是
# 手枪相反，那些可以堵塞更容易）
# 亲爱的我，有人竟然会被射杀。那是什么？另一具尸体？

# ## some Swallows-specific topics (sort of)

# 在哪里的问题
class WhereQuestionTopic(Topic):
    pass


# 威胁给
class ThreatGiveMeTopic(Topic):
    pass


# 威胁说
class ThreatTellMeTopic(Topic):
    pass


# 威胁同意
class ThreatAgreeTopic(Topic):
    pass


# ## some Swallows-specific beliefs
# 涉嫌隐藏
class SuspicionOfHiding(Belief):
    """This character suspects some other character of hiding this thing."""

    def __str__(self):
        return "我觉得有人把 %s 藏起来了" % (
            self.subject.render()
        )


# 基本角色特征
class Character(Animate):
    def __init__(self, name, location=None, collector=None):
        """
        特定于字符的构造函数。在里面，我们建立了一些特定属性（情绪）。
        隐藏属性
        """
        Animate.__init__(self, name, location=location, collector=None)
        # 发生事件是可能会改变。但现在， 初始化的情绪是平静的。
        self.nerves = '平静'

    def configure_objects(self, revolver=None, brandy=None, dead_body=None):
        """
        在这里，我们设置了一些重要的项目，这个角色需要知道。这也许是一种依赖注入。
        角色需要知道的重要事情
        """
        self.revolver = revolver
        self.brandy = brandy
        self.dead_body = dead_body

    def believe_location(self, thing, location, informant=None, concealer=None):
        # 我们重写此方法以除去我们的动画也怀疑物品被隐藏。”因为我们找到了它。
        Animate.believe_location(self, thing, location, informant=informant, concealer=concealer)
        self.beliefs.remove(SuspicionOfHiding(thing))

    def move_to(self, location):
        """
        重写某些行为在移动到新的位置。
        """
        Animate.move_to(self, location)
        if random.randint(0, 10) == 0:
            self.emit("<1>,欢迎您再次来到<2>。",
                      [self, self.location], excl=True)

        # 好了，看看四周。
        for x in self.location.contents:
            assert x.location == self.location
            if x == self:
                continue
            if x.horror():
                belief = self.recall_location(x)
                if belief:
                    amount = random.choice(['战栗', '波动'])
                    emotion = random.choice(['害怕', '厌恶', '呕吐', '憎恨'])  # 情感
                    self.emit("<1> 感觉到 %s 的 %s 当 <he-1> 发现 <2>" % (emotion, amount), [self, x])
                    self.remember_location(x, self.location)
                else:
                    verb = random.choice(['尖叫着', '叫喊着', '平淡的'])
                    self.emit("<1> %s 看着 <indef-2>" % verb, [self, x], excl=True)
                    self.remember_location(x, self.location)
                    self.nerves = '战栗'
            elif x.animate():
                other = x
                self.emit("<1> 看到 <2>", [self, other])
                other.emit("<1> 看到 <2> 走入 %s" % self.location.noun(), [other, self])
                self.remember_location(x, self.location)
                self.greet(x, "'你好, <2>,' <1> 微笑着说")
                for y in other.contents:
                    if y.treasure():
                        self.emit(
                            "<1> 注意到 <2> <was-2> 拿起了 <indef-3>",
                            [self, other, y])
                        if self.revolver.location == self:
                            self.point_at(other, self.revolver)
                            self.address(other,
                                         ThreatGiveMeTopic(self, subject=y),
                                         "'给我 <3>, <2>, 否则我就给你一枪,' <he-1> 威胁道",
                                         [self, other, y])
                            return
                # 检查怀疑被隐藏的东西。
                suspicions = list(self.beliefs.beliefs_of_class(SuspicionOfHiding))
                # 如果我们这样做…我们可以做点什么…
                actionable_suspicions = []
                for suspicion in suspicions:
                    if not suspicion.subject.treasure():
                        continue
                    if self.beliefs.get(ItemLocation(suspicion.subject)):
                        continue
                    actionable_suspicions.append(suspicion)
                if actionable_suspicions and self.revolver.location == self:
                    suspicion = random.choice(actionable_suspicions)
                    self.point_at(other, self.revolver)
                    self.address(other,
                                 ThreatTellMeTopic(self, subject=suspicion.subject),
                                 "'告诉我你藏了 <3>, <2>, 否则我就给你一枪,' <he-1> 说",
                                 [self, other, suspicion.subject])
                    return
            elif x.notable():
                self.emit("<1> 看到了 <2>", [self, x])
                self.remember_location(x, self.location)

    def live(self):
        """
        改写故事中的一些行为。
        """
        # 首先，如果在谈话中，把注意力集中到那一点上。
        if self.topic is not None:
            return self.converse(self.topic)

        # 否则，如果你想要的东西在这里，你必须把它们捡起来。
        for x in self.location.contents:
            if self.does_desire(x):
                self.pick_up(x)
                return
        people_about = False

        # 否则，专注于一些有价值的对象（可能是左轮手枪），你拿着：
        fixated_on = None
        for y in self.contents:
            if y.treasure():
                fixated_on = y
                break
        if not fixated_on and random.randint(0, 20) == 0 and self.revolver.location == self:
            fixated_on = self.revolver

        # 看看你是不是一个人
        for x in self.location.contents:
            if x.animate() and x is not self:
                people_about = True

        choice = random.randint(0, 25)
        if choice < 10 and not people_about:
            return self.hide_and_seek(fixated_on)
        if choice < 20:
            return self.wander()
        if choice == 20:
            self.emit("<1> 打了个哈欠", [self])
        elif choice == 21:
            self.emit("<1> 目视远方", [self])
        elif choice == 22:
            self.emit("<1> 关心 <he-1> 听到的东西", [self])
        elif choice == 23:
            self.emit("<1> 挠了挠 <his-1> 头", [self])
        elif choice == 24:
            self.emit("<1> 立即觉得事情有点不对劲了", [self])
        else:
            return self.wander()

    #
    # 下面是相当具体的情节。
    #

    # 隐藏与搜索
    def hide_and_seek(self, fixated_on):
        # 检查一个地方躲起来，你很在意的事情
        containers = []
        for container in self.location.contents:
            if container.container():
                # 我以前藏过什么东西吗？回忆啊，信念是渣渣
                beliefs_about_container = []
                for thing in self.beliefs.subjects():
                    belief = self.recall_location(thing)
                    if belief and belief.location == container:
                        beliefs_about_container.append(belief)
                containers.append((container, beliefs_about_container))
        if not containers:
            # ？…也许这应该是来电者的责任。
            return self.wander()
        # 好啊!我们现在有一个容器列表，每一个容器都有零个或更多的事物存在的信念。
        if fixated_on:
            (container, beliefs) = random.choice(containers)
            self.emit("<1> 把 <2> 藏在 <3> 里", [self, fixated_on, container])
            fixated_on.move_to(container)
            self.remember_location(fixated_on, container, concealer=self)
            return self.wander()
        else:
            # 我们在找宝藏！
            # todo: 优先选择可能是更好地。
            (container, beliefs) = random.choice(containers)
            # 有时候，我们不在乎我们认为我们知道什么（这让我们，例如，探索的东西，希望白兰地）
            if beliefs and random.randint(0, 3) == 0:
                beliefs = None
            if beliefs:
                belief = random.choice(beliefs)
                thing = belief.subject
                picking_up = random.randint(0, 5) == 0
                if thing is self.revolver:
                    picking_up = True
                if picking_up:
                    if belief.concealer is self:
                        self.emit("<1> 取回了 <he-1> 藏在 <2> 的 <3> ",
                                  [self, container, thing])
                    else:
                        self.emit("<1> 从 <2> 取回了 <3> ",
                                  [self, container, thing])
                    # but!
                    if thing.location != container:
                        self.emit("但是 <he-2> <was-2> 不见了",
                                  [self, thing], excl=True
                                  )
                        # 忘记一切. 如此逼真!
                        self.forget_location(thing)
                    else:
                        thing.move_to(self)
                        self.remember_location(thing, self)
                else:
                    self.emit("<1> 检查到 <3> <was-3> 依然在 <2>",
                              [self, container, thing])
                    # but!
                    if thing.location != container:
                        self.emit("但是 <he-2> <was-2> 不见了",
                                  [self, thing], excl=True
                                  )
                        self.forget_location(thing)
                        self.beliefs.add(SuspicionOfHiding(thing))
            else:  # 没有关于这个的记忆
                self.emit("<1> 搜索了 <2>", [self, container])
                desired_things = []
                for thing in container.contents:
                    # 记住你在搜索这个容器时看到的东西。
                    self.remember_location(thing, container)
                    if self.does_desire(thing):
                        desired_things.append(thing)
                if desired_things:
                    thing = random.choice(desired_things)
                    self.emit("<1> 发现了 <2> 然后捡起它 <him-2>",
                              [self, thing, container], exciting=True)
                    thing.move_to(self)
                    self.remember_location(thing, self)

    # 谈话
    def converse(self, topic):
        self.topic = None
        other = topic.originator
        if isinstance(topic, ThreatGiveMeTopic):
            found_object = None
            for x in self.contents:
                if x is topic.subject:
                    found_object = x
                    break
            if not found_object:
                self.speak_to(other,
                              "'但是我没有 <3>!' 抗拒 <1>",
                              [self, other, topic.subject])
            else:
                self.speak_to(other,
                              "'求你别开枪!', <1> 哭着说",
                              [self, other, found_object])
                self.give_to(other, found_object)
        elif isinstance(topic, ThreatTellMeTopic):
            belief = self.recall_location(topic.subject)
            if not belief:
                self.speak_to(other,
                              "'我记不起来了, <2>,' <1> 重复道",
                              [self, other, topic.subject])
            else:
                self.speak_to(other,
                              "'不要开枪!', <1> 哭着喊道, '<he-3> <is-3> 在 <4>'",
                              [self, other, topic.subject, belief.location])
                other.believe_location(topic.subject, belief.location,
                                       informant=self, concealer=self)
        elif isinstance(topic, ThreatAgreeTopic):
            self.speak_to(other,
                          "'你对一个有说服力的理由犹豫不决, <2>,' <1> 说",
                          [self, other])
            self.beliefs.remove(Goal(topic.subject))
            # 更新其他的beliefsbelief自我不再包含这个目标
            other.believed_beliefs_of(self).remove(Goal(topic.subject))
        elif isinstance(topic, GreetTopic):
            # 发出的，因为在这一speak_to导致太多的愚蠢
            self.emit("'你好啊, <2>,'  <1> 回道", [self, other])
            # 这需要更一般化。
            self_belief = self.recall_location(self.dead_body)
            if self_belief:
                self.discuss(other, self_belief)
                return
            # 这个需要不是在所有时间
            for x in other.contents:
                if x.notable():
                    self.remember_location(x, other)
                    self.speak_to(other, "'我看到你正在 <indef-3>,'  <1> 说", [self, other, x])
                    return
            choice = random.randint(0, 3)
            if choice == 0:
                self.question(other, "'天气不错啊，是不?'  <1> 闲聊说")
            if choice == 1:
                self.speak_to(other, "'我想知道你在哪里,' <1> 说")
        elif isinstance(topic, QuestionTopic):
            if topic.subject is not None:
                choice = random.randint(0, 1)
                if choice == 0:
                    self.speak_to(other, "'我对 <3> 一无所知, <2>,' <1> 抱怨道",
                                  [self, other, topic.subject])
                if choice == 1:
                    self.speak_to(other, "'也许吧, <2>,' <1> 回答")
            else:
                self.speak_to(other, "'也许吧, <2>,' <1> 回答")
        elif isinstance(topic, WhereQuestionTopic):
            belief = self.recall_location(topic.subject)
            if not belief:
                self.speak_to(other,
                              "'我不知道,' <1> 简单的回答",
                              [self, other, topic.subject])
            elif belief.concealer == self:
                self.question(other,
                              "'为什么你不知道 <3> 在哪儿, <2>?'",
                              [self, other, topic.subject])
            elif topic.subject.location == self:
                self.speak_to(other,
                              "'我就在这儿拿到 <3> 的, <2>'",
                              [self, other, topic.subject])
                self.put_down(topic.subject)
            else:
                if topic.subject.location.animate():
                    self.speak_to(other,
                                  "'我认为 <3> 有 <4>,', <1> 回忆",
                                  [self, other, belief.location, topic.subject])
                else:
                    self.speak_to(other,
                                  "'我坚信 它在<3>, <2>,', <1> 回忆",
                                  [self, other, belief.location])
                other.believe_location(
                    topic.subject, belief.location, informant=self
                )
        elif isinstance(topic, SpeechTopic):
            choice = random.randint(0, 5)
            if choice == 0:
                self.emit("<1> 点头", [self])
            if choice == 1:
                self.emit("<1> 保持沉默", [self])
            if choice == 2:
                self.question(other, "'你真的这样想?' <1> 问道")
            if choice == 3:
                self.speak_to(other, "'是的，这真丢脸,' <1> 陈述")
            if choice == 4:
                self.speak_to(other, "'哦, 我知道, 我知道,' <1> 说")
            if choice == 5:
                self.speak_to(other, "'我明白了, <2>, 我明白了,' <1> 恍然大悟")

    # 讨论
    def discuss(self, other, self_memory):
        assert self_memory
        assert isinstance(self_memory, Belief)
        # 现在，self_memory大约是在我们的脑海中有一个itemlocation信仰
        assert isinstance(self_memory, ItemLocation)

        # 我相信另一方对此有何看法？
        other_beliefs = self.believed_beliefs_of(other)
        other_memory = other_beliefs.get(self_memory)

        if not other_memory:
            self.question(other,
                          "'你知道这儿是 <indef-3> 在 <4>?' <1> 问",
                          [self, other, self_memory.subject, self_memory.location],
                          subject=self_memory.subject)
            # 现在他们知道我们的想法了，不管怎样
            other.believed_beliefs_of(self).add(self_memory)
            return
        else:
            choice = random.randint(0, 2)
            if choice == 0:
                self.question(other, "'你认为我们应该对 <3> 做些什么?' <1>说",
                              [self, other, self_memory.subject])
                other.believed_beliefs_of(self).add(self_memory)
            if choice == 1:
                self.speak_to(other, "'我觉得我们应该对 <3> 做点什么, <2>,' <1> 说",
                              [self, other, self_memory.subject])
                other.believed_beliefs_of(self).add(self_memory)
            if choice == 2:
                if self.nerves == '平静':
                    self.decide_what_to_do_about(other, self_memory.subject)
                else:
                    if self.brandy.location == self:
                        self.emit("<1> 给 <him-1> 自己一杯白兰地",
                                  [self, other, self_memory.subject])
                        self.quench_desire(self.brandy)
                        self.nerves = '平静'
                        self.put_down(self.brandy)
                    elif self.recall_location(self.brandy):
                        self.speak_to(other,
                                      "'我得先喝两口,' <1> 叹了一声",
                                      [self, other, self_memory.subject],
                                      subject=self.brandy)
                        self.desire(self.brandy)
                        if random.randint(0, 1) == 0:
                            self.address(other, WhereQuestionTopic(self, subject=self.brandy),
                                         "'你觉得 <3> 应该在哪?'",
                                         [self, other, self.brandy])
                    else:
                        self.address(other, WhereQuestionTopic(self, subject=self.brandy),
                                     "'白兰地在哪?  我想喝几口,' <1> 说",
                                     [self, other, self_memory.subject])
                        self.desire(self.brandy)

    # 决定去做什么
    def decide_what_to_do_about(self, other, thing):
        # 这可能是受是否拥有这种性格，哦，我不知道，把其他的枪口下，或没有，或什么的
        my_goal = self.beliefs.get(Goal(thing))
        if my_goal is None:
            if random.randint(0, 1) == 0:
                self.beliefs.add(Goal(thing, '叫警察了'))
            else:
                self.beliefs.add(Goal(thing, '试图解决'))
        my_goal = self.beliefs.get(Goal(thing))
        assert my_goal is not None

        # 这里开始变得有点gnarly.what我相信其他的信仰吗？
        other_beliefs = self.believed_beliefs_of(other)
        # 更具体地说，他们的目标是什么？
        other_goal = other_beliefs.get(Goal(thing))

        # 他们还没有。告诉他们我们的。
        if other_goal is None:
            self.speak_to(other,
                          "'我觉得我们应该 %s <3>, <2>,'  <1> 说" % my_goal.phrase,
                          [self, other, thing])
            # 好吧，他们知道我现在在想什么：
            other.believed_beliefs_of(self).add(my_goal)
        elif other_goal.phrase == my_goal.phrase:
            # 达成协议
            self.question(other,
                          ("'所以我们同意 %s ，<3>?' <1> 问" %
                           my_goal.phrase),
                          [self, other, thing])
            # 另一方可能没有意识到他们同意。
            other.believed_beliefs_of(self).add(my_goal)
        else:  # 我们不同意.
            if self.revolver.location == self:
                self.point_at(other, self.revolver)
                self.address(other,
                             ThreatAgreeTopic(self, subject=thing),
                             (
                                 "'我觉得我们最好 %s <3>, <2>,' <he-1> 咬牙切齿的说" %
                                 my_goal.phrase),
                             [self, other, thing])
                # 万一他们不知道呢
                other.believed_beliefs_of(self).add(my_goal)
            else:
                self.speak_to(other,
                              ("'我不认为这是个好主意 去做 %s <3>, <2>,' <1> 说" %
                               my_goal.phrase),
                              [self, other, thing])
                other.believed_beliefs_of(self).add(my_goal)


# 男性角色
class MaleCharacter(MasculineMixin, ProperMixin, Character):
    pass


# 女性角色
class FemaleCharacter(FeminineMixin, ProperMixin, Character):
    pass
