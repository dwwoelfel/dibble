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


def test_inheritance():
    class InheritedModel(SimpleModel):
        xbool = unicode
        xint = unicode
        xfloat = unicode
        xbytes = unicode
        xunicode = bool
        xlist = unicode
        xdict = unicode
        #xdatetime = unicode

        ybool = bool
        yint = int
        yfloat = float
        ybytes = bytes
        yunicode = unicode
        ylist = list
        ydict = dict
        #ydatetime = datetime


    m = InheritedModel()
    assert isinstance(m.xbool, dibble.fields.Unicode)
    assert isinstance(m.xint, dibble.fields.Unicode)
    assert isinstance(m.xfloat, dibble.fields.Unicode)
    assert isinstance(m.xbytes, dibble.fields.Unicode)
    assert isinstance(m.xunicode, dibble.fields.Bool)
    assert isinstance(m.xlist, dibble.fields.Unicode)
    assert isinstance(m.xdict, dibble.fields.Unicode)
    #assert isinstance(m.xdatetime, dibble.fields.Unicode)

    assert isinstance(m.ybool, dibble.fields.Bool)
    assert isinstance(m.yint, dibble.fields.Int)
    assert isinstance(m.yfloat, dibble.fields.Float)
    assert isinstance(m.ybytes, dibble.fields.Bytes)
    assert isinstance(m.yunicode, dibble.fields.Unicode)
    assert isinstance(m.ylist, dibble.fields.List)
    assert isinstance(m.ydict, dibble.fields.Dict)
    #assert isinstance(m.ydatetime, dibble.fields.DateTime)


def test_update():
    class TestModel(dibble.model.Model):
        counter = int

    m = TestModel()
    m.counter.inc(1)
