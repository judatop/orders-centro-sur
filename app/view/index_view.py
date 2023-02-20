from flask import render_template, url_for
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from werkzeug.utils import redirect

from app import app


@app.route('/', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
@login_required
def index():
    try:
        params = []
        return render_template("index.html", segment="index", params=params)
    except TemplateNotFound:
        return render_template('page-404.html'), 404
