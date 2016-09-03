from django.shortcuts import render_to_response, redirect
from django.template.context_processors import csrf
import csv

N = 3

rc = [[]]
rp = [[]]

for i in range(1, N+1):
    f = open('csv/rc' + str(i) + '.csv', 'r')
    csvReader = csv.reader(f)

    lst = []
    rc.append(lst)

    for row in csvReader:
        lst.append(row)

    f.close()


for i in range(1, N+1):
    f = open('csv/rp' + str(i) + '.csv', 'r')
    csvReader = csv.reader(f)

    lst = []
    rp.append(lst)

    for row in csvReader:
        lst.append(row)

    f.close()

print (rc)

def index(request):
    return render_to_response('index.html')


def start(request):
    #
    c = {}
    c.update(csrf(request))

    if request.method == 'GET':
        return render_to_response('start.html', c)

    step = int(request.POST['step'])

    if step == 0:
        #
        request.session.clear()

        #
        request.session['name'] = request.POST['name']
        request.session['party'] = request.POST['party']

        #
        c['level'] = 1

        return render_to_response('question.html', c)
    else:
        level = int(request.POST['level'])
        amount = int(request.POST['amount'] if request.POST['amount'] else '-1')

        if amount > 0:
            c['candidate'] = rc[level]
            c['party'] = rp[level]
            return render_to_response('ranking.html', c)
        else:
            c['level'] = step + 1

            return render_to_response('question.html', c)

    return render_to_response('start.html', c)
