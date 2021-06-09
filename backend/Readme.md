
Start virual enviroment:
```
py -3.7 -m venv venv
venv\Scripts\activate
```

Set enviroment variables:
```
$env:DB_USER = "postgres"
$env:DB_PASSWORD = "piko"
```

Run backend:
```
python app.py
```

Run tests:
```
dropdb -U postgres casting_agency_test
python test_app.py -v
```

Scale up the minimap to 2 in VSCode for comment headlines to take effect.