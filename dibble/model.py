# -*- coding: utf-8 -*-
from datetime import datetime
from . import fields
from .update import Update


class ModelBase(object):
    def __init__(self, *arg, **kw):
        initial = dict(*arg, **kw)

        for k in dir(self):
            v = getattr(self, k)

            if isinstance(v, fields.UnboundField):
                if k in initial:
                    bound = v.bind(k, self, initial[k])

                else:
                    bound = v.bind(k, self)

                setattr(self, k, bound)

        self.update = Update()


class Model(ModelBase):
    pass
