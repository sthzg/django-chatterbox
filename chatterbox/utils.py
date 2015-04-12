# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


def digattr(obj, attr, default=None):
    """Perform template-style dotted lookup

    Function is taken from https://github.com/funkybob/django-nap,
    (c) Curtis Maloney. Thanks @FunkyBob for the hint to this solution.

    """
    steps = attr.split('.')
    for step in steps:
        try:    # dict lookup
            obj = obj[step]
        except (TypeError, AttributeError, KeyError):
            try:    # attribute lookup
                obj = getattr(obj, step)
            except (TypeError, AttributeError):
                try:    # list index lookup
                    obj = obj[int(step)]
                except (IndexError, ValueError, KeyError, TypeError):
                    return default
        if callable(obj) and not getattr(obj, 'do_not_call_in_templates', False):
            obj = obj()
    return obj
