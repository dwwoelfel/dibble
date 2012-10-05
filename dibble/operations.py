# -*- coding: utf-8 -*-
"""
"""
import collections
import functools


class UnknownFieldError(KeyError): pass
class DuplicateFieldError(KeyError): pass


def reloading(fn):
    @functools.wraps(fn)
    def wrapper(self, *arg, **kw):
        self._reload(force=False)
        return fn(self, *arg, **kw)

    return wrapper



class SetMixin(object):
    @reloading
    def set(self, value):
        self._setvalue(value)
        self.model._update.set(self.name, value)


class IncrementMixin(object):
    @reloading
    def inc(self, increment):
        if self.defined:
            self._setvalue(self._value + increment)

        else:
            self._setvalue(increment)

        self.model._update.inc(self.name, increment)


class RenameMixin(object):
    def rename(self, new):
        # TODO: this is a relatively naive implementation, extend if more is needed
        import dibble.fields

        f = getattr(self.model, self.name, None)

        if isinstance(f, dibble.fields.Field):
            if hasattr(self.model, new):
                raise DuplicateFieldError('Field {0!r} is already present on Model'.format(new))

            else:
                oldname = self.name
                delattr(self.model, self.name)
                setattr(self.model, new, f)
                f._name = new
                self.model._update.rename(oldname, new)

        else:
            raise UnknownFieldError('Unknown Field: {0!r}'.format(self.name))


class UnsetMixin(object):
    @reloading
    def unset(self):
        # TODO: this is a relatively naive implementation, extend if more is needed
        import dibble.fields

        f = getattr(self.model, self.name, None)

        if isinstance(f, dibble.fields.Field):
            self._setvalue(dibble.fields.undefined)
            self.model._update.unset(self.name)

        else:
            raise UnknownFieldError('Unknown Field: {0!r}'.format(self.name))


class PushMixin(object):
    @reloading
    def push(self, value):
        if self.defined:
            self._setvalue(self._value + [value])

        else:
            self._setvalue([value])

        self.model._update.push(self.name, value)


class PushAllMixin(object):
    @reloading
    def push_all(self, values):
        if self.defined:
            self._setvalue(self._value + values)

        else:
            self._setvalue(values[:])

        self.model._update.pushAll(self.name, values)


class AddToSetMixin(object):
    @reloading
    def add_to_set(self, value):
        newvalue = (self._value[:] if self.defined else [])

        if isinstance(value, collections.Mapping) and ('$each' in value):
            for v in value['$each']:
                if not v in newvalue:
                    newvalue.append(v)

        else:
            if not value in newvalue:
                newvalue.append(value)

        self._setvalue(newvalue)
        self.model._update.addToSet(self.name, value)


class PopMixin(object):
    @reloading
    def pop(self, first=False):
        if first:
            self._setvalue(self._value[1:])

        else:
            self._setvalue(self._value[:-1])

        self.model._update.pop(self.name, first)


class PullMixin(object):
    @reloading
    def pull(self, value):
        if isinstance(value, dict):
            raise NotImplementedError('using pull() with a match criteria is not supported')

        else:
            self._setvalue([x for x in self._value if x != value])

        self.model._update.pull(self.name, value)


class PullAllMixin(object):
    @reloading
    def pull_all(self, values):
        self._setvalue([x for x in self._value if (x not in values)])
        self.model._update.pullAll(self.name, values)
