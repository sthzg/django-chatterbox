# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from demoapp.models import Somemodel
from django.contrib import admin


class SomemodelAdmin(admin.ModelAdmin):
    list_display = ('title',)

    def save_model(self, request, obj, form, change):
        obj.current_user = request.user
        super(SomemodelAdmin, self).save_model(request, obj, form, change)

admin.site.register(Somemodel, SomemodelAdmin)
