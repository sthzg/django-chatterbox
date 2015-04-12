# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.test.testcases import SimpleTestCase
from chatterbox.events import BaseChatterboxEvent
from .helpers import MailEventDummyClass, get_test_dict


class BaseChatterboxTests(SimpleTestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_add_template(self):
        """ ``add_template()`` stores passed values as expected.
        """
        be = BaseChatterboxEvent()
        be.add_template('foo', 'chatterbox_tests/empty_foo.html')
        be.add_template('bam', 'chatterbox_tests/empty_bar.html')

        self.assertEqual(len(be.templates), 2)
        self.assertTrue('foo' in be.templates)
        self.assertTrue('bam' in be.templates)
        self.assertTrue(be.templates.get('foo') == 'chatterbox_tests/empty_foo.html')  # NOQA

    def test_add_token(self):
        """ ``add_token`` yields the expected data structure.
        """
        be = BaseChatterboxEvent()
        be.add_token('bam', 'baz')
        be.add_token('actor.foo', 42)
        be.add_token('bar.baz.boo.jap', 'jahu')

        self.assertEqual(be._tokens['bam'], 'baz')
        self.assertEqual(be._tokens['actor']['foo'], 42)
        self.assertEqual(be._tokens['bar']['baz']['boo']['jap'], 'jahu')

    def test_add_nested_token_on_leaf_raises(self):
        # TODO(sthzg) implement
        # be = BaseChatterboxEvent()
        # be.add_token('bam', 'baz')
        # be.add_token('bam.foo', 42)
        pass

    def test_build_tokens_with_dict(self):
        """ ``build_tokens()`` resolves variables on current scope correctly.
        """
        be = BaseChatterboxEvent()
        be.actor = get_test_dict()
        be.token_fields = ('actor.foo', 'actor.bar.eggs', 'actor.bar',)
        be.build_tokens()

        tokens = be._tokens
        self.assertEqual(tokens['actor']['foo'], 'ham')
        self.assertTrue(isinstance(tokens['actor']['bar'], dict))
        self.assertEqual(tokens['actor']['bar']['juice'], False)
        self.assertEqual(tokens['actor']['bar']['eggs'], True)


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
