# coding=utf-8
import random

from swallows.engine.events import Event


### TOPICS主题 ###

# a "topic" is just what a character has recently had addressed to
# them.  It could be anything, not just words, by another character
# (for example, a gesture.)

class Topic(object):
    def __init__(self, originator, subject=None):
        self.originator = originator
        self.subject = subject


class GreetTopic(Topic):
    pass


class SpeechTopic(Topic):
    pass


class QuestionTopic(Topic):
    pass


### BELIEFS ###

#
# a belief is something an Animate believes.  they come in a few types:
#
# - a belief that an object is somewhere
#   - because they saw it there (memory)
#   - because some other character told them it was there
# - a belief that they should do something (a goal), which has subtypes:
#   - a belief that an object is desirable & they should try to acquire it
#   - a belief that something should be done about something (bland, general)
# - a belief that another Animate believes something
#
# of course, any particular belief may turn out not to be true
#
# 真的是抱有一个信念。。。
# abstract base class
class Belief(object):
    # constructor of all subclasses of this class should accept being
    # called with only one argument, as a convenience sort of thing
    # for BeliefSet.get and .remove, which don't really care about anything
    # about the Belief except for its class and its subject.
    # although, usually, you do want to pass more than one argument when
    # making a real Belief to pass to BeliefSet.add.  (clear as mud, right?)
    def __init__(self, subject):  # kind of silly for an ABC to have a
        assert isinstance(subject, Actor)  # constructor, but it is to emphasize
        self.subject = subject  # that all beliefs have a subject,
        # which is the thing we believe
        # something about

    def __str__(self):
        raise NotImplementedError


class ItemLocation(Belief):  # formerly "Memory"
    def __init__(self, subject, location=None, informant=None, concealer=None):
        assert isinstance(subject, Actor)
        assert isinstance(location, Actor) or location is None
        self.subject = subject  # the thing we think is somewhere
        self.location = location  # the place we think it is
        self.informant = informant  # the actor who told us about it
        self.concealer = concealer  # the actor who we think hid it there

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


class Goal(Belief):
    def __init__(self, subject, phrase=None):
        assert isinstance(subject, Actor)
        self.subject = subject  # the thing we would like to do something about
        self.phrase = phrase  # human-readable description

    def __str__(self):
        return "我应该 %s %s" % (
            self.phrase,
            self.subject.render()
        )


# 欲望
class Desire(Goal):
    def __init__(self, subject):
        assert isinstance(subject, Actor)
        self.subject = subject  # the thing we would like to acquire

    def __str__(self):
        return "我想要 %s" % (
            self.subject.render()
        )


# oh dear 坚信的信念
class BeliefsBelief(Belief):
    def __init__(self, subject, belief_set=None):
        assert isinstance(subject, Animate)
        self.subject = subject  # the animate we think holds the belief
        if belief_set is None:
            belief_set = BeliefSet()
        assert isinstance(belief_set, BeliefSet)
        self.belief_set = belief_set  # the beliefs we think they hold

    def __str__(self):
        return "%s 坚信 { %s }" % (
            self.subject.render(),
            self.belief_set
        )


# 信念的集合
class BeliefSet(object):
    """A BeliefSet works something like a Python set(), but has the
    following constraints:
    
    There can be only one of each type of Belief about a particular
    item in the set.

    So it's really kind of a map from Actors to maps from Belief
    subclasses to Beliefs.

    But it behooves us (or at least, me) to think of it as a set.
    (Besides, it might change.)

    """

    def __init__(self):
        self.belief_map = {}

    def add(self, belief):
        assert isinstance(belief, Belief)
        subject = belief.subject
        self.belief_map.setdefault(subject, {})[belief.__class__] = belief

    def remove(self, belief):
        # the particular belief passed to us doesn't really matter.  we extract
        # the class and subject and return any existing belief we may have
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


