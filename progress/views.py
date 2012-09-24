from django.shortcuts import render_to_response
from django.template import RequestContext

from progress.models import Goal, DayLog

def index(request):
    goals = Goal.objects.all()
    daylogs = sorted(DayLog.objects.all()[:7], key=lambda k: k.date, reverse=True)

    return render_to_response('index.html',
            {'goals': goals, 'daylogs': daylogs},
            context_instance=RequestContext(request))
