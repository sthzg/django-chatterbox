# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from chatterbox import events, registry


class UserSavesSomemodelEvent(events.ChatterboxMailEvent):
    originator = 'demoapp'
    event = 'User saves somemodel'
    template_subject = 'demoapp/email_subject.jinja'
    template_body = 'demoapp/email_body.jinja'
    mail_to = 'foo@example.com'
    languages = ['en', 'de']
    token_fields = (
        'actor.username',
        'obj.title',
        'obj.body',
        'obj.aprop'
    )
    # TODO(sthzg) Support metadata fields.
    # metadata_fields = (
    #     'actor.pk',
    #     'obj.pk',
    # )


registry.register(UserSavesSomemodelEvent)
