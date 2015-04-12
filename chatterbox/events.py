# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json
from collections import OrderedDict
from django.template import loader
from django.template.context import Context
from django.utils.datetime_safe import datetime
from .models import Message


class BaseChatterboxEvent(object):
    """ Provides basic interface and functionality of a chatterbox event.

    The main purpose of chatterbox events is to provide a declarative
    interface to library users. ``BaseChatterboxEvent`` is expected to be
    extended by concrete implementations, e.g. the ``ChatterboxMailEvent``.
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

    # TODO(sthzg) validate given attributes on __init__ time.

    def __init__(self, *args, **kwargs):
        self._content = dict()

    def notify_chatterbox(self, actor=None, target=None, **kwargs):
        """ Persists current event on the ``Message`` model.

        The optional arguments ``actor`` and ``target`` will be automatically
        passed to the templates that render the content.

        :param actor:
        :param target:
        :param kwargs:
        """
        # TODO(sthzg) validate given attributes on notify_chatterbox time.
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
        """ Renders content output by using ``template``.

        :param template: path to template that needs to be resolvable by Django
        :type template: str
        :return: rendered output
        :rtype: str
        """
        t = loader.get_template(template)
        c = Context({
            'actor': self.actor,
            'event': self.event,
            'target': self.target,
            'extra': self.extra
        })

        return t.render(c)

    def _save_message(self):
        """ Saves the event on the ``Message`` model.
        """
        # TODO(sthzg) exception handling
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
        """ Returns the due date of the message.

        The due date is a ``datetime`` object of the earliest allowed time
        to process the message, e.g. the earliest allowed time to send an
        email in case of a ``ChatterboxMailEvent``.

        :return: due date of the message
        :rtype: datetime
        """
        return datetime.now()


class ChatterboxEvent(BaseChatterboxEvent):
    pass


class ChatterboxMailEvent(ChatterboxEvent):
    """ Provides a base class for events that should be sent by email.

    If for example you want to queue a notification to be sent by mail when a
    user sends an inquiry, you would extend this class and hook it up in
    your app.

    E.g., you can declare the event like this:

        # somewhere in your app, e.g. in chatter.py
        class UserSentInquiryEvent(ChatterboxMailEvent):
            originator = 'my_app'
            event = 'User sends inquiry'
            mail_to = 'me@example.com'
            template_subject = 'my_app/chatterbox/email_subject.html'
            template_body = 'my_app/chatterbox/email_body.html'


    Now you can use this event when the inquiry is sent, e.g.:

        def inquiry_saved(sender, **kwargs):
            inst = kwargs.get('instance')

            if hasattr(inst, 'current_user'):
                current_user = inst.current_user
            else:
                raise Exception("current_user is not available on instance.")

            ch = UserSentInquiryEvent()
            ch.mail_from = current_user.email
            ch.notify_chatterbox(
                actor=current_user,
                target=kwargs.get('instance')
            )

        post_save.connect(inquiry_saved, sender=YourInquiryModel)

    .. note::

        If used with a ``post_save`` signal and you need access to the user
        that saved the instance you need to make sure to attach the user to
        the ``instance`` manually, e.g. in the save-methods of your form or
        admin form.

    """
    channel = 'email'
    mail_from = None
    mail_to = None
    template_subject = None
    template_body = None

    # TODO(sthzg) validate given attributes on __init__ time.

    def __init__(self, *args, **kwargs):
        self.add_template('subject', self.template_subject)
        self.add_template('body', self.template_body)

        super(ChatterboxMailEvent, self).__init__(*args, **kwargs)

    def notify_chatterbox(self, actor=None, target=None, **kwargs):
        # TODO(sthzg) validate given attributes on notify_chatterbox time.
        self.add_channel_data('from', self.mail_from)
        self.add_channel_data('to', self.mail_to)

        super(ChatterboxMailEvent, self).notify_chatterbox(
            actor, target, **kwargs)
