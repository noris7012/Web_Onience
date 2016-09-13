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
csvReader = csv.reader(f, quotechar='|')

for row in csvReader:
    question.append(row)

print question


def index(request):
    return render_to_response('index.html')


def add_rank(row):
    return [str(int(row[0]) + 1), row[1], row[2], row[3]]

def get_rank(row):
    return int(row[0])

def get_amount(row):
    return int(row[3])


def make_list(lst, aver, me, rank):
    ret = []
    # 랭크 중복 제거
    for row in lst:
        b = False
        for r in ret:
            if get_rank(r) == get_rank(row):
                b = True
                break
        if b:
            continue
        ret.append(row)

    # 나 추가
    for i in range(0, len(ret)):
        if i == 0 and rank <= get_rank(ret[i]):
            ret.insert(0, me)
            break
        if i == len(ret) - 1:
            ret.append(me)
            break
        if get_rank(ret[i]) < rank <= get_rank(ret[i+1]):
            ret.insert(i+1, me)
            break

    # 평균값 추가
    for i in range(0, len(ret)):
        if get_amount(ret[i]) >= get_amount(aver) > get_amount(ret[i+1]):
            ret.insert(i+1, aver)
            break

    # Rank Up
    for i in range(0, len(ret)):
        # Me Pass
        if len(ret[i]) > 4 and ret[i][4]:
            continue

        # 평균 Pass
        if int(ret[i][1]) == -1:
            continue

        if get_rank(ret[i]) >= rank:
            temp = list(ret[i])
            temp[0] = str(int(temp[0])+1)
            ret[i] = temp

    return ret



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
            lst = rchead[level]
            for i in range(0, len(rclst)):
                if i == 0 and amount > get_amount(rclst[i]):
                    rank = i + 1
                    me = [str(rank), party, name, str(amount), True]
                    lst.append(add_rank(rclst[0]))
                    break
                elif i == len(rclst) - 1 and get_amount(rplst[i]) >= amount:
                    rank = i + 2
                    me = [str(rank), party, name, str(amount), True]
                    lst.append(rclst[i])
                    break

                if get_amount(rclst[i]) >= amount > get_amount(rclst[i+1]):
                    rank = i + 2
                    me = [str(rank), party, name, str(amount), True]
                    lst += [rclst[i], rclst[i+1]]
                    break
            lst += rcfoot[level]
            lst = make_list(lst, rcaver[level], me, rank)

            c['candidate'] = lst

            request.session['result' + str(level)] = ['Q' + str(level) + '.' + title[level], str(rank), str(amount)]

            key = str(level) + party
            rplst = rp[key]
            lst = list(rphead[key])
            for i in range(0, len(rplst)):
                if i == 0 and amount > get_amount(rplst[i]):
                    rank = i+1
                    me = [str(rank), party, name, str(amount), True]
                    lst.append(rplst[0])
                    break
                elif i == len(rplst) - 1 and get_amount(rplst[i]) >= amount:
                    rank = i+2
                    me = [str(rank), party, name, str(amount), True]
                    lst.append(rplst[0])
                    break

                if get_amount(rplst[i]) >= amount > get_amount(rplst[i+1]):
                    rank = i+2
                    me = [str(rank), party, name, str(amount), True]
                    lst += [rplst[i], rplst[i+1]]
                    break
            lst += rpfoot[key]
            lst = make_list(lst, rpaver[key], me, rank)

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