### ACTORS (objects in the world) ###
#
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

    def container(self):
        return False

    def article(self):
        return '那个'

    def posessive(self):
        return "它"

    def accusative(self):
        return "它"

    def pronoun(self):
        return "它"

    def was(self):
        return "过去是"

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
        """Return a string containing what we call this object, in the context
        of the given event (which may be None, to get a 'generic' description.)

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
                repl = event.initiator().posessive()
        if repl is not None:
            name = name.replace('<*>', repl)
        article = self.article()
        if not article:
            return name
        return '%s %s' % (article, name)

    def indefinite(self):
        article = '一个'
        return '%s %s' % (article, self.name)


### some mixins for Actors ###

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


class MasculineMixin(object):
    def posessive(self):
        return "他"

    def accusative(self):
        return "他"

    def pronoun(self):
        return "他"


class FeminineMixin(object):
    def posessive(self):
        return "她"

    def accusative(self):
        return "她"

    def pronoun(self):
        return "她"


### ANIMATE OBJECTS ###

class Animate(Actor):
    def __init__(self, name, location=None, owner=None, collector=None):
        Actor.__init__(
            self, name, location=location, owner=owner, collector=None
        )
        self.topic = None
        self.beliefs = BeliefSet()

    def animate(self):
        return True

    # for debugging
    def dump_beliefs(self):
        for subject in self.beliefs.subjects():
            for belief in self.beliefs.beliefs_for(subject):
                print ".oO{ %s }" % belief

    ###--- belief accessors/manipulators ---###

    # these are mostly just aliases for accessing the BeliefSet.

    def remember_location(self, thing, location, concealer=None):
        """Update this Animate's beliefs to include a belief that the
        given thing is located at the given location.

        Really just a readable alias for believe_location.

        """
        self.believe_location(thing, location, informant=None, concealer=concealer)

    def believe_location(self, thing, location, informant=None, concealer=None):
        """Update this Animate's beliefs to include a belief that the
        given thing is located at the given location.  They may have
        been told this by someone.

        """
        self.beliefs.add(ItemLocation(
            thing, location, informant=informant, concealer=concealer
        ))

    def recall_location(self, thing):
        """Return an ItemLocation (belief) about this thing, or None."""
        return self.beliefs.get(ItemLocation(thing))

    def forget_location(self, thing):
        self.beliefs.remove(ItemLocation(thing))

    def desire(self, thing):
        self.beliefs.add(Desire(thing))

    def quench_desire(self, thing):
        # usually called when it has been acquired
        self.beliefs.remove(Desire(thing))

    def does_desire(self, thing):
        if thing.treasure():
            return True  # omg YES
        if thing.weapon():
            return True  # could come in handy.  (TODO, sophisticate this?搞复杂点如何？)
        return self.beliefs.get(Desire(thing)) is not None

    def believed_beliefs_of(self, other):
        """Returns a BeliefSet (not a Belief) that this Animate
        believes the other Animate holds.

        Typically you would manipulate this BeliefSet directly
        with add, remove, get, etc.

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

    ###--- generic actions ---###
    # 出现在某地
    def place_in(self, location):
        """Like move_to but quieter.  For setting up scenes, etc.

        """
        if self.location is not None:
            self.location.contents.remove(self)
        self.location = location
        self.location.contents.add(self)
        # this is needed so that the Editor knows where the character starts.
        # the Editor should (does?) strip out all instances of these that
        # aren't informative to the reader.
        self.emit("<1> <was-1> 在 <2>", [self, self.location])
        # a side-effect of the following code is, if they start in a location
        # with a horror,they don't react to it.  They probably should.
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
            # otherwise we get "Bob saw Bob leave the room", eh?
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
        # it would be nice if there was some way to
        # indicate the revolver as part of the Topic which will follow,
        # or otherwise indicate the context as "at gunpoint"

        assert self.location == other.location
        assert item.location == self
        self.emit("<1> 拿 <3> 指着 <2>",
                  [self, other, item])
        for actor in self.location.contents:
            if actor.animate():
                actor.remember_location(item, self)

    def put_down(self, item):
        assert (item.location == self)
        self.emit("<1> 放下 <2>", [self, item])
        item.move_to(self.location)
        for actor in self.location.contents:
            if actor.animate():
                actor.remember_location(item, self.location)

    def pick_up(self, item):
        assert (item.location == self.location)
        self.emit("<1> 捡起 <2>", [self, item])
        item.move_to(self)
        for actor in self.location.contents:
            if actor.animate():
                actor.remember_location(item, self)

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
        """This gets called on each turn an animate moves.
        
        You need to implement this for particular animates.
        
        """
        raise NotImplementedError(
            '请实现 %s.live()' % self.__class__.__name__
        )


class Male(MasculineMixin, ProperMixin, Animate):
    pass


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


### OTHER INANIMATE OBJECTS ###

class Item(Actor):
    def takeable(self):
        return True


class Weapon(Item):
    def weapon(self):
        return True


class Container(Actor):
    def container(self):
        return True


class ProperContainer(ProperMixin, Container):
    pass


# 财宝
class Treasure(Item):
    def treasure(self):
        return True


class PluralTreasure(PluralMixin, Treasure):
    pass


class Horror(Actor):
    def horror(self):
        return True
