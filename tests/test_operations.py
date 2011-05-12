# -*- coding: utf-8 -*-
from nose.tools import raises, eq_
import dibble.fields
import dibble.model
import dibble.operations


class TestModel(dibble.model.Model):
    counter = dibble.fields.Field(default=1)


class ListFieldTestModel(dibble.model.Model):
    tags = dibble.fields.Field()


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


def test_push():
    m = ListFieldTestModel()
    m.tags.push('fumm')

    eq_(dict(m._update), {'$push': {'tags': 'fumm'}})
    eq_(m.tags.value, ['fumm'])

    m = ListFieldTestModel(tags=['foo', 'bar'])
    m.tags.push('baz')

    eq_(dict(m._update), {'$push': {'tags': 'baz'}})
    eq_(m.tags.value, ['foo', 'bar', 'baz'])


def test_push_all():
    m = ListFieldTestModel()
    m.tags.push_all(['fumm', 'fnorb'])

    eq_(dict(m._update), {'$pushAll': {'tags': ['fumm', 'fnorb']}})
    eq_(m.tags.value, ['fumm', 'fnorb'])

    m = ListFieldTestModel(tags=['foo'])
    m.tags.push_all(['bar', 'baz'])

    eq_(dict(m._update), {'$pushAll': {'tags': ['bar', 'baz']}})
    eq_(m.tags.value, ['foo', 'bar', 'baz'])


def test_add_to_set():
    m = ListFieldTestModel(tags=['foo'])
    m.tags.add_to_set('foo')

    eq_(dict(m._update), {'$addToSet': {'tags': 'foo'}})
    eq_(m.tags.value, ['foo'])

    m = ListFieldTestModel()
    m.tags.add_to_set('foo')

    eq_(dict(m._update), {'$addToSet': {'tags': 'foo'}})
    eq_(m.tags.value, ['foo'])

    m = ListFieldTestModel(tags=['foo'])
    m.tags.add_to_set({'$each': ['foo', 'bar', 'baz']})

    eq_(dict(m._update), {'$addToSet': {'tags': {'$each': ['foo', 'bar', 'baz']}}})
    eq_(m.tags.value, ['foo', 'bar', 'baz'])


def test_pop():
    m = ListFieldTestModel(tags=['foo', 'bar'])
    m.tags.pop()

    eq_(dict(m._update), {'$pop': {'tags': 1}})
    eq_(m.tags.value, ['foo'])

    m = ListFieldTestModel(tags=['foo', 'bar'])
    m.tags.pop(first=True)

    eq_(dict(m._update), {'$pop': {'tags': -1}})
    eq_(m.tags.value, ['bar'])


def test_pull():
    m = ListFieldTestModel(tags=['foo', 'bar', 'baz'])
    m.tags.pull('bar')

    eq_(dict(m._update), {'$pull': {'tags': 'bar'}})
    eq_(m.tags.value, ['foo', 'baz'])

    m = ListFieldTestModel(tags=['foo', 'bar', 'baz', 'baz', 'bar', 'baz', 'foo'])
    m.tags.pull('baz')

    eq_(dict(m._update), {'$pull': {'tags': 'baz'}})
    eq_(m.tags.value, ['foo', 'bar', 'bar', 'foo'])


@raises(NotImplementedError)
def test_pull_criteria():
    m = ListFieldTestModel(tags=['foo', 'bar', 'baz'])
    m.tags.pull({'$nin': ['foo', 'bar']})


def test_pull_all():
    m = ListFieldTestModel(tags=['foo', 'bar', 'baz'])
    m.tags.pull_all(['foo', 'bar'])

    eq_(dict(m._update), {'$pullAll': {'tags': ['foo', 'bar']}})
    eq_(m.tags.value, ['baz'])
