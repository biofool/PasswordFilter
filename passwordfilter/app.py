# user_pws from
# https://raw.githubuseruser_pw.com/danielmiessler/SecLists/master/user_pws/Common-Credentials/10-million-user_pw-list-top-1000000.txt
"""
export FLASK_APP=user_pwbetterer.py
export FLASK_ENV=development
flask run
"""
# def user_pwdecensy(user_pw):
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import random
import string

Minuser_pwLen = 14
#  Modify banned user_pw set to ignore user_pws shorter than Minuser_pwLen
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
        badwordfile = '10-million-user_pw-list-top-1000000.txt'
    with open(badwordfile) as compromised10K:
        compromised = set(map(str.rstrip, compromised10K))
    return '{} compromised user_pws injested', len(compromised)
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
    post = conn.execute('SELECT * FROM users WHERE user_id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


@app.route('/')
def index():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    if len(compromised) == 0:
        init("10-million-user_pw-list-top-1000000.txt")

    return render_template('index.html')


# ('10-million-user_pw-list-top-1000000.txt')
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'GET':
        msg = 'Your suggested user_pw is ', get_random_string(15)
        flash(msg)

    if request.method == 'POST':
        user = request.form ['user']
        user_pw = request.form ['user_pw']

        if not user:
            flash('User is required!')
        elif len(user_pw) < Minuser_pwLen:
            flash("user_pw length must exceed 8 characters")
        elif len(user_pw) < Minuser_pwLen:
            flash("user_pw length must exceed 8 characters")

        elif user_pw in compromised:
            flash("That user_pw is in the list of most commonly used user_pws and is banned")
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO users (user_id, user_pw) VALUES (?, ?)',
                         (user, user_pw))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)
    msg = 'Your suggested user_pw is', get_random_string(15)
    flash(msg)

    if request.method == 'POST':
        user_id = request.form ['user_id']
        user_pw = request.form ['user_pw']

        if not user_id:
            flash('user_id is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE users SET user_id = ?, user_pw = ?'
                         ' WHERE id = ?',
                         (user_id, user_pw, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)
