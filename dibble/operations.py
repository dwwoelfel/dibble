# -*- coding: utf-8 -*-
"""
"""
import collections


class UnknownFieldError(KeyError): pass
class DuplicateFieldError(KeyError): pass


class SetMixin(object):
    def set(self, value):
        self._value = value
        self.model._update.set(self.name, value)


class IncrementMixin(object):
    def inc(self, increment):
        if self.defined:
            self._value += increment

        else:
            self._value = increment

        self.model._update.inc(self.name, increment)


class RenameMixin(object):
    def rename(self, new):
        # TODO: this is a relatively naive implementation, extend if more is needed
        import dibble.fields

        f = getattr(self.model, self.name)

        if isinstance(f, dibble.fields.Field):
            if hasattr(self.model, new):
                raise DuplicateFieldError('Field {0!r} is already present on Model'.format(new))

            else:
                oldname = self.name
                delattr(self.model, self.name)
                setattr(self.model, new, f)
                f.name = new
                self.model._update.rename(oldname, new)

        else:
            raise UnknownFieldError('Unknown Field: {0!r}'.format(self.name))


class UnsetMixin(object):
    def unset(self):
        # TODO: this is a relatively naive implementation, extend if more is needed
        import dibble.fields

        f = getattr(self.model, self.name)

        if isinstance(f, dibble.fields.Field):
            self._value = dibble.fields.undefined
            self.model._update.unset(self.name)

        else:
            raise UnknownFieldError('Unknown Field: {0!r}'.format(self.name))


class PushMixin(object):
    def push(self, value):
        if self.defined:
            self._value.append(value)

        else:
            self._value = [value]

        self.model._update.push(self.name, value)


class PushAllMixin(object):
    def push_all(self, values):
        if self.defined:
            self._value.extend(values)

        else:
            self._value = [x for x in values]

        self.model._update.pushAll(self.name, values)


class AddToSetMixin(object):
    def add_to_set(self, value):
        if not self.defined:
            self._value = []

        if isinstance(value, collections.Mapping) and ('$each' in value):
            for v in value['$each']:
                if not v in self._value:
                    self._value.append(v)

        else:
            if not value in self._value:
                self._value.append(value)

        self.model._update.addToSet(self.name, value)


class PopMixin(object):
    def pop(self, first=False):
        if first:
            self._value.pop(0)

        else:
            self._value.pop()

        self.model._update.pop(self.name, first)


class PullMixin(object):
    def pull(self, value):
        if isinstance(value, dict):
            raise NotImplementedError('using pull() with a match criteria is not supported')

        else:
            self._value = [x for x in self._value if x != value]

        self.model._update.pull(self.name, value)


class PullAllMixin(object):
    def pull_all(self, values):
        self._value = [x for x in self._value if (x not in values)]
        self.model._update.pullAll(self.name, values)
