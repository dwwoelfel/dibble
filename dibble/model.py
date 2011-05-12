# -*- coding: utf-8 -*-
from datetime import datetime
from . import fields
from .update import Update


class ModelError(Exception): pass
class UnboundModelError(ModelError): pass


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
                attrs[k] = a(k)

            else:
                attrs[k] = a(k, default)

        instance = type.__new__(cls, name, bases, attrs)

        return instance


class ModelBase(object):
    __metaclass__ = ModelMeta

    def __init__(self, *arg, **kw):
        self._update = Update()
        self._fields = {}
        self._mapper = None

        data = dict(*arg, **kw)
        # TODO: set values

        for k in dir(self):
            v = getattr(self, k)

            if isinstance(v, fields.UnboundField):
                bound = v.bind(self)
                setattr(self, k, bound)


    def bind(self, mapper):
        self._mapper = mapper


    def save(self, *arg, **kw):
        if not self._mapper:
            raise UnboundModelError()

        return self._mapper.save(self, *arg, **kw)



class Model(ModelBase):
    pass

