# -*- coding: utf-8 -*-
from datetime import datetime




class Field(object):
    pass


class Bool(Field):
    pass


class Int(Field, int):
    pass


class Float(Field, float):
    pass


class Bytes(Field, bytes):
    pass


class Unicode(Field, unicode):
    pass


class List(Field, list):
    pass


class Dict(Field, dict):
    pass


class DateTime(Field, datetime):
    pass


FIELDS = {
        bool: Bool,
        int: Int,
        float: Float,
        bytes: Bytes,
        unicode: Unicode,
        list: List,
        dict: Dict,
        datetime: DateTime
        }


class InvalidFieldTypeError(KeyError):
    pass


def field(typ):
    if typ in FIELDS:
        f = FIELDS[typ]

    elif isinstance(typ, Field):
        f = typ

    else:
        f = None

    return f
