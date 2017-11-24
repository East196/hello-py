#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Example of extending _The Swallows_ world to produce a different story.
#

import sys

reload(sys)
sys.setdefaultencoding('utf8')
# Example of using _The Swallows_ engine, but not its world,
# to produce a different story.
#

import sys
from os.path import realpath, dirname, join

# get the ../src/ directory onto the Python module search path
sys.path.insert(0, join(dirname(realpath(sys.argv[0])), '..', 'src'))

# now we can:
from novel.swallows import Publisher
from novel.swallows import Location, ProperLocation, Male

### world ###

main_street = ProperLocation("大街", noun="街道")
butchers = Location("肉店", noun="商店")
bakery = Location("面包店", noun="商店")
candlestick_factory = Location("蜡烛厂", noun="建筑")

main_street.set_exits(butchers, bakery, candlestick_factory)
butchers.set_exits(main_street)
bakery.set_exits(main_street)
candlestick_factory.set_exits(main_street)

downtown = (main_street, butchers, bakery, candlestick_factory)


class Tweedle(Male):
    def live(self):
        self.wander()


tweedledee = Tweedle('天使特警')
tweedledum = Tweedle('特威德尔德姆')

# ## main ## #

publisher = Publisher(
    characters=(
        tweedledee,
        tweedledum,
    ),
    setting=downtown,
    title="恐怖故事",
    # debug=True,
)
publisher.publish()
