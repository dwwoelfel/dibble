# -*- coding: utf-8 -*-
from pymongo.cursor import Cursor as PymongoCursor


class ModelCursor(PymongoCursor):
    def __init__(self, mapper, *arg, **kw):
        super(ModelCursor, self).__init__(*arg, **kw)
        self.mapper = mapper


    def __getitem__(self, key):
        doc = super(ModelCursor, self).__getitem__(key)

        instance = self.mapper.model(doc)
        instance.bind(self.mapper)

        return instance


    def next(self):
        doc = super(ModelCursor, self).next()

        instance = self.mapper.model(doc)
        instance.bind(self.mapper)

        return instance


class ModelMapper(object):
    def __init__(self, model, collection):
        self.model = model
        self.collection = collection


    def __call__(self, *arg, **kw):
        doc = self.model(*arg, **kw)
        doc.bind(self)
        return doc


    def count(self):
        return self.collection.count()


    def find(self, spec=None, *args, **kw):
        spec = spec or {}

        return ModelCursor(self, self.collection, spec, *args, **kw)


    def find_one(self, spec=None, *arg, **kw):
        spec = spec or {}
        doc = self.collection.find_one(spec, *arg, **kw)

        if doc:
            doc = self.model(doc)
            doc.bind(self)

        return doc


    def update(self, spec, doc, *arg, **kw):
        return self.collection.update(spec, doc, *arg, **kw)


    def save(self, doc, *arg, **kw):
        return self.collection.save(doc, *arg, **kw)

