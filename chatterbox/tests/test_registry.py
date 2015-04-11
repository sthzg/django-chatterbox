# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import chatterbox
from django.test.testcases import SimpleTestCase
from .helpers import MailEventDummyClass


class RegistryTests(SimpleTestCase):
    def setUp(self):
        chatterbox.clear_registry()

    def tearDown(self):
        chatterbox.clear_registry()

    def test_registering_multiple_elements(self):
        """ Registering an event class in the registry works as expected.
        """
        chatterbox.register(MailEventDummyClass)
        registry = chatterbox.get_registry()

        key = 'chatterbox_tests: Stephan runs unit tests'

        self.assertEqual(len(registry), 1)
        self.assertTrue(key in registry)
        self.assertTrue(MailEventDummyClass in registry.get(key).__mro__)

