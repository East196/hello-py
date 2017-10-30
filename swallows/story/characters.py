# coding=utf-8

import random

from swallows.engine.objects import (
    Animate, ProperMixin, MasculineMixin, FeminineMixin,
    Topic,
    GreetTopic, SpeechTopic, QuestionTopic,
    Belief, ItemLocation, Goal,
)


# TODO

# They can hide something, then see the other carrying it, then check that
# it's still hidden, and be surprised that it's no longer ther.
# 'Hello, Alice', said Bob.  'Hello, Bob', replied Alice.  NEVER GETS OLD
# they should always scream at seeing the dead body.  the scream should
#   be heard throughout the house and yard.
# ...they check that the brandy is still in the liquor cabinet.  is this
#   really necessary?
# certain things can't be taken, but can be dragged (like the body)
# path-finder between any two rooms -- not too difficult, even if it
#   would be nicer in Prolog.
# "it was so nice" -- actually *have* memories of locations, and feelings
#   (good/bad, 0 to 10 or something) about memories
# anxiety memory = the one they're most recently panicked about
# memory of whether the revolver was loaded last time they saw it
# calling their bluff
# making a run for it when at gunpoint (or trying to distract them,
#   slap the gun away, scramble for it, etc)
# revolver might jam when they try to shoot it (maybe it should be a
#   pistol instead, as those can jam more easily)
# dear me, someone might actually get shot.  then what?  another dead body?


### some Swallows-specific topics (sort of)

class WhereQuestionTopic(Topic):
    pass


class ThreatGiveMeTopic(Topic):
    pass


class ThreatTellMeTopic(Topic):
    pass


class ThreatAgreeTopic(Topic):
    pass


### some Swallows-specific beliefs

class SuspicionOfHiding(Belief):
    """This character suspects some other character of hiding this thing."""

    def __str__(self):
        return "我觉得有人把 %s 藏起来了" % (
            self.subject.render()
        )


### Base character personalities for The Swallows

