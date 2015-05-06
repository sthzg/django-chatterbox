# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json
from django.http.response import Http404
from django.shortcuts import render
from django.template import loader
from django.template.context import Context
from django.views.generic.base import View


class Preview(View):
    def post(self, request):
        data = request.POST

        if not data:
            raise Http404

        lang = data.get('lang')
        ctx = json.loads(data.get('preview_context'))
        templates = json.loads(data.get('templates'))

        output = list()
        for template in templates:
            t_path = ''
            t = loader.get_template(t_path)
            c = ctx
            output.append(t.render(c))

        c = Context({
            'output': output
        })

        return render(request, 'chatterbox/preview.html', c)
