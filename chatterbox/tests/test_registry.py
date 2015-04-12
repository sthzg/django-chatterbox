# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from chatterbox import registry
from django.test.testcases import SimpleTestCase
from .helpers import MailEventDummyClass


class RegistryTests(SimpleTestCase):
    def setUp(self):
        registry.clear_registry()

    def tearDown(self):
        registry.clear_registry()

    def test_registering_multiple_elements(self):
        """ Registering an event class in the registry works as expected.
        """
        registry.register(MailEventDummyClass)
        reg = registry.get_registry()

        key = 'chatterbox_tests: Stephan runs unit tests'

        self.assertEqual(len(reg), 1)
        self.assertTrue(key in reg)
        self.assertTrue(MailEventDummyClass in reg.get(key).__mro__)

