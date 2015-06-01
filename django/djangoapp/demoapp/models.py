# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Somemodel(models.Model):
    class Meta:
        verbose_name = _('some model')
        verbose_name_plural = _('some models')

    title = models.CharField(
        _('title'),
        max_length=100
    )

    body = models.TextField(
        _('body')
    )

    def aprop(self):
        return 'I am aprop'

    property(aprop)

    def __unicode__(self):
        return '{}'.format(self.title)
