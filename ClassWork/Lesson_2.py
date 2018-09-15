s = '{} Sacha'
h = s.format('Helo')
h  # 'Helo Sacha'
s = '{} Sacha. {}?'
h = s.format('Helo', 'How are you')
h # 'Helo Sacha. How are you?'
x = 'one = {1}; two = {0}'
x.format('dos', 'uno') #'one = uno; two = dos'

l = [2, 3, 4]
l.pop(0) # [3,4] -удаляет элемент по индексу
x.sort #сортирует по возрастанию
x.reverso #переворачивает

'''Картеж'''
z = (4, 6, 8)

'''Practice'''
#1
vals = [5, 8, 88, 9, 4]
def mean(vals):
    if len(vals) > 0:
        average = float(sum(vals))/len(vals)
        print(average)
    else:
        print('n/a')
mean(vals)

#5.1
cons = 'ptk'
vowels = 'ao'
for v in vowels:
    for c in cons:
        print(c+v)
#5.2
verbs = ('run swim sleep draw')
nouns = ('sun backer snake')
for s in nouns.split():
    for v in verbs.split():
        for o in nouns.split():
            print(s + ' ' + v + ' ' + o)
