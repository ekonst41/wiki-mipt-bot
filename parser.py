from bs4 import BeautifulSoup
import requests
import re

teachers_global = []
urls = ['https://goo.su/m2B8Re', 'https://goo.su/Cm80o', 'https://goo.su/DZJmwg', 'https://goo.su/eDsJJ', 'https://goo.su/t09sSa', 'https://goo.su/Y7NsLvJ', 'https://goo.su/Gx3rFy', 'https://goo.su/4e8XI5']
for url in urls:
    page = requests.get(url)
    soup = str(BeautifulSoup(page.text, "html.parser"))
    teachers = re.findall(r'(title=")([А-ЯЁа-яё]+ [А-ЯЁа-яё]+ [А-ЯЁа-яё]+)(")', soup)
    teachers = [i[1] for i in teachers]
    teachers = [teacher.split() for teacher in teachers]
    teachers = ["{}_{}_{}".format(t[0], t[1], t[2]) for t in teachers]
    for teacher in teachers:
        teachers_global.append(teacher.replace('ё', 'е'))

t = open('teachers.txt', 'w', encoding="utf-8")
for teacher in teachers_global:
    t.write(str(teacher) + '\n')
t.close()
