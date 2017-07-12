#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import arrow

open("d:/test_" + str(arrow.now().timestamp) + ".txt", 'w').write(str(111))
open("d:/cctest.txt", 'w').write(str(111));

td = {'lastTime': u'2015-10-26 21:08:18' + u'+08:00'}
print arrow.get(td['lastTime'])
print arrow.get(td['lastTime']).timestamp
print arrow.now()
print arrow.now().timestamp

print (arrow.now().timestamp - arrow.get(td['lastTime']).timestamp) / 3600
print (arrow.now().timestamp - arrow.get(td['lastTime']).timestamp) > 48 * 3600
print ''.join(str(time.time()).split('.', 1)) + '0'
