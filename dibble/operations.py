# -*- coding: utf-8 -*-
"""
"""
import collections

undefined = object()

class UnknownFieldError(KeyError): pass
class DuplicateFieldError(KeyError): pass


class SetMixin(object):
    def set(self, value):
        self.model._update.set(self.name, value)
        self.value = value


class IncrementMixin(object):
    def inc(self, increment):
        self.model._update.inc(self.name, increment)
        self.value += increment


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
            delattr(self.model, self.name)
            self.model._update.unset(self.name)

        else:
            raise UnknownFieldError('Unknown Field: {0!r}'.format(self.name))


class PushMixin(object):
    def push(self, value):
        if self.defined:
            self.value.append(value)

        else:
            self.value = [value]

        self.model._update.push(self.name, value)


class PushAllMixin(object):
    def push_all(self, values):
        if self.defined:
            self.value.extend(values)

        else:
            self.value = [x for x in values]

        self.model._update.pushAll(self.name, values)


class AddToSetMixin(object):
    def add_to_set(self, value):
        if not self.defined:
            self.value = []

        if isinstance(value, collections.Mapping) and ('$each' in value):
            for v in value['$each']:
                if not v in self.value:
                    self.value.append(v)

        else:
            if not value in self.value:
                self.value.append(value)

        self.model._update.addToSet(self.name, value)
