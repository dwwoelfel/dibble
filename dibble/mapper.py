# -*- coding: utf-8 -*-
from pymongo.cursor import Cursor as PymongoCursor


class ModelCursor(PymongoCursor):
    def __init__(self, model, *arg, **kw):
        super(ModelCursor, self).__init__(*arg, **kw)
        self.model = model

    def next(self):
        doc = super(ModelCursor, self).next()

        return self.model(doc.to_dict())


class ModelMapper(object):
    def __init__(self, model, collection):
        self.model = model
        self.collection = collection


    def __call__(self, *arg, **kw):
        return self.model(*arg, **kw)


    def count(self):
        return self.collection.count()


    def find(self, spec=None, *args, **kw):
        spec = spec or {}

        return ModelCursor(self.model, self.collection, *args, **kw)


    def find_one(self, spec=None, *arg, **kw):
        spec = spec or {}
        doc = self.collection.find_one(spec, *arg, **kw)

        if doc:
            doc = self.model(doc)

        return doc


    def save(self, doc, *arg, **kw):
        return self.collection.save(doc, *arg, **kw)

