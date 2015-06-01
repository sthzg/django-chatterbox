# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.db import models
from django.utils.datetime_safe import datetime
from django.utils.translation import ugettext_lazy as _


class MessageManager(models.Manager):
    def due(self, channel=None):
        """ Returns messages that are due for action.

        :param channel: channel(s) to filter for
        :type channel: str or list
        :return: queryset of matches
        :rtype: QuerySet
        :raises: ValueError
        """
        q_filter = {
            'should_cancel': False,
            'is_done': False,
            'scheduled_for__lte': datetime.now()
        }

        if channel:
            if type(channel) is not str and type(channel) is not list:
                raise ValueError(
                    'The argument channel must be of type str or list.'
                )

            if type(channel) is str:
                channel = [channel]

            q_filter.update({'channel__in': channel})

        return self.filter(**q_filter).order_by('priority', 'scheduled_for')


class Message(models.Model):
    class Meta:
        verbose_name = _('message')
        verbose_name_plural = _('messages')

    objects = MessageManager()

    #: A string that identifies the originator of the message, usually the
    #: Django app name.
    originator = models.CharField(
        _('originator'),
        max_length=100,
        default=None
    )

    #: An arbitrary string that uniquely identifies the message. It can be 
    #: set by whoever calls `notify_chatterbox()` to allow business logic 
    #: that determines if a certain message has already been generated. 
    #: `natural_id` may be NULL but otherwise has to be **unique**.
    natural_id = models.CharField(
        _('natural id'),
        max_length=32,
        blank=True,
        null=True,
        default=None,
        unique=True
    )

    #: A string that identifies the event type, e.g. 'User liked Story'.
    event = models.CharField(
        _('event'),
        max_length=100,
        default=None
    )

    #: A JSON-serialized dictionary containing arbitrary information that
    #: you want to save with a record. Use this field to save information
    #: from your actor, object or target. E.g., if any of these objects are
    #: model instances you could save their primary key and model class. This
    #: way you could fetch the instance if necessary.
    #:
    #:  .. note:
    #:
    #:     The ``Message`` model does not contain generic foreign keys to
    #:     actor, object or target, since there are many use cases where
    #:     these components could be different entities but model instances.
    #:
    metadata = models.TextField(
        _('meta data'),
        default=None,
        null=True
    )

    #: A JSON-serialized dictionary containing all necessary content to
    #: generate the message. If a message is intended to be mailed, this
    #: might have a ``subject`` and a ``body`` field.
    content = models.TextField(
        _('content'),
        default=None
    )

    #: A boolean that indicates whether the message has been processed, e.g.
    #: an email has been sent, a tweet has been tweeted, etc.
    is_done = models.BooleanField(
        _('is done'),
        default=False
    )

    #: A string that identifies the channel that this message should be
    #: processed with, e.g. email or twitter.
    channel = models.CharField(
        _('channel'),
        max_length=30,
        default=None
    )

    #: A JSON-serialized dict containing all fields that are necessary to
    #: provide to the channel, e.g. a from and to for constructing an email.
    channel_data = models.TextField(
        _('channel data'),
        default=None
    )

    #: Identifier for the natural language that the generated message is in.
    #: Will be the language code in 99% of the time. For messages that contain
    #: mixed languages you can also choose an arbitrary id, e.g. 'mixed`.
    language = models.CharField(
        _('language'),
        max_length=7,  # e.g. zh-hans
        default=''
    )

    #: The priority to process this message. In the context of queuing
    #: multiple messages at once this makes it possible to prioritize
    #: more important messages, e.g. a particular notification over the
    #: delivery of a newsletter.
    priority = models.PositiveIntegerField(
        _('priority'),
        max_length=2,
        default=10
    )

    #: A datetime that indicates the earliest allowed time to process the
    #: message. Note that due to queueing there is no guarantee that a
    #: message will be processed exactly at that time.
    scheduled_for = models.DateTimeField(
        _('scheduled for'),
        default=None
    )

    #: Datetime of the actual processing of the message.
    done_at = models.DateTimeField(
        _('done at'),
        default=None,
        null=True
    )

    #: A boolean indicating whether processing this message is cancelled.
    should_cancel = models.BooleanField(
        _('should cancel'),
        default=False,
    )

    #: If ``should_cancel`` is True, the reason why it has been cancelled.
    cancel_reason = models.CharField(
        _('reason to cancel'),
        max_length=500,
        default=None,
        null=True,
    )

    #: Flag indicating whether the last attempt to process this message
    #: yielded an error.
    has_error = models.NullBooleanField(
        _('has error'),
        default=None
    )

    #: A counter that increases each time that processing this message yielded
    #: an error. This can be used to configure the amount of retries before
    #: a message should be treated as ``has_failed``.
    error_count = models.PositiveIntegerField(
        _('error count'),
        default=None,
        null=True
    )

    #: A JSON-serialized list of error messages. The length of the list should
    #: match ``error_count``, so that the errors can be mapped correctly.
    error_data = models.TextField(
        _('error data'),
        default=None,
        null=True
    )

    #: A flag indicating that processing this message has been marked as
    #: constantly failing. E.g. if an email couldn't be delivered in three
    #: attempts the message might be marked to ``has_failed``.
    has_failed = models.BooleanField(
        _('has failed'),
        default=False
    )

    created = models.DateTimeField(
        _('created'),
        auto_now_add=True
    )

    modified = models.DateTimeField(
        _('last modified'),
        auto_now=True
    )

    def __unicode__(self):
        return '{} originates {}'.format(
            self.originator,
            self.event
        )
