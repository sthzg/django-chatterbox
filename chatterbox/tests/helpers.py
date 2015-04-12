# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from chatterbox.events import ChatterboxMailEvent


class MailEventDummyClass(ChatterboxMailEvent):
    originator = 'chatterbox_tests'
    event = 'Stephan runs unit tests'
    mail_from = 'foo@example.com'
    mail_to = 'bar@example.com'
    template_subject = 'chatterbox_tests/email_subject.html'
    template_body = 'chatterbox_tests/email_body.html'
    token_fields = (
        ''
    )


class TestClass(object):
    foo = 'ham'
    bar = {
        'eggs': True,
        'juice': False
    }


def get_test_dict():
    return {
        'foo': 'ham',
        'bar': {
            'eggs': True,
            'juice': False
        }
    }
