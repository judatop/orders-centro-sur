from flask import url_for
from flask_login import logout_user
from werkzeug.utils import redirect

from app import app


@app.route('/logout.html', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))