class Character(Animate):
    def __init__(self, name, location=None, collector=None):
        """Constructor specific to characters.  In it, we set up some
        Swallows-specific properties ('nerves').
        隐藏属性
        """
        Animate.__init__(self, name, location=location, collector=None)
        # this should really be *derived* from having a recent memory
        # of seeing a dead body in the bathroom.  but for now,
        # 初始化的心情是平静的
        self.nerves = '平静'

    def configure_objects(self, revolver=None, brandy=None, dead_body=None):
        """Here we set up some important items that this character needs
        to know about.  This is maybe a form of dependency injection.
        角色需要知道的重要事情
        """
        self.revolver = revolver
        self.brandy = brandy
        self.dead_body = dead_body

    def believe_location(self, thing, location, informant=None, concealer=None):
        # we override this method of Animate in order to also remove
        # our suspicion that the item has been hidden.  'cos we found it.
        Animate.believe_location(self, thing, location, informant=informant, concealer=concealer)
        self.beliefs.remove(SuspicionOfHiding(thing))

    def move_to(self, location):
        """Override some behaviour upon moving to a new location.

        """
        Animate.move_to(self, location)
        if random.randint(0, 10) == 0:
            self.emit("很高兴 <1> 再次来到 <2> ",
                      [self, self.location], excl=True)

        # okay, look around you.
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
                # check if we suspect something of being hidden.
                suspicions = list(self.beliefs.beliefs_of_class(SuspicionOfHiding))
                # if we do... and we can do something about it...
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
        """Override some behaviour for taking a turn in the story.

        """
        # first, if in a conversation, turn total attention to that
        if self.topic is not None:
            return self.converse(self.topic)

        # otherwise, if there are items here that you desire, you *must* pick
        # them up.
        for x in self.location.contents:
            if self.does_desire(x):
                self.pick_up(x)
                return
        people_about = False

        # otherwise, fixate on some valuable object (possibly the revolver)
        # that you are carrying:
        fixated_on = None
        for y in self.contents:
            if y.treasure():
                fixated_on = y
                break
        if not fixated_on and random.randint(0, 20) == 0 and self.revolver.location == self:
            fixated_on = self.revolver

        # check if you are alone
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
    # The following are fairly plot-specific.
    #

    def hide_and_seek(self, fixated_on):
        # check for some place to hide the thing you're fixating on
        containers = []
        for container in self.location.contents:
            if container.container():
                # did I hide something here previously?
                beliefs_about_container = []
                for thing in self.beliefs.subjects():
                    belief = self.recall_location(thing)
                    if belief and belief.location == container:
                        beliefs_about_container.append(belief)
                containers.append((container, beliefs_about_container))
        if not containers:
            # ? ... maybe this should be the responsibility of the caller
            return self.wander()
        # ok!  we now have a list of containers, each of which has zero or
        # more beliefs of things being in it.
        if fixated_on:
            (container, beliefs) = random.choice(containers)
            self.emit("<1> 把 <2> 藏在 <3> 里", [self, fixated_on, container])
            fixated_on.move_to(container)
            self.remember_location(fixated_on, container, concealer=self)
            return self.wander()
        else:
            # we're looking for treasure!
            # todo: it would maybe be better to prioritize this selection
            (container, beliefs) = random.choice(containers)
            # sometimes, we don't care what we think we know about something
            # (this lets us, for example, explore things in hopes of brandy)
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
                        # forget ALLLLLLL about it, then.  so realistic!
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
            else:  # no memories of this
                self.emit("<1> 搜索了 <2>", [self, container])
                desired_things = []
                for thing in container.contents:
                    # remember what you saw whilst searching this container
                    self.remember_location(thing, container)
                    if self.does_desire(thing):
                        desired_things.append(thing)
                if desired_things:
                    thing = random.choice(desired_things)
                    self.emit("<1> 发现了 <2> 然后捡起它 <him-2>",
                              [self, thing, container], exciting=True)
                    thing.move_to(self)
                    self.remember_location(thing, self)

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
            # update other's BeliefsBelief about self to no longer
            # contain this Goal
            other.believed_beliefs_of(self).remove(Goal(topic.subject))
        elif isinstance(topic, GreetTopic):
            # emit, because making this a speak_to leads to too much silliness
            self.emit("'你好啊, <2>,'  <1> 回道", [self, other])
            # this needs to be more general
            self_belief = self.recall_location(self.dead_body)
            if self_belief:
                self.discuss(other, self_belief)
                return
            # this need not be *all* the time
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
                # -- this is getting really annoying.  disable for now. --
                # item = random.choice(ALL_ITEMS)
                # self.question(other, "'But what about <3>, <2>?' posed <1>",
                #    [self, other, item], subject=item)
                self.speak_to(other, "'我明白了, <2>, 我明白了,' <1> 恍然大悟")

    # this is its own method for indentation reasons
    def discuss(self, other, self_memory):
        assert self_memory
        assert isinstance(self_memory, Belief)
        # for now,
        # self_memory is an ItemLocation belief about something on our mind
        assert isinstance(self_memory, ItemLocation)

        # what do I believe the other believes about it?
        other_beliefs = self.believed_beliefs_of(other)
        other_memory = other_beliefs.get(self_memory)

        if not other_memory:
            self.question(other,
                          "'你知道这儿是 <indef-3> 在 <4>?' <1> 问",
                          [self, other, self_memory.subject, self_memory.location],
                          subject=self_memory.subject)
            # well now they know what we think, anyway
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

    # this is its own method for indentation reasons
    def decide_what_to_do_about(self, other, thing):
        # this should probably be affected by whether this
        # character has, oh, i don't know, put the other at
        # gunpoint yet, or not, or something
        my_goal = self.beliefs.get(Goal(thing))
        if my_goal is None:
            if random.randint(0, 1) == 0:
                self.beliefs.add(Goal(thing, '叫警察了'))
            else:
                self.beliefs.add(Goal(thing, '试图解决'))
        my_goal = self.beliefs.get(Goal(thing))
        assert my_goal is not None

        # here's where it gets a bit gnarly.
        # what do I believe the other believes?
        other_beliefs = self.believed_beliefs_of(other)
        # more specifically, what are their goals regarding the thing?
        other_goal = other_beliefs.get(Goal(thing))

        # they don't have one yet.  tell them ours.
        if other_goal is None:
            self.speak_to(other,
                          "'我觉得我们应该 %s <3>, <2>,'  <1> 说" % my_goal.phrase,
                          [self, other, thing])
            # ok, they know what I think now:
            other.believed_beliefs_of(self).add(my_goal)
        elif other_goal.phrase == my_goal.phrase:
            # TODO make this an AgreementQuestion or smth
            self.question(other,
                          ("'所以我们同意 %s ，<3>?' <1> 问" %
                           my_goal.phrase),
                          [self, other, thing])
            # the other party might not've been aware that they agree
            other.believed_beliefs_of(self).add(my_goal)
        else:  # WE DO NOT AGREE.
            if self.revolver.location == self:
                self.point_at(other, self.revolver)
                self.address(other,
                             ThreatAgreeTopic(self, subject=thing),
                             (
                                 "'我觉得我们最好 %s <3>, <2>,' <he-1> 咬牙切齿的说" %
                                 my_goal.phrase),
                             [self, other, thing])
                # just in case they weren't clued in yet
                other.believed_beliefs_of(self).add(my_goal)
            else:
                self.speak_to(other,
                              ("'我不认为这是个好主意 去做 %s <3>, <2>,' <1> 说" %
                               my_goal.phrase),
                              [self, other, thing])
                other.believed_beliefs_of(self).add(my_goal)


class MaleCharacter(MasculineMixin, ProperMixin, Character):
    pass


class FemaleCharacter(FeminineMixin, ProperMixin, Character):
    pass
