
class Country:
    def __init__(self, country_name):
        self.country_name = country_name
        self.records = dict()


class Records:
    def __init__(self, date, total_cases, total_deaths, new_cases, new_deaths):
        self.date = date
        self.total_cases = total_cases
        self.total_deaths = total_deaths
        self.new_cases = new_cases
        self.new_deaths = new_deaths

    def __repr__(self):
        return f'<date:{self.date}, total_cases: {self.total_cases}, total_deaths: {self.total_deaths}, ' \
               f'new_cases: {self.new_cases}, new_deaths: {self.new_deaths}>'
