from flask import render_template, redirect, url_for, abort
from app.main import main



#views
@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''

    title = 'Home - Welcome to Exhibit Pitch'
    return render_template('index.html', title = title)