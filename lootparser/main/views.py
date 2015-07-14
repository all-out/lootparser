from django.shortcuts import render
from django.views.generic import View
from main.models import Paste


def paste(request):
    context = {}
    context['first'] = 'Hello World!'
    return render(request, 'paste.html', context)


class Paste(View):

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'paste.html', context)

    def post(self, request, *args, **kwargs):
        context = {}
        raw_paste = request.POST.get('raw_paste', None)
        # print raw_paste
        new_paste = Paste(contents=raw_paste)
        print '\n\n\n'
        print new_paste.contents
        print str(new_paste.creation_date)
        print '\n\n\n'
        new_paste.save()
        return render(request, 'paste.html', context)
