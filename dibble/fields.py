# -*- coding: utf-8 -*-
"""
"""
from .operations import (SetMixin, IncrementMixin, RenameMixin)


undefined = object()


class FieldMeta(type):
    def __call__(cls, *arg, **kw):
        if 'model' in kw:
            return type.__call__(cls, *arg, **kw)

        return UnboundField(cls, *arg, **kw)


class UnboundField(object):
    def __init__(self, field_class, *arg, **kw):
        self.field_class = field_class
        self.arg = arg
        self.kw = kw

    def bind(self, name, model, initial=undefined):
        return self.field_class(name=name, model=model, initial=initial, *self.arg, **self.kw)


class Field(SetMixin, IncrementMixin, RenameMixin):
    __metaclass__ = FieldMeta

    def __init__(self, default=undefined, name=None, initial=undefined, model=None):
        self.name = name
        self.model = model
        self.default = default
        self.value = (initial if initial is not undefined else default)



class Bool(Field):
    pass


class Int(Field, IncrementMixin):
    pass


class Float(Field):
    pass


class Bytes(Field):
    pass


class Unicode(Field):
    pass


class List(Field):
    pass


class Dict(Field):
    pass


class DateTime(Field):
    pass
