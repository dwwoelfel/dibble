# -*- coding: utf-8 -*-
import dibble.fields


def test_unbound():
    f = dibble.fields.Field()
    assert isinstance(f, dibble.fields.UnboundField)


def test_bind():
    fakemodel = object()
    f = dibble.fields.Field()
    bound = f.bind(name='foo', model=fakemodel)
    assert bound.model is fakemodel
