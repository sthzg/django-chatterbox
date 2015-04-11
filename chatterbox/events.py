# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json
from collections import OrderedDict
from django.template import loader
from django.template.context import Context
from django.utils.datetime_safe import datetime
from .models import Message


class BaseChatterboxEvent(object):
    """
    """
    originator = None
    event = None
    actor = None
    target = None
    channel = None
    channel_data = dict()
    templates = OrderedDict()
    priority = 10
    extra = dict()
    tokens = None

    def __init__(self, *args, **kwargs):
        self._content = dict()

    def notify_chatterbox(self, actor=None, target=None, **kwargs):
        self.actor = actor or dict()
        self.target = target or dict()
        self.extra.update(kwargs.get('extra', dict()))
        self._content = self.build_content()
        self._save_message()

    def add_template(self, key, template_path):
        """ Adds a template to be collected when generating the event message.

        :param key: key for the template path, e.g. ``subject`` or ``body``
        :type key: str
        :param template_path: template path that can be resolved from Django
        :type template_path: str
        """
        self.templates[key] = template_path

    def add_channel_data(self, key, value):
        """ Adds a key-value pair with information that the channel needs to
        have to be usable, e.g. ``from`` and ``to`` for the email channel.

        :param key:
        :type key: str
        :param value:
        :type value: any
        """
        self.channel_data[key] = value

    def build_content(self):
        """ Returns a dictionary of the output from all configured templates.

        :return: dict of collected output as key => value
        :rtype: OrderedDict
        """
        content = OrderedDict()

        for key in self.templates:
            content[key] = self.render(self.templates.get(key))

        return content

    def render(self, template):
        t = loader.get_template(template)
        c = Context({
            'actor': self.actor,
            'event': self.event,
            'target': self.target,
            'extra': self.extra
        })

        return t.render(c)

    def _save_message(self):
        message = Message()
        message.originator = self.originator
        message.event = self.event
        message.content = json.dumps(self._content)
        message.channel = self.channel
        message.channel_data = json.dumps(self.channel_data)
        message.priority = self.priority
        message.scheduled_for = self.get_schedule()
        message.save()

    def get_schedule(self):
        return datetime.now()


class ChatterboxEvent(BaseChatterboxEvent):
    pass


class ChatterboxMailEvent(ChatterboxEvent):
    channel = 'email'
    mail_from = None
    mail_to = None
    template_subject = None
    template_body = None

    def __init__(self, *args, **kwargs):
        self.add_template('subject', self.template_subject)
        self.add_template('body', self.template_body)

        super(ChatterboxMailEvent, self).__init__(*args, **kwargs)

    def notify_chatterbox(self, actor=None, target=None, **kwargs):
        self.add_channel_data('from', self.mail_from)
        self.add_channel_data('to', self.mail_to)

        super(ChatterboxMailEvent, self).notify_chatterbox(
            actor, target, **kwargs)
