from flask import render_template

from app.main import bp
import os
import markdown as md

# @bp.route('/')
# def index():
#     return render_template('index.html')


@bp.route('/')
def index():
    if os.path.isfile('README.md'):
        with open('README.md') as plik_md:
            plik_md_html = md.markdown(plik_md.read(), extensions=['tables', 'markdown.extensions.fenced_code'])
    else:
        plik_md_html = None
    return render_template("index.html", md=plik_md_html)
