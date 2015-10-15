 # -*- coding:utf-8 -*-

from storm.locals import Unicode, Int, DateTime

class User(object):
    id = Int(Primary=True)
    username = Unicode(allow_none)
    address = Unicode()
