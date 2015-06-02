# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import uuid
from demoapp.chatter import UserSavesSomemodelEvent
from demoapp.models import Somemodel
from django.db.models.signals import post_save


def somemodel_saved(sender, **kwargs):
    inst = kwargs.get('instance')

    if hasattr(inst, 'current_user'):
        current_user = inst.current_user
    else:
        raise Exception("current_user is not available on instance.")

    ch = UserSavesSomemodelEvent()
    ch.mail_from = current_user.email
    ch.notify_chatterbox(
        languages=['de', 'en'],
        actor=current_user,
        obj=kwargs.get('instance'),
        natural_id=uuid.uuid4()
    )


post_save.connect(somemodel_saved, sender=Somemodel)
