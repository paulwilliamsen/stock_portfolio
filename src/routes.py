from flask import render_template, abort, redirect, url_for, request
from sqlalchemy.exc import DBAPIError, IntegrityError
from . import app
from .models import Company, db
import requests
import json
import os


@app.route('/')
def home():
    """
    """
    return render_template('home.html')


@app.route('/search', methods=['GET'])
def company_search_form():
    """
    """
    return render_template('/search.html')

@app.route('/search', methods=['POST'])
def company_search_results(): 
    symbol = request.form.get('symbol') 


    url = f'https://api.iextrading.com/1.0/stock/{symbol}/company'

    response = requests.get(url)

    data = json.loads(response.text)

    company = Company(name=data['companyName'], symbol=['symbol'])

    return response.text  

    db.session.add(company)
    db.session.commit()

    return redirect(url_for('.portfolio'))

        # Use try/except in future
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