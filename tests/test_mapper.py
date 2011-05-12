# -*- coding: utf-8 -*-
from nose.tools import eq_
import pymongo
from nose import with_setup
from dibble.fields import Field
from dibble.mapper import ModelMapper
from dibble.model import Model

DBNAME = 'dibbletest'


class UserModel(Model):
    name = Field()


def get_db():
    con = pymongo.Connection()

    return con[DBNAME]


def get_mapper():
    db = get_db()

    return ModelMapper(UserModel, db.user)


def setup_db():
    db = get_db()
    db.connection.drop_database(DBNAME)


@with_setup(setup_db)
def test_modelmapper():
    users = get_mapper()

    assert users.count() == 0

    dummy_user = {'name': 'test'}
    users.save(dummy_user)

    eq_( users.count(), 1)
    eq_(users.find_one(), dummy_user)

    username = 'testuser'
    user = users(name=username)

    eq_(user.name.value, username)
