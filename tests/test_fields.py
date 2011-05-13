# -*- coding: utf-8 -*-
from nose.tools import eq_
import dibble.fields


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
