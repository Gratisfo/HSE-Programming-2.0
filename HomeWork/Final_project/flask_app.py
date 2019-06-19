from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import re
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np
import requests
import tqdm
import os
from collections import Counter
from matplotlib import style

style.use('ggplot')



requests_get = requests.get
token = '182c5edb182c5edb182c5edb3d184747871182c182c5edb452d7c4237b114640b581059'
vk_api_base = 'https://api.vk.com/method'

app = Flask(__name__)


@app.route('/')
def index():
    all_raw_words = []
    if request.args:

        com_1 = request.args['community_1']
        posts_1 = get_data(com_1)
        raw_words_1 = get_text(posts_1)
        for word in raw_words_1:
            all_raw_words.append(word)
        top_words_1 = freq_words(raw_words_1)
        name_plot_1 = 'static\plot_1.png'
        plot_1 = create_plot(top_words_1,  name_plot_1)


        com_2 = request.args['community_2']
        posts_2 = get_data(com_2)
        raw_words_2 = get_text(posts_2)
        for word in raw_words_2:
            all_raw_words.append(word)
        top_words_2 = freq_words(raw_words_2)
        name_plot_2 = 'static\plot_2.png'
        plot_2 = create_plot(top_words_2, name_plot_2)


        com_3 = request.args['community_3']
        posts_3 = get_data(com_3)
        raw_words_3 = get_text(posts_3)
        for word in raw_words_3:
            all_raw_words.append(word)
        top_words_3 = freq_words(raw_words_3)
        name_plot_3 = 'static\plot_3.png'
        plot_3 = create_plot(top_words_3, name_plot_3)

        all_top_words = freq_words(all_raw_words)

        name_plot_all = 'static\plot_all.png'
        plot_all = create_plot(all_top_words, name_plot_all)
        return redirect('stats')
    return render_template('intro.html')

def get_data(domain):
    p_list = []
    offset = 0
    count = 100
    for i in tqdm.tqdm(list(range(3))):
        offset += count * i
        request = requests_get(vk_api_base + '/wall.get', params={
            'domain': domain,
            'offset': offset,
            'access_token': token,
            'count': count,
            'v': '5.92'
        })
        p_list.extend(request.json()['response']['items'])
    return p_list


def split_words(text):
    return text.split()


def get_text(posts):
    words = []
    for post in posts:
        text = split_words(post['text'])
        for word in text:
            word = word.replace(',', '')
            word = word.replace('.', '')
            word = word.replace(':', '')
            word = word.replace('!', '')
            word = word.replace('?', '')
            word = word.replace('#', '')
            word = word.replace('‾', '')
            word = word.replace('_', '')
            if len(word) > 3  and len(word) < 10:
                words.append(word)
    # print(words)
    return words

def freq_words(raw_words):
    raw_words = Counter(raw_words)
    raw_words = dict(raw_words)
    raw_words = {c : raw_words[c] for c in raw_words if raw_words[c] > 5 and len(c) > 5}
    top_words = sorted(raw_words.items(), key=lambda x: x[1], reverse=True)[:10]
    return top_words


from scipy.interpolate import interp1d
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import style

style.use('ggplot')

def create_plot(topwords, plot_name):
    word_nums = []
    word_labs = []
    for t in topwords:
        word_labs.append(t[0])
        word_nums.append(t[1])

    plt.rc('xtick', labelsize=15)
    plt.rc('ytick', labelsize=15)


    plt.figure(figsize=(40, 10), dpi=80)
    plt.bar(word_labs, word_nums)


    plt.ylabel('Количество слов\n', fontsize=15)
    plt.xlabel('\nСлова', fontsize=15)


    plt.savefig(plot_name, dpi=300)




@app.route('/stats')
def searching():
    return render_template('stats.html')

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
    import os
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)



