# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from chatterbox.handlers import EmailChannelMessageHandler
from chatterbox.models import Message


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            '--dry-run',
            dest='dryrun',
            action='store_true',
            default=True,
            help='If True only lists the messages to be processed'),
    )

    can_import_settings = True

    def handle(self, *args, **options):
        self.stdout.write(
            '{}\tChecking backend for messages to be '
            'processed:'.format(datetime.now())
        )

        due = Message.objects.due()

        for message in due:
            self.stdout.write('{}, {}'.format(
                message.pk,
                message
            ))

            # Process the message
            if message.channel == 'email':
                handler = EmailChannelMessageHandler(message)
                handler.process()

        self.stdout.write('{}\tAll done, sir!'.format(datetime.now()))
        exit(0)
