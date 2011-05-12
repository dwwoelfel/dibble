# -*- coding: utf-8 -*-
from nose.tools import raises, eq_
import dibble.fields
import dibble.model
import dibble.operations


class TestModel(dibble.model.Model):
    counter = dibble.fields.Field(default=1)


def test_set():
    m = TestModel()
    m.counter.set(2)

    eq_(dict(m._update), {'$set': {'counter': 2}})
    eq_(m.counter.value, 2)


def test_increment():
    m = TestModel()
    m.counter.inc(1)

    eq_(dict(m._update), {'$inc': {'counter': 1}})
    eq_(m.counter.value, 2)


@raises(TypeError)
def test_increment_unset():
    class UnsetTestModel(dibble.model.Model):
        counter = dibble.fields.Field()

    m = UnsetTestModel()
    m.counter.inc(1)


def test_rename():
    class RenameTestModel(dibble.model.Model):
        field1 = dibble.fields.Field()

    m = RenameTestModel()
    f = m.field1
    m.field1.rename('field2')

    eq_(dict(m._update), {'$rename': {'field1': 'field2'}})
    eq_(m.field2.name, 'field2')
    assert m.field2 is f

    # FIXME: delattr makes the unbound field visible again, assertion will fail until this is fixed
    #assert not hasattr(m, 'field1')


@raises(dibble.operations.DuplicateFieldError)
def test_rename_errors():
    class RenameTestModel(dibble.model.Model):
        field1 = dibble.fields.Field()
        field2 = dibble.fields.Field()

    m = RenameTestModel()
    m.field1.rename('field2')


def test_unset():
    m = TestModel()
    m.counter.unset()

    eq_(dict(m._update), {'$unset': {'counter': 1}})

    # FIXME: delattr makes the unbound field visible again, assertion will fail until this is fixed
    #assert not hasattr(m, 'counter')
