# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json
import logging
from django.core.mail import send_mail
from django.utils.datetime_safe import datetime

logger = logging.getLogger('chatterbox')


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

        if not mail_from or not mail_to or not subject:
            logger.error(
                'Message with pk {} can not be processed, since either '
                'mail_from: {}, mail_to: {} or subject: {} are empty'.format(
                    msg.pk,
                    mail_from,
                    mail_to,
                    subject
                )
            )
            return

        # TODO(sthzg) Proof of concept, make it fault tolerant
        # TODO(sthzg) Add logging
        send_mail(subject, body, mail_from, [mail_to])
        msg.is_done = True
        msg.done_at = datetime.now()
        msg.save()
