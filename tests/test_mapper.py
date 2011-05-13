# -*- coding: utf-8 -*-
from nose.tools import eq_, assert_dict_contains_subset
import pymongo
from nose import with_setup
from dibble.fields import Field
from dibble.mapper import ModelMapper
from dibble.model import Model

DBNAME = 'dibbletest'


class UserModel(Model):
    name = Field()


class AdvancedUserModel(Model):
    logincount = Field()
    username = Field()
    usernames = Field()


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
def test_modelmapper_new():
    users = get_mapper()

    username = 'testuser'
    user = users(name=username)

    eq_(user['name'], username)
    eq_(user.name.value, username)


@with_setup(setup_db)
def test_modelmapper_count():
    mapper = get_mapper()
    eq_(mapper.count(), 0)


@with_setup(setup_db)
def test_modelmapper_save_and_find_one():
    users = get_mapper()

    dummy_user = {'name': 'test'}
    users.save(dummy_user)

    eq_(users.count(), 1)


@with_setup(setup_db)
def test_find_generator():
    users = get_mapper()

    dummy_user = {'name': 'test'}
    users.save(dummy_user)

    cursor = users.find({'name': dummy_user['name']})

    eq_(cursor.count(), 1)

    db_user = list(cursor)[0]

    eq_(db_user.name.value, dummy_user['name'])
    eq_(db_user['name'], dummy_user['name'])



@with_setup(setup_db)
def test_find_getitem():
    users = get_mapper()

    dummy_user = {'name': 'test'}
    users.save(dummy_user)

    cursor = users.find({'name': dummy_user['name']})

    eq_(cursor.count(), 1)

    db_user = cursor[0]

    eq_(db_user.name.value, dummy_user['name'])
    eq_(db_user['name'], dummy_user['name'])



@with_setup(setup_db)
def test_modelmapper_model_save():
    db = get_db()
    users = ModelMapper(AdvancedUserModel, db.user)

    user = users()
    user.logincount.inc(1)
    user.username.set('Foo Bar')
    user.usernames.push('Foo Bar')
    user.save()

    u = dict(users.collection.find_one())
    expected = {'logincount': 1, 'username': 'Foo Bar', 'usernames': ['Foo Bar']}

    assert_dict_contains_subset(expected, u)

    users.collection.update({}, {'$set': {'username': 'Fumm Fumm'}})

    user.logincount.inc(41)
    user.save()

    u = dict(users.collection.find_one())
    expected = {'logincount': 42, 'username': 'Fumm Fumm', 'usernames': ['Foo Bar']}

    assert_dict_contains_subset(expected, u)
