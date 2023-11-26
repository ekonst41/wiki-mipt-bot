from bs4 import BeautifulSoup
import requests
import re
from rdflib import Graph

translator = {'communication': 'Общение', 'expert': 'Знания', 'freebie': 'Халявность', 'instructor': 'Умение преподавать', 'total': 'Общая оценка'}

def response_maker(teach, rate):
    t = teach.split(sep='_')
    t = ' '.join(t)
    response = t + '\n'
    for key in rate.keys():
        response += translator[key] + ': ' + str(rate[key]) + '\n'
    return response


def get_ratings(teacher):
    teacher_url = 'https://wiki.mipt.tech/index.php/' + teacher
    page = requests.get(teacher_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    content_blocks = soup.find(rel="alternate")
    new_url = "https://wiki.mipt.tech" + content_blocks.get('href')
    page = requests.get(new_url)
    g = Graph()
    g.parse(new_url)
    text = str(g.serialize(format='ttl'))
    ratings = re.findall(r'([a-z]*)"\^\^xsd:string ;\n    property:Average_rating (\d.\d*)', text)
    rates = dict()
    for rating in ratings[:5]:
        if rating[1][1] != 'e':
            rates[rating[0]] = round(float(rating[1]), 2)
        else:
            rates[rating[0]] = float(rating[1][0])
    if len(rates) != 0:
        response = response_maker(teacher, rates)
    else:
        t = teacher.split(sep='_')
        t = ' '.join(t)
        response = t + '\n'
        response += 'По этому преподавателю пока нет оценок.'
    return response


def search(req):
    search = []
    with open('teachers.txt', 'r', encoding='utf-8') as f:
        f = f.readlines()
        for teacher in f:
            match_total = True
            for requests in req:
                requests = requests.lower()
                match = re.search(requests + '_', teacher.lower()) or re.search('_' + requests + '\n', teacher.lower())
                match_total = match and match_total
            if match_total:
                search.append(teacher[:-1])
    if len(search) == 1:
        response = get_ratings(search[0])
    elif len(search) > 1:
        response = 'По вашему запросу мы нашли таких преподавателей:\n'
        for item in search:
            i = item.split(sep='_')
            response = response + ' '.join(i) + '\n'
        response += 'Уточните ваш запрос.'
    else:
        response = 'Мы не нашли такого преподавателя :(\nПроверьте, правильно ли вы всё написали'
    return response

