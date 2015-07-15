from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.views.generic import View
from main.models import Paste
import evepaste


class PasteView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        return render_to_response(
            'paste.html', context,
            context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        context = {}
        raw_paste = request.POST.get('raw_paste', None)
        new_paste = Paste(raw_paste=raw_paste)
        new_paste.save()
        return redirect('display', paste_id=new_paste.id)


class DisplayView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        paste_id = self.kwargs['paste_id']
        context['paste'] = Paste.objects.get(id=paste_id)
        return render_to_response(
                'display.html', context,
                context_instance=RequestContext(request))
