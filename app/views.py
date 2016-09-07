# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, redirect
from django.template.context_processors import csrf
import csv

N = 3

title = ['', '문자', '로고송', '다과']

rc = [[]]
rp = [[]]

rchead = [[]]
rcfoot = [[]]
rcaver = [[]]

rphead = [[]]
rpfoot = [[]]
rpaver = [[]]

question = [[]]

for i in range(1, N + 1):
    f = open('csv/rc' + str(i) + '.csv', 'r')
    csvReader = csv.reader(f)

    lst = []
    rc.append(lst)

    head = []
    rchead.append(head)

    foot = []
    rcfoot.append(foot)

    j = 0
    sum = 0
    for row in csvReader:
        if j < 3:
            head.append(row)

        lst.append(row)
        sum += int(row[2])
        j += 1

    for k in range(len(lst) - 3, len(lst)):
        foot.append(lst[k])

    rcaver.append(['', '평균', str(sum / len(lst)), '-1'])

    f.close()

for i in range(1, N + 1):
    f = open('csv/rp' + str(i) + '.csv', 'r')
    csvReader = csv.reader(f)

    lst = []
    rp.append(lst)

    head = []
    rphead.append(head)

    foot = []
    rpfoot.append(foot)

    j = 0
    sum = 0
    for row in csvReader:
        if j < 3:
            head.append(row)

        lst.append(row)
        sum += int(row[2])
        j += 1

    for k in range(len(lst) - 3, len(lst)):
        foot.append(lst[k])

    rpaver.append(['', '평균', str(sum / len(lst)), '-1'])

    f.close()

f = open('csv/question.csv')
csvReader = csv.reader(f)

for row in csvReader:
    question.append(row)

print (question)


def index(request):
    return render_to_response('index.html')


def add_rank(row):
    return [str('나+1'), row[1], row[2], row[3]]


def del_rank(row):
    return [str('나-1'), row[1], row[2], row[3]]


def get_amount(row):
    return int(row[2])


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
        c['question'] = question[1]

        return render_to_response('question.html', c)
    else:
        level = int(request.POST['level'])
        amount = int(request.POST.get('amount', -1))
        name = request.session['name']
        party = str(request.session['party'])

        if amount > 0:
            c['level'] = step

            rank = 0
            rclst = rc[level]
            lst = rchead[level] + [rcaver[level]]
            for i in range(0, len(rclst)):
                if i == 0 and amount > get_amount(rclst[i]):
                    rank = i+1
                    lst += [['나', name, str(amount), party, True], add_rank(rclst[0])]
                    break
                elif i == len(rclst) - 1:
                    rank = i+1
                    lst += [del_rank(rclst[i]), ['나', name, str(amount), party, True]]
                    break

                if get_amount(rclst[i]) >= amount > get_amount(rclst[i+1]):
                    rank = i+2
                    lst += [del_rank(rclst[i]), ['나', name, str(amount), party, True], add_rank(rclst[i+1])]
                    break
            lst += rcfoot[level]
            c['candidate'] = lst

            request.session['result' + str(level)] = [title[level], str(rank), str(amount)]

            rplst = rp[level]
            lst = rphead[level] + [rpaver[level]]
            for i in range(0, len(rplst)):
                if i == 0 and amount > get_amount(rplst[i]):
                    lst += [['나', name, str(amount), party, True], add_rank(rplst[0])]
                    break
                elif i == len(rplst) - 1:
                    lst += [del_rank(rplst[0]), ['나', name, str(amount)], party, True]
                    break

                if get_amount(rplst[i]) >= amount > get_amount(rplst[i+1]):
                    lst += [del_rank(rplst[i]), ['나', name, str(amount), party, True], add_rank(rplst[i+1])]
                    break
            lst += rpfoot[level]
            c['party'] = lst
            return render_to_response('ranking.html', c)
        else:
            if step == N:
                lst = []
                for i in range(1, N + 1):
                    lst.append(request.session['result' + str(i)])

                c['result'] = lst

                return render_to_response('result.html', c)
            else:
                c['level'] = step + 1
                c['question'] = question[step + 1]

                return render_to_response('question.html', c)

    return render_to_response('start.html', c)
