from django.shortcuts import render_to_response, redirect
from django.template.context_processors import csrf


def index(request):
    return render_to_response('index.html')


def start(request):
    #
    c = {}
    c.update(csrf(request))

    if request.method == 'GET':
        return render_to_response('start.html', c)

    #
    request.session.clear()

    #
    request.session['name'] = request.POST['name']
    request.session['party'] = request.POST['party']

    #
    c['level'] = 1
    c['name'] = request.session['name']
    c['party'] = request.session['party']

    return render_to_response('question.html', c)
