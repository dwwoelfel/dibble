# -*- coding: utf-8 -*-
import pymongo
from nose import with_setup
from dibble.mapper import ModelMapper
from dibble.model import Model

DBNAME = 'dibbletest'


class UserModel(Model):
    username = unicode


def setup_db():
    con = pymongo.Connection()
    con.drop_database(DBNAME)


@with_setup(setup_db)
def test_modelmapper():
    db = pymongo.Connection()[DBNAME]
    users = ModelMapper(UserModel, db.user)

    assert users.count() == 0

    dummy_user = {'username': 'test'}
    users.save(dummy_user)

    assert users.count() == 1
    assert users.find_one() == dummy_user

