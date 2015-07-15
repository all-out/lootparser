from main.models import Paste


def pastebar(request):
    '''Returns a dictionary containing the 8 most recently created pastes.'''
    pastes = Paste.objects.all().order_by('-created')#[:8]
    context = {}
    context['pastebar'] = pastes
    return context
