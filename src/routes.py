from flask import render_template, abort, redirect, url_for, request, session
from sqlalchemy.exc import DBAPIError, IntegrityError
from . import app
from .forms import CompanyForm, CompanyAddForm
from .models import Company, db
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

    form = CompanyForm()


    if form.validate_on_submit():
        symbol = form.data['symbol']

        url = f'https://api.iextrading.com/1.0/stock/{symbol}/company'

        response = requests.get(url)
        data = json.loads(response.text)
        session['name'] = data['companyName']
        session['symbol'] = data['symbol']
        #might need brackets

        return redirect(url_for('.company_preview'))

    return render_template('company/search.html', form=form)


@app.route('/preview', methods=['GET', 'POST'])
def company_preview():
    """
    """
    form_context = {
        'name': session['name'],
        'symbol': session['symbol'],
    }
    form = CompanyAddForm(**form_context)

    if form.validate_on_submit():
        try:
            company = Company(name=form.data['companyName'], symbol=form.data['symbol'])
            db.session.add(company)
            db.session.commit()
        except (DBAPIError, IntegrityError):
            abort(400)
            return render_template('/.html', form=form)

        return redirect(url_for('company/portfolio.html'))

    return render_template(
        '/preview.html',
        form=form,
        name=form_context['name'],
        symbol=session['symbol'],
    )



@app.route('/portfolio')
def portfolio():
    """
    """
    return render_template('company/portfolio.html')

        
        