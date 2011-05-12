# -*- coding: utf-8 -*-
"""
"""
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
