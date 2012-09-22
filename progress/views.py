from django.shortcuts import render_to_response
from django.template import RequestContext

from progress.models import Goal, Update

def index(request):
	goals = Goal.objects.all()

	return render_to_response('index.html',
		{'goals': goals},
		context_instance=RequestContext(request))
