# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json
from django.core.mail import send_mail


class EmailChannelMessageHandler(object):
    def __init__(self, message):
        self._message = message

    def process(self):
        msg = self._message

        channel_data = json.loads(msg.channel_data)
        content = json.loads(msg.content)

        mail_from = channel_data.get('from')
        mail_to = channel_data.get('to')
        subject = content.get('subject')
        body = content.get('body')

        send_mail(subject, body, mail_from, [mail_to])
