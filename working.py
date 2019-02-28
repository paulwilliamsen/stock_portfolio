
    if request.method == 'POST':
        companyName = request.form.get('company')

        url = 'https://api.iextrading.com/1.0/stock/{}}/company'.format(
            os.environ.get('API_URL'),
            companyName,
            os.environ.get('API_KEY'),
        )

        res = requests.get(url)
        data = json.loads(res.text)

        try:
            company = Company(name=data['company'],)
            db.session.add(company)
            db.session.commit()
        except (DBAPIError, IntegrityError):
            abort(400)

        return redirect(url_for('.weather_detail'))

