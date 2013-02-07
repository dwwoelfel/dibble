# -*- coding: utf-8 -*-
import pymongo
from . import fields
from .update import Update


class ModelError(Exception):
    pass


class UnboundModelError(ModelError):
    pass


class UnsavedModelError(ModelError):
    pass


class UndefinedFieldError(KeyError):
    pass


class ModelBase(object):
    _id = fields.Field()

    def __init__(self, *arg, **kw):
        initial = dict(*arg, **kw)
        self._update = Update()
        self._fields = {}
        self._mapper = None
        self._requires_reload = False

        for k in dir(self):
            # lookup in class to avoid triggering property evaluation
            v = getattr(self.__class__, k, None)

            if isinstance(v, fields.UnboundField):
                field = getattr(self, k)

                if k in initial:
                    bound = field.bind(k, self, initial[k])

                else:
                    bound = field.bind(k, self)

                setattr(self, k, bound)
                self._fields[k] = bound

    def __iter__(self):
        for name, field in self._fields.iteritems():
            if field.defined:
                yield (name, field.value)

    def __getitem__(self, key):
        field = self._fields[key]

        if field.defined:
            return self._fields[key].value

        raise UndefinedFieldError('Field {0!r} is not defined.'.format(key))

    def __repr__(self):
        return '<{0}({1!r})>'.format(self.__class__.__name__, dict(self))

    @property
    def is_new(self):
        return not self._id.defined

    def bind(self, mapper):
        self._mapper = mapper

    def reload(self, force=True):
        if self._requires_reload or force:
            if not self._mapper:
                raise UnboundModelError()

            if not self._id.defined:
                raise UnsavedModelError()

            new = self._mapper.find_one({'_id': self._id.value}, slave_ok=False,
                                        read_preference=pymongo.ReadPreference.PRIMARY)

            for name, field in new._fields.items():
                if name in self._fields:
                    self._fields[name].reset(field._value)

            self._requires_reload = False

    def save(self, *arg, **kw):
        if not self._mapper:
            raise UnboundModelError()

        kw.setdefault('safe', True)
        self._requires_reload = False

        if self.is_new:
            doc = dict(self)

            if '_id' in kw:
                #TODO: Test
                doc['_id'] = kw.pop('_id')

            kw['safe'] = True

            oid = self._mapper.save(doc, *arg, **kw)
            self._id.reset(oid)

        else:
            doc = dict(self)
            upd = dict(self._update)
            oid = doc.get('_id', None)

            # do not perform update with empty update document as
            # this would overwrite/clear existing data
            if upd:
                self._mapper.update({'_id': oid}, upd, *arg, **kw)

        self._update.clear()
        self._requires_reload = True

        return oid


class Model(ModelBase):
    pass
