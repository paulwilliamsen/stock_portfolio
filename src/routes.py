from flask import render_template, abort, redirect, url_for, request
from sqlalchemy.exc import DBAPIError, IntegrityError
from . import app
import requests
import json
import os


@app.route('/')
def home():
    """
    """
    return render_template('home.html')


@app.route('/search', methods=['GET', 'POST'])
def company_search():
    """
    """
    if request.method == 'GET':
        return render_template('/search.html')
      
    elif request.method == 'POST':
        companyName = request.form.get('company')

        url = 'https://api.iextrading.com/1.0/stock/{}}/company'.format(
            os.environ.get('API_URL'),
            companyName,
            os.environ.get('API_KEY'),
        )

        res = requests.get(url)
        data = json.loads(res.text)

        return redirect(url_for('/portfolio.html'))

        # return render_template('/portfolio.html')
        # try:
        #     company = Company(name=data['company'],)
        #     db.session.add(company)
        #     db.session.commit()
        # except (DBAPIError, IntegrityError):
        #     abort(400)




@app.route('/portfolio')
def portfolio():
    """
    """
    return render_template('/portfolio.html')