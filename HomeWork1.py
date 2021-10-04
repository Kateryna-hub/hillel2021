from django.http import Http404
from django.core.management import execute_from_command_line
from django.http import HttpResponse
from django.urls import path 
from django.conf import settings
from django.shortcuts import render
import this
from stdlib_list import stdlib_list
from random import choice
#URL
# https://docs.python.org 

settings.configure(
    DEBUG = True,
    ROOT_URLCONF=__name__,
    SECRET_KEY='Aghjk',
)

TEMPLATE = """
<!DOCTYPE html>
<html>
    <body>
    <h1>{message}</h1>
    {content}
    </body>
</html>
"""
text = ''.join(this.d.get(c, c) for c in this.s)
title, _, *quotes = text.splitlines()


def handler_index(request):
    link = '<a href="doc/">{}</a>'.format('Python standard library')
    return HttpResponse(TEMPLATE.format(message=link,
                                        content=''))


def handler(request):
    list_modules = [name for name in stdlib_list()
                if not name.startswith('_') and '.' not in name ]
    links = ['<a href="{}">{}</a><br>'.format(name, name) for name in list_modules]
    return HttpResponse(TEMPLATE.format(message='Python standard library',
                                        content=''.join(links)))


def mod_handler(request, mod_name):
    try:
        mod = __import__(mod_name)
        func = [name for name in dir(mod)
                    if not name.startswith('_')]
        links = ['<a href="{}/{}">{}</a><br>'.format(mod_name, name, name) for name in func]
    except:
        raise Http404("Module does not exist")
    return HttpResponse(TEMPLATE.format(message=mod_name,
                                        content=''.join(links)))


def obj_handler(request,mod_name, obj_name):
    try:
        mod = __import__(mod_name)
        func = getattr(mod, obj_name)
        content = func.__doc__
    except:
        raise Http404("Module or object does not exist")    
    return HttpResponse(content, content_type='text/plan')

urlpatterns = [
    path('', handler_index),
    path('doc/', handler),
    path('doc/<mod_name>', mod_handler),
    path('doc/<mod_name>/<obj_name>', obj_handler),
]


if __name__ == '__main__':
    execute_from_command_line()