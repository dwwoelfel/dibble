# -*- coding: utf-8 -*-
from . import fields
from .update import Update


class ModelError(Exception): pass
class UnboundModelError(ModelError): pass
class UnsavedModelError(ModelError): pass
class UndefinedFieldError(KeyError): pass


class ModelBase(object):
    _id = fields.Field()

    def __init__(self, *arg, **kw):
        initial = dict(*arg, **kw)
        self._update = Update()
        self._fields = {}
        self._mapper = None

        for k in dir(self):
            v = getattr(self, k)

            if isinstance(v, fields.UnboundField):
                if k in initial:
                    bound = v.bind(k, self, initial[k])

                else:
                    bound = v.bind(k, self)

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


    def bind(self, mapper):
        self._mapper = mapper


    def reload(self):
        if not self._mapper:
            raise UnboundModelError()

        if not self._id.defined:
            raise UnsavedModelError()

        new = self._mapper.find_one({'_id': self._id.value})

        for name, field in new._fields.items():
            if name in self._fields:
                self._fields[name]._reinit(field.value)


    def save(self, *arg, **kw):
        if not self._mapper:
            raise UnboundModelError()

        if self._id.defined:
            doc = dict(self)
            upd = dict(self._update)
            oid = doc.get('_id', None)
            self._mapper.update({'_id': oid}, upd, *arg, **kw)


        else:
            doc = dict(self)
            oid = self._mapper.save(doc, *arg, **kw)
            self._id._reinit(oid)

        self._update.clear()

        return oid



class Model(ModelBase):
    pass
