import sys
import argparse
from flask import Flask
from flask_cors import CORS


DEBUG = False
modules = {}
app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    with open('templates/index.html', encoding='utf-8') as file_handle:
        return file_handle.read()

@app.route('/book')
def book():
    with open('templates/book.html', encoding='utf-8') as file_handle:
        return file_handle.read()

@app.route('/rpg2')
def rpg2():
    with open('templates/rpg2.html', encoding='utf-8') as file_handle:
        return file_handle.read()

def parse_args(args):
    global DEBUG

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true')

    args = parser.parse_args(args)

    if args.debug:
        DEBUG = True

    return args


if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    app.run()
