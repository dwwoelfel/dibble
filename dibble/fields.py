# -*- coding: utf-8 -*-
"""
"""
import collections
from dibble.operations import (SetMixin, IncrementMixin, RenameMixin, UnsetMixin, PushMixin, PushAllMixin, AddToSetMixin, PopMixin, PullMixin, PullAllMixin)


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


class Field(SetMixin, IncrementMixin, RenameMixin, UnsetMixin, PushMixin, PushAllMixin, AddToSetMixin, PopMixin, PullMixin, PullAllMixin):
    __metaclass__ = FieldMeta

    def __init__(self, default=undefined, name=None, initial=undefined, model=None):
        self._default = default
        self._value = (initial if initial is not undefined else self.default)
        self.name = name
        self.model = model
        self.initial = initial


    def __call__(self):
        return self._value


    @property
    def defined(self):
        return (self._value is not undefined)


    @property
    def default(self):
        return (self._default() if isinstance(self._default, collections.Callable) else self._default)


    @property
    def value(self):
        return self._value


    def _reinit(self, value):
        self.initial = value
        self.reset()


    def reset(self):
        self._value = (self.initial if self.initial is not undefined else self.default)
        self.model._update.drop_field(self.name)


