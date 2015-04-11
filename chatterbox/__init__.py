# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from chatterbox import admin
from .chatterbox import register, get_registry, clear_registry

__all__ = [
    admin,
    register,
    get_registry,
    clear_registry
]
