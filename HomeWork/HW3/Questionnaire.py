import csv
import json
from flask import Flask
from flask import render_template, request

app = Flask(__name__)

@app.route('/')
def index():

    right = 0
    user_answers = []
    right_answer = ['пить', 'пью', 'алкоголь', 'водка', 'книга', 'книжка'
                    'печатать', 'клавиатура', 'компьютер', 'программировать', 'любить', 'любовь', 'люблю']
    if request.args:
        name = request.args['name']
        age = request.args['age']
        sex = request.args['sex']
        education = request.args['education']
        alcohol = request.args['alcohol']
        drink = request.args['drink']
        computer = request.args['computer']
        book = request.args['book']
        love = request.args['love']
        user_answers.append(alcohol.lower())
        user_answers.append(drink.lower())
        user_answers.append(computer.lower())
        user_answers.append(book.lower())
        user_answers.append(love.lower())
        for a in user_answers:
            for r in right_answer:
                if a == r:
                    right = right + 1

        with open('metadata.csv', mode='a', encoding="utf-8") as csv_file:
            fieldnames = ['Имя', 'Возраст', 'Пол', 'Образование', 'Алкоголь', 'Пить', 'Компьютер', 'Книга', 'Любить']

            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter='\t')

            # writer.writeheader()
            writer.writerow({'Имя': name,
                             'Возраст': age,
                             'Пол': sex,
                             'Образование': education,
                             'Алкоголь': alcohol,
                             'Пить': drink,
                             'Компьютер': computer,
                             'Книга': book,
                             'Любить': love })


        return render_template('stats.html', name=name, right=right)
    return render_template('metadata.html')

@app.route('/json')
def get_json():
    dict_csv = {}
    fieldnames = ['name', 'age', 'sex', 'education', 'alcohol', 'drink', 'computer', 'book', 'love']
    with open('metadata.csv', 'r', encoding="utf-8") as f:
        reader = csv.DictReader(f, fieldnames=fieldnames, delimiter='\t')
        for row in reader:
            name = row['name']
            age = row['age']
            sex = row['sex']
            education = row['education']
            alcohol = row['alcohol']
            drink = row['drink']
            computer = row['computer']
            book = row['book']
            love = row['love']

        dict_csv['name'] = name
        dict_csv['age'] = age
        dict_csv['sex'] = sex
        dict_csv['education'] = education
        dict_csv['alcohol'] = alcohol
        dict_csv['drink'] = drink
        dict_csv['computer'] = computer
        dict_csv['book'] = book
        dict_csv['love'] = love
        json_data = json.dumps(dict_csv, ensure_ascii=False)
        return render_template('json.html', json=json_data)

@app.route('/search')
def searching():
    return render_template('search.html')

@app.route('/result')
def show_result():
    if request.args:
        sex = request.args['sex_search']
        word = request.args['word_search']
        fieldnames = ['name', 'age', 'sex', 'education',  'alcohol', 'drink', 'computer', 'book', 'love']
        with open('metadata.csv', 'r', encoding="utf-8") as f:
            reader = csv.DictReader(f, fieldnames=fieldnames, delimiter='\t')
            for row in reader:
                if row['sex'] == sex:
                    if word == 'алкоголь':
                        sign = 'alcohol'
                        user_answer = row['alcohol']
                    elif word == 'пить':
                        sign = 'drink'
                        user_answer = row['drink']
                    elif word == 'компьютер':
                        sign = 'computer'
                        user_answer = row['computer']
                    elif word == 'книга':
                        sign = 'book'
                        user_answer = row['book']
                    elif word == 'любить':
                        sign = 'love'
                        user_answer = row['love']
                    else:
                        sign = 'None'
                        user_answer = 'None'
                else:
                    user_answer = 'None'
                    sign = 'None'
                    sorry = 'Изините, нет данных по выбранному параметру, попоробуйте сменить пол..'


            return render_template('result.html', user_answer = user_answer, sign = sign, word = word, sorry = sorry)





if __name__ == '__main__':
    app.run(debug=True)




