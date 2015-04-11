# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.test.testcases import SimpleTestCase
from chatterbox.events import BaseChatterboxEvent
from .helpers import MailEventDummyClass


class BaseChatterboxTests(SimpleTestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_add_template(self):
        """ add_template() stores passed values as expected.
        """
        be = BaseChatterboxEvent()
        be.add_template('foo', 'chatterbox_tests/empty_foo.html')
        be.add_template('bam', 'chatterbox_tests/empty_bar.html')

        self.assertEqual(len(be.templates), 2)
        self.assertTrue('foo' in be.templates)
        self.assertTrue('bam' in be.templates)
        self.assertTrue(be.templates.get('foo') == 'chatterbox_tests/empty_foo.html')  # NOQA


class ChatterboxMailEventTests(SimpleTestCase):
    def setUp(self):
        self.template_subject = 'chatterbox_tests/email_subject.html'
        self.template_body = 'chatterbox_tests/email_body.html'

    def tearDown(self):
        pass

    def test_class_members(self):
        """ various behavioral basics work as expected. Might later be split
        into smaller and more fragmented test cases.
        """
        chatter = MailEventDummyClass()

        self.assertEqual(chatter.originator, 'chatterbox_tests')
        self.assertEqual(chatter.event, 'Stephan runs unit tests')
        self.assertEqual(chatter.mail_from, 'foo@example.com')
        self.assertEqual(chatter.mail_to, 'bar@example.com')
        self.assertEqual(chatter.template_subject, self.template_subject)
        self.assertEqual(chatter.template_body, self.template_body)
        self.assertTrue('subject' in chatter.templates)
        self.assertTrue('body' in chatter.templates)
