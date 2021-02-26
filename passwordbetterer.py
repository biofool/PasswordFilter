# Passwords from
# https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt
"""
export FLASK_APP=passwordbetterer.py
export FLASK_ENV=development
flask run
"""
# def passworddecensy(password):
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import random
import string

compromised = ()


def get_random_string(length: int) -> object:
    """

    @rtype: object
    """
    # choose from all lowercase letter
    letters = string.printable
    result_str = ''.join(random.choice(letters) for i in range(length))
    # if (result_str in badwords):
    #     result_str = get_random_string(length)
    return result_str


def init(custombadwordfile):
    global compromised
    if custombadwordfile:
        badwordfile = custombadwordfile
    else:
        badwordfile = '10-million-password-list-top-1000000.txt'
    with open(badwordfile) as compromised10K:
        compromised = set(map(str.rstrip, compromised10K))
    return '{} compromised passwords injested', len(compromised)
    # Validate


app = Flask(__name__)
app.config['SECRET_KEY'] = get_random_string(15)


# import time

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    global post
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    if len(compromised) == 0:
        init("10-million-password-list-top-1000000.txt")

    return render_template('index.html')


# ('10-million-password-list-top-1000000.txt')
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form ['user']
        content = request.form ['password']

        if not title:
            flash('User is required!')
        elif len(content) < 8:
            flash("Password length must exceed 8 characters")

        elif content in compromised:
            flash("That password is in the list of most commonly used passwords and is banned")
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form ['title']
        content = request.form ['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)
