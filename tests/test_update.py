# -*- coding: utf-8 -*-
from nose.tools import raises
import dibble.update


@raises(dibble.update.DuplicateFieldError)
def test_fielddict_duplicate():
    fd = dibble.update.FieldDict()
    fd['foo'] = 'bar'
    fd['foo'] = 'baz'


@raises(NotImplementedError)
def test_fielddict_update():
    fd = dibble.update.FieldDict()
    fd.update({'foo': 'bar'})


@raises(dibble.update.InvalidOperatorError)
def test_opdict_invalidoperator():
    ops = dibble.update.OperatorDict()
    ops['$fumm'] = {'foo': 'bar'}


@raises(NotImplementedError)
def test_opdict_update():
    fd = dibble.update.OperatorDict()
    fd.update({'foo': 'bar'})
