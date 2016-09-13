# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, redirect
from django.template.context_processors import csrf
import csv

N = 7
P = 5

title = ['', '먹거리', '로고송', '언론/광고', '문자', '유세차량', '선거운동원', '홍보물']

f = open('csv/data.csv', 'r')
csvReader = csv.reader(f)

rcdata = {}
rpdata = {}

for i in range(1, N+1):
    rcdata[str(i)] = []
    for j in range(1, P+1):
        rpdata[str(i)+str(j)] = []

for row in csvReader:
    # 전체 랭킹 먼저
    rcdata[row[0]].append([row[1], row[2], row[3]])
    # 정당 랭킹
    rpdata[row[0]+row[1]].append([row[1], row[2], row[3]])

for i in range(1, N+1):
    rcdata[str(i)] = sorted(rcdata[str(i)], key=lambda r: int(r[2]), reverse=True)
    for j in range(1, P+1):
        rpdata[str(i)+str(j)] = sorted(rpdata[str(i)+str(j)], key=lambda r: int(r[2]), reverse=True)

f.close()

rc = [[]]

rchead = [[]]
rcfoot = [[]]
rcaver = [[]]

rp = {}
rphead = {}
rpfoot = {}
rpaver = {}

question = [[]]

for i in range(1, N + 1):
    lst = []
    rc.append(lst)

    head = []
    rchead.append(head)

    foot = []
    rcfoot.append(foot)

    j = 0
    sum = 0
    rank = 1
    for row in rcdata[str(i)]:
        # 순위 당 이름 금액
        row = [str(rank)] + row
        if j < 3:
            head.append(row)

        lst.append(row)
        sum += int(row[3])
        j += 1
        rank += 1

    for k in range(len(lst) - 3, len(lst)):
        foot.append(lst[k])

    rcaver.append(['', '-1', '평균', str(sum / len(lst))])

for i in range(1, N + 1):
    for j in range(1, P + 1):
        key = str(i) + str(j)

        lst = []
        rp[key] = lst

        head = []
        rphead[key] = head

        foot = []
        rpfoot[key] = foot

        k = 0
        sum = 0
        rank = 1
        for row in rpdata[key]:
            # 순위 당 이름 금액
            row = [str(rank)] + row
            if k < 3:
                head.append(row)

            lst.append(row)
            sum += int(row[3])
            k += 1
            rank += 1

        for k in range(len(lst) - 3, len(lst)):
            foot.append(lst[k])

        rpaver[key] = ['', '-1', '평균', str(sum / len(lst))]

f = open('csv/question.csv')
csvReader = csv.reader(f, quoting=csv.QUOTE_NONE)

for row in csvReader:
    question.append(row)

print question

def index(request):
    return render_to_response('index.html')


def add_rank(row):
    return [str(int(row[0]) + 1), row[1], row[2], row[3]]


def get_amount(row):
    return int(row[3])


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
            lst = list(rchead[level])
            for i in range(0, len(rclst)):
                if i == 0 and amount > get_amount(rclst[i]):
                    rank = i + 1
                    lst += [[str(rank), party, name, str(amount), True], add_rank(rclst[0])]
                    break
                elif i == len(rclst) - 1:
                    rank = i + 1
                    lst += [rclst[i], [str(rank), party, name, str(amount), True]]
                    break

                if get_amount(rclst[i]) >= amount > get_amount(rclst[i+1]):
                    rank = i + 2
                    lst += [rclst[i], [str(rank), party, name, str(amount), True], add_rank(rclst[i+1])]
                    break
            lst += rcfoot[level]

            aver = rcaver[level]
            for i in range(0, len(lst)):
                if get_amount(lst[i]) >= get_amount(aver) > get_amount(lst[i+1]):
                    lst.insert(i+1, aver)
                    break

            c['candidate'] = lst

            request.session['result' + str(level)] = ['Q' + str(level) + '.' + title[level], str(rank), str(amount)]

            key = str(level) + party
            rplst = rp[key]
            lst = list(rphead[key])
            for i in range(0, len(rplst)):
                if i == 0 and amount > get_amount(rplst[i]):
                    lst += [[str(i+1), party, name, str(amount), True], add_rank(rplst[0])]
                    break
                elif i == len(rplst) - 1:
                    lst += [rplst[0], [str(i+1), party, name, str(amount), True]]
                    break

                if get_amount(rplst[i]) >= amount > get_amount(rplst[i+1]):
                    lst += [rplst[i], [str(i+2), party, name, str(amount), True], add_rank(rplst[i+1])]
                    break
            lst += rpfoot[key]

            aver = rpaver[key]
            for i in range(0, len(lst)):
                if get_amount(lst[i]) >= get_amount(aver) > get_amount(lst[i+1]):
                    lst.insert(i+1, aver)
                    break

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
