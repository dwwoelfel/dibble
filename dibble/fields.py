# -*- coding: utf-8 -*-
"""
"""
import collections
from dibble.operations import SetMixin, IncrementMixin, RenameMixin, UnsetMixin, PushMixin, PushAllMixin
from dibble.operations import AddToSetMixin, PopMixin, PullMixin, PullAllMixin


class InvalidatedSubfieldError(Exception):
    pass


# used for undefined defaults and initial values
undefined = type('Undefined', (object, ), {'__nonzero__': lambda s: False})()
# used for unknown values in reset-calls
unknown = type('Unknown', (object, ), {'__nonzero__': lambda s: False})()


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


class BaseField(object):
    __metaclass__ = FieldMeta

    def __init__(self, default=undefined, name=None, initial=undefined, model=None):
        self._default = default
        self._value = (initial if initial is not undefined else self.default)
        self._name = name
        self.model = model
        self.initial = initial

    def __call__(self):
        return self.value

    @property
    def name(self):
        return self._name

    @property
    def defined(self):
        return (self._value is not undefined)

    @property
    def default(self):
        return (self._default() if isinstance(self._default, collections.Callable) else self._default)

    @property
    def value(self):
        if self._name != '_id':
            self._reload(force=False)

        return (self._value if self.defined else None)

    def reset(self, value=unknown):
        if value is unknown:
            self._value = (self.initial if self.initial is not undefined else self.default)
            self.model._update.drop_field(self.name)

        else:
            self.initial = value
            self.reset()

    def _reload(self, *arg, **kw):
        self.model.reload(*arg, **kw)


class Field(BaseField, SetMixin, IncrementMixin, RenameMixin, UnsetMixin, PushMixin, PushAllMixin, AddToSetMixin,
            PopMixin, PullMixin, PullAllMixin):
    def __init__(self, default=undefined, name=None, initial=undefined, model=None):
        super(Field, self).__init__(default, name, initial, model)
        self._subfields = {}

    def _setvalue(self, value):
        self._value = value
        self._reset_subfields()

    def _reset_subfields(self):
        if self._subfields:
            if self._value is undefined:
                for field in self._subfields.values():
                    field.reset(undefined)

            elif isinstance(self._value, collections.Mapping):
                for key, field in self._subfields.items():
                    if key in self._value:
                        v = self._value[key]
                        field.reset(v)

                    else:
                        field._invalidate()

            else:
                for field in self._subfields.values():
                    field._invalidate()

                self._subfields.clear()

    def reset(self, value=unknown):
        super(Field, self).reset(value)

        if value is not unknown:
            self._reset_subfields()

    def subfield(self, key):
        if key not in self._subfields:
            sf = Subfield(parent=self)

            if self.defined:
                if isinstance(self._value, collections.Mapping):
                    if key in self._value:
                        sf_initial = self._value[key]
                        bsf = sf.bind(key, self.model, initial=sf_initial)

                    else:
                        bsf = sf.bind(key, self.model)

                else:
                    raise ValueError('Cannot create subfield for {0!r}'.format(self._value))

            else:
                bsf = sf.bind(key, self.model)

            self._subfields[key] = bsf

        return self._subfields[key]

    def __getitem__(self, item):
        return self.subfield(item)


class Subfield(Field):
    def __init__(self, default=undefined, name=None, initial=undefined, model=None, parent=None):
        super(Subfield, self).__init__(default=default, name=name, initial=initial, model=model)
        self.parent = parent

    @property
    def name(self):
        return '{0}.{1}'.format('.'.join(x._name for x in reversed(self.parents)), self._name)

    @property
    def parents(self):
        parentlist = []
        field = self.parent

        while field is not None:
            parentlist.append(field)
            field = getattr(field, 'parent', None)

        return parentlist

    def _setvalue(self, value):
        if self.parent is None:
            raise InvalidatedSubfieldError('Subfield {0!r} was invalidated by an update to it\'s '
                                           'parent Field.'.format(self._name))

        super(Subfield, self)._setvalue(value)

        parents = self.parents
        parent, key, v = parents[0], self._name, value

        while parent is not None:
            if parent.defined:
                parent._value[key] = v
                break

            parent._value = v = {key: v}
            key = parent._name
            parent = getattr(parent, 'parent', None)

    def _invalidate(self):
        self.parent = None
        self.model = None

    @property
    def value(self):
        if self.parent is None:
            raise InvalidatedSubfieldError('Subfield {0!r} was invalidated by an update to it\'s '
                                           'parent Field.'.format(self._name))

        return super(Subfield, self).value

    def _reload(self, *arg, **kw):
        if self.parent is None:
            raise InvalidatedSubfieldError('Subfield {0!r} was invalidated by an update to it\'s '
                                           'parent Field.'.format(self._name))

        return super(Subfield, self)._reload(*arg, **kw)
