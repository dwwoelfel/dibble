# -*- coding: utf-8 -*-
"""
"""


class IncrementMixin(object):
    def inc(self, increment):
        self.model.update.inc(self.name, increment)


class RenameMixin(object):
    def rename(self, new):
        self.model.update.rename(self.name, new)
