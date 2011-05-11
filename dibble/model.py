# -*- coding: utf-8 -*-
from datetime import datetime
from . import fields


def public_attrs(attrs):
    return [x for x in attrs.items() if not x[0].startswith('__')]


class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        undefined = object()

        for k, v in public_attrs(attrs):
            # FIXME: naive split of tuple, needs more sane implementation
            if isinstance(v, tuple):
                v, default = v

            else:
                default = undefined

            a = fields.field(v)
            if a is None:
                pass

            elif default is undefined:
                attrs[k] = a()

            else:
                attrs[k] = a(default)

        instance = type.__new__(cls, name, bases, attrs)

        return instance


class ModelBase(object):
    __metaclass__ = ModelMeta

    @classmethod
    def field_wrapper(cls):
        print 'ModelBase', cls


class Model(ModelBase):
    pass
