# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.contrib import admin
from chatterbox.models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'scheduled_for',
        'originator',
        'event',
        'channel',
        'is_done',
        'done_at',
        'priority',
        'should_cancel',
        'created',
    )

    def has_add_permission(self, request):
        return False


admin.site.register(Message, MessageAdmin)