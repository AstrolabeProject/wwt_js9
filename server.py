#!/usr/bin/python
from flask import Flask, request, send_file, redirect
import base64
import requests
app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def image_storage():
    if request.method == 'POST':
        split_data = request.data.split(b'&')
        url_data = base64.b64decode(split_data[0][26:])
        app.stored_image = open("saved.png", "wb")
        app.stored_image.write(url_data)
        app.stored_image.close()
        edit_wtml({'RA': split_data[2][3:], 'Dec': split_data[1][4:]})
        return 'success'
    else:
        return send_file('saved.png', mimetype='image/png')


@app.route('/images.wtml', methods=['GET'])
def wtml_return():
    return send_file('template.wtml')


@app.route('/images2.wtml', methods=['GET'])
def second_wtml_return():
    return send_file('images.wtml')

@app.route('/home', methods=['GET'])
def wwt_js9_home():
        return send_file('public/js9-1.12/WWT.html')


@app.route('/<file>', methods=['GET'])
def give_file(file):
    return send_file('public/js9-1.12/{}'.format(file))


def edit_wtml(dictionary):
    print('here is the dict')
    print(dictionary)
    with open('template.wtml', 'r') as old, open('images.wtml', 'w') as new:
        for line in old.readlines():
            try:
                attribute = list(filter(lambda x: x in line, list(dictionary.keys())))[0]
                new.write(' ' * 5 + attribute + '=' + '"' + dictionary[attribute].decode('utf-8') + '"' + '\n')
            except IndexError:
                new.write(line)



if __name__ == '__main__':
    # app.run()
    edit_wtml({'RA': b'1000', 'Dec': b'50'})
