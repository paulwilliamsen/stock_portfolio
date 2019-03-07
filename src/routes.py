from flask import render_template, abort, redirect, url_for, request, session, flash
from sqlalchemy.exc import DBAPIError, IntegrityError
from . import app
from .forms import CompanyForm, CompanyAddForm, PortfolioCreateForm
from .models import Company, db, Portfolio
import requests
import json
import os

@app.add_template_global
def get_portfolios():
    """
    """
    return Portfolio.query.all()


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
            company = Company(name=form.data['name'], portfolio_id=form.data['portfolios'], symbol=form.data['symbol'])
            db.session.add(company)
            db.session.commit()
        except (DBAPIError, IntegrityError):
            flash('Oops. Something went wrong with your search.')
            db.session.rollback()
            return render_template('/company/search.html', form=form)

        return redirect(url_for('company/portfolio.html'))

    return render_template(
        'company/preview.html',
        form=form,
        name=form_context['name'],
        symbol=session['symbol'],
    )



@app.route('/portfolio', methods=['POST'])
def portfolio():
    """
    """

    form = PortfolioCreateForm()\

    if form.validate_on_submit():
        try:
            portfolio = Portfolio(portfolio_name=form.data['name'])
            db.session.add(portfolio)
            db.session.commit()
        except (DBAPIError, IntegrityError):
            flash('Oops. Something went wrong with your search.')
            return render_template('company/portfolio.html')
        return redirect(url_for('.company_search'))

    portfolio = Portfolio.query.all()
    return render_template('company/portfolio.html', portfolio=portfolio, form=form)
        

