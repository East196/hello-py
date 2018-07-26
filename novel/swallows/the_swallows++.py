#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Example of extending _The Swallows_ world to produce a different story.
#

import sys


from os.path import realpath, dirname, join

# get the ../src/ directory onto the Python module search path
sys.path.insert(0, join(dirname(realpath(sys.argv[0])), '..', 'src'))

# now we can import the classes we will work with
from novel.swallows.story.characters import MaleCharacter
from novel.swallows.story.world import (
    alice, bob, house, upstairs_hall,
    revolver, brandy, dead_body
)
from novel.swallows.engine.events import Publisher
from novel.swallows.engine.objects import Location, ProperLocation, Male, Item, ProperContainer

# we extend the world of The Swallows by adding a new character.
# note that we have to inform the new character of certain important objects
# in the world are, so that he can react sensibly to them.
# (you *can* pass other objects here, for example 'revolver=brandy', in which
# case the character will act fairly nonsensibly, threatening other characters
# with the bottle of brandy and so forth)
fred = MaleCharacter('弗雷德')
fred.configure_objects(
    revolver=revolver,
    brandy=brandy,
    dead_body=dead_body,
)

# we extend the world by adding new locations and objects
# note that locations exited-to and from must be imported from swallows.story.world (above)
# "Location" is imported from swallows.engine.objects
freds_office = ProperLocation("<*> 办公室", owner=fred)
freds_office.set_exits(upstairs_hall)

upstairs_hall.set_exits(freds_office)  # adds to existing (unknown) exits

# we extend the world by adding some Objects
# "ProperContainer" and "Item" are imported from swallows.engine.objects
desk = ProperContainer("<*> 书桌", owner=fred, location=freds_office)
pencils = Item('铅笔盒', location=desk)

# ## main ## #

publisher = Publisher(
    characters=(
        alice,
        bob,
        fred,
    ),
    setting=house,
    title="我的飞飞",
    # debug=True,
)
publisher.publish()
