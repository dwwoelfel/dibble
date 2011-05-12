# -*- coding: utf-8 -*-
"""
"""


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
        self.model._update.rename(self.name, new)
