# -*- coding: utf-8 -*-
import uuid
from nose.tools import eq_, assert_not_equal
import dibble.fields
import dibble.model


def test_unbound():
    f = dibble.fields.Field()
    assert isinstance(f, dibble.fields.UnboundField)


def test_bind():
    fakemodel = object()
    f = dibble.fields.Field()
    bound = f.bind(name='foo', model=fakemodel)
    assert bound.model is fakemodel


def test_field_call():
    fakemodel = object()
    f = dibble.fields.Field()
    bf = f.bind(name='foo', model=fakemodel, initial=5)

    eq_(bf.value, 5)
    eq_(bf(), 5)


def test_field_reset():
    model = dibble.model.Model()
    f = dibble.fields.Field()
    bf = f.bind(name='foo', model=model, initial=5)
    bf.set(42)

    eq_(bf.value, 42)
    eq_(dict(model._update), {'$set': {'foo': 42}})

    bf.reset()

    eq_(bf.value, 5)
    eq_(dict(model._update), {})


def test_field_reset_default():
    model = dibble.model.Model()
    f = dibble.fields.Field(default=lambda: uuid.uuid4().hex)
    bf = f.bind(name='foo', model=model)
    v1 = bf.value

    bf.reset()

    v2 = bf.value

    assert_not_equal(v1, v2)


def test_field_reinit():
    model = dibble.model.Model()
    f = dibble.fields.Field()
    bf = f.bind(name='foo', model=model, initial=5)
    bf.set(42)

    eq_(bf.value, 42)
    eq_(dict(model._update), {'$set': {'foo': 42}})

    bf._reinit(42)

    eq_(bf.value, 42)
    eq_(dict(model._update), {})

    bf.reset()

    eq_(bf.value, 42)
    eq_(dict(model._update), {})


def test_field_reinit_default_undefined():
    model = dibble.model.Model()
    f = dibble.fields.Field(default=42)
    bf = f.bind(name='foo', model=model)

    eq_(bf.value, 42)
    bf._reinit(dibble.fields.undefined)

    eq_(bf.value, 42)
