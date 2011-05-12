# -*- coding: utf-8 -*-
from nose.tools import eq_
import dibble.fields
import dibble.model


class SimpleModel(dibble.model.Model):
    xbool = dibble.fields.Field()
    xint = dibble.fields.Field()
    xfloat = dibble.fields.Field()
    xbytes = dibble.fields.Field()
    xunicode = dibble.fields.Field()
    xlist = dibble.fields.Field()
    xdict = dibble.fields.Field()


def test_initialization():
    cls = SimpleModel
    m = SimpleModel()

    assert isinstance(cls.xbool, dibble.fields.UnboundField)
    assert isinstance(cls.xint, dibble.fields.UnboundField)
    assert isinstance(cls.xfloat, dibble.fields.UnboundField)
    assert isinstance(cls.xbytes, dibble.fields.UnboundField)
    assert isinstance(cls.xunicode, dibble.fields.UnboundField)
    assert isinstance(cls.xlist, dibble.fields.UnboundField)
    assert isinstance(cls.xdict, dibble.fields.UnboundField)

    assert isinstance(m.xbool, dibble.fields.Field)
    assert isinstance(m.xint, dibble.fields.Field)
    assert isinstance(m.xfloat, dibble.fields.Field)
    assert isinstance(m.xbytes, dibble.fields.Field)
    assert isinstance(m.xunicode, dibble.fields.Field)
    assert isinstance(m.xlist, dibble.fields.Field)
    assert isinstance(m.xdict, dibble.fields.Field)


def test_inheritance():
    class InheritedModel(SimpleModel):
        ybool = dibble.fields.Field()
        yint = dibble.fields.Field()
        yfloat = dibble.fields.Field()
        ybytes = dibble.fields.Field()
        yunicode = dibble.fields.Field()
        ylist = dibble.fields.Field()
        ydict = dibble.fields.Field()


    m = InheritedModel()

    assert isinstance(m.xbool, dibble.fields.Field)
    assert isinstance(m.xint, dibble.fields.Field)
    assert isinstance(m.xfloat, dibble.fields.Field)
    assert isinstance(m.xbytes, dibble.fields.Field)
    assert isinstance(m.xunicode, dibble.fields.Field)
    assert isinstance(m.xlist, dibble.fields.Field)
    assert isinstance(m.xdict, dibble.fields.Field)

    assert isinstance(m.ybool, dibble.fields.Field)
    assert isinstance(m.yint, dibble.fields.Field)
    assert isinstance(m.yfloat, dibble.fields.Field)
    assert isinstance(m.ybytes, dibble.fields.Field)
    assert isinstance(m.yunicode, dibble.fields.Field)
    assert isinstance(m.ylist, dibble.fields.Field)
    assert isinstance(m.ydict, dibble.fields.Field)


def test_update():
    class TestModel(dibble.model.Model):
        counter = dibble.fields.Field()

    m = TestModel()
    m.counter.set(1)

    eq_(dict(m.update), {'$set': {'counter': 1}})

    m.counter.inc(1)

    eq_(dict(m.update), {'$set': {'counter': 1}, '$inc': {'counter': 1}})



def test_initial():
    class TestModel(dibble.model.Model):
        counter = dibble.fields.Field()

    m = TestModel(counter=5)
    eq_(m.counter.value, 5)

    m = TestModel({'counter': 10})
    eq_(m.counter.value, 10)


def test_default():
    class TestModel(dibble.model.Model):
        counter = dibble.fields.Field(default=100)

    m = TestModel()
    eq_(m.counter.value, 100)


def test_default_initial():
    class TestModel(dibble.model.Model):
        counter = dibble.fields.Field(default=100)

    m = TestModel({'counter': 5})
    eq_(m.counter.value, 5)
