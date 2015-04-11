# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


_registry = dict()


def register(cls):
    _registry.update({'{}: {}'.format(cls.originator, cls.event): cls})


def get_registry():
    return _registry


def clear_registry():
    _registry.clear()
