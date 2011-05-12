# -*- coding: utf-8 -*-
"""
"""


class SetMixin(object):
    def set(self, value):
        self.model.update.set(self.name, value)
        self.value = value


class IncrementMixin(object):
    def inc(self, increment):
        self.model.update.inc(self.name, increment)
        self.value += increment


class RenameMixin(object):
    def rename(self, new):
        self.model.update.rename(self.name, new)
