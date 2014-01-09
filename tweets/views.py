from django.shortcuts import render_to_response
from django.template import RequestContext


def MainHomePage(request):
    context = {'tweets': [1, 2, 3]}
    return render_to_response('index.html', context,
                              context_instance=RequestContext(request))
