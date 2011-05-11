# -*- coding: utf-8 -*-
import unittest
import dibble.fields
import dibble.model
from datetime import datetime


class SimpleModel(dibble.model.Model):
    xbool = bool
    xint = int
    xfloat = float
    xbytes = bytes
    xunicode = unicode
    xlist = list
    xdict = dict
    #xdatetime = datetime


def test_initialization():
    m = SimpleModel()
    assert isinstance(m.xbool, dibble.fields.Bool)
    assert isinstance(m.xint, dibble.fields.Int)
    assert isinstance(m.xfloat, dibble.fields.Float)
    assert isinstance(m.xbytes, dibble.fields.Bytes)
    assert isinstance(m.xunicode, dibble.fields.Unicode)
    assert isinstance(m.xlist, dibble.fields.List)
    assert isinstance(m.xdict, dibble.fields.Dict)
    #assert isinstance(m.xdatetime, dibble.fields.DateTime)


