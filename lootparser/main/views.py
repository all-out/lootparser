from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.generic import View
from main.models import Paste


class PasteView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'paste.html', context)

    def post(self, request, *args, **kwargs):
        context = {}
        raw_paste = request.POST.get('raw_paste', None)
        new_paste = Paste(raw_paste=raw_paste)
        new_paste.save()
        return render_to_response(
                'paste.html', context,
                context_instance=RequestContext(request))


class DisplayView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        paste_id = self.kwargs['paste_id']
        context['paste'] = Paste.objects.get(id=paste_id)
        return render_to_response(
                'display.html', context,
                context_instance=RequestContext(request))
