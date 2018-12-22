import sqlite3
import re
from flask import Flask
from flask import render_template, request

def create_DB(filename, filename_2):
    #файл со статьей
    with open(filename, encoding='utf-8') as f:
        raw_article = f.read()
        regTitle = re.compile('@ti\s(.*?)\n', flags=re.DOTALL) 
        title = regTitle.findall(raw_article) #Название статьи
        regText = re.compile('@url.*?\n(.*)', flags=re.DOTALL)
        text = regText.findall(raw_article) #текст статьи
        regLink = re.compile('@url\s(.*?)\n', flags=re.DOTALL)
        link = regLink.findall(raw_article) #ссылка на статью
  
  #файл с лематизированной статьей
   with open(filename_2, encoding='utf-8') as l: 
        lem_text = l.read()

        # подключаемся к базе данных
        conn = sqlite3.connect('Articles_Data.db')

        # создаем объект "курсор", которому будем передавать запросы
        c = conn.cursor()

        # создаем таблицу
        c.execute("CREATE TABLE IF NOT EXISTS article(title, link, text, lem_text)")
        # встваляем данные из статей
        c.execute('INSERT INTO article VALUES  (?, ?, ?, ?)', (title[0], link[0], text[0], lem_text))
        #для проверки БД
        for i in c.execute("SELECT * FROM article"):
            print(i)
        # сохраняем изменения
        conn.commit()

        # отключаемся от БД
        conn.close()
        return (conn)

app = Flask(__name__)

#страница поиска
@app.route('/')
def searching():
    return render_template('search.html')

#страница с выдачей результатов
@app.route('/result')
def show_result():
    if request.args:
        # поисковый запрос = токен
        word = (request.args['word_search']) 
        print(word)
        # подключаемся к базе данных
        conn = sqlite3.connect('Articles_Data.db')
        # создаем объект "курсор", которому будем передавать запросы
        c = conn.cursor()
        # оформляем запрос для нужной формы ДБ
        word_DB = ('% ' + word + ' %',)
        texts = []
        # ищем  в статье запрос
        for row in c.execute('SELECT * FROM article WHERE text LIKE ? ', word_DB): 
            link = row[1] 
            context = row[2]
            # ищет предложение, в котором содержиться запрос
            context = re.findall('\.\s(.*?' + word + '.*?)\.', context)
            
            if len(context) > 1:
                result = link + '\n' + '\n '.join(context)
            else:
                result = link + '\n' + context[0]
            texts.append(result)
        return render_template('result.html', word = word, result = texts)

def main():


    comDB1 = create_DB('article_1.txt', 'article_1_lem.txt')
    comDB2 = create_DB('article_2.txt', 'article_2_lem.txt')
    comDB3 = create_DB('article_3.txt', 'article_3_lem.txt')
    comDB4 = create_DB('article_4.txt', 'article_4_lem.txt')
    comDB5 = create_DB('article_5.txt', 'article_5_lem.txt')

    app.run(debug=True)

if __name__ == '__main__':
    main()

