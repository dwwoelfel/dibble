# -*- coding: utf-8 -*-
"""
"""
import datetime
from .operations import IncrementMixin


class FieldMeta(type):
    def __call__(cls, *arg, **kw):
        if 'model' in kw:
            print 'call:', cls, arg, kw
            return type.__call__(cls, *arg, **kw)

        return UnboundField(cls, *arg, **kw)


class UnboundField(object):
    def __init__(self, field_class, *arg, **kw):
        self.field_class = field_class
        self.arg = arg
        self.kw = kw

    def bind(self, model):
        return self.field_class(model=model, *self.arg, **self.kw)


class Field(object):
    __metaclass__ = FieldMeta

    def __init__(self, name, default=None, model=None):
        self.name = name
        self.model = model
        self.default = default


class Bool(Field):
    pass


class Int(Field, IncrementMixin, int):
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


class DateTime(Field, datetime.datetime):
    pass


FIELDS = {
        bool: Bool,
        int: Int,
        float: Float,
        bytes: Bytes,
        unicode: Unicode,
        list: List,
        dict: Dict,
        datetime.datetime: DateTime
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
