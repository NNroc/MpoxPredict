import urllib.request

url = 'https://raw.githubusercontent.com/owid/monkeypox/main/owid-monkeypox-data.csv'
urllib.request.urlretrieve(url, "owid-monkeypox-data.csv")
