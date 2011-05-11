# -*- coding: utf-8 -*-
import datetime






class Field(object):
    pass


class Boolean(Field):
    pass


class Integer(Field, int):
    pass


class Float(Field, float):
    pass


class Binary(Field, bytes):
    pass


class Unicode(Field, unicode):
    pass


class List(Field, list):
    pass


class Document(Field, dict):
    pass


class DateTime(Field, datetime.datetime):
    pass


FIELDS = {
        bool: Boolean,
        int: Integer,
        float: Float,
        bytes: Binary,
        str: Binary,
        unicode: Unicode,
        list: List,
        dict: Document,
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
