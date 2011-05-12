# -*- coding: utf-8 -*-
from nose.tools import raises, eq_
import dibble.fields
import dibble.model


class TestModel(dibble.model.Model):
    counter = dibble.fields.Field(default=1)


def test_set():
    m = TestModel()
    m.counter.set(2)

    eq_(dict(m.update), {'$set': {'counter': 2}})
    eq_(m.counter.value, 2)


def test_increment():
    m = TestModel()
    m.counter.inc(1)

    eq_(dict(m.update), {'$inc': {'counter': 1}})
    eq_(m.counter.value, 2)


@raises(TypeError)
def test_increment_unset():
    class UnsetTestModel(dibble.model.Model):
        counter = dibble.fields.Field()

    m = UnsetTestModel()
    m.counter.inc(1)
