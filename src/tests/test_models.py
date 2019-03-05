from src.models import Company


class TestClass:
    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def test_create_city(self, session):
        company = Company(name='Google', symbol='goog')

        session.add(company)
        session.commit()

        assert company.id > 0

        company = Company.query.all()

        assert len(company) == 1

        assert company[0].name == 'Bellevue'

    def test_create_city_again(self, session):
        company = Company(name='Google', symbol='goog')
        session.add(company)
        session.commit()

        assert company.id > 0

        company = Company.query.all()

        assert len(company) == 1

    def test_tc2(self):
        pass