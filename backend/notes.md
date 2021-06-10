
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

Auth0 INFO:
Domain:
```
dev-bfn-8r1t.eu.auth0.com
```
Client ID:
```
5tHDsFBmk1BCUrvSvJS4DAmHYLoych1E
```
Api Name and Identifier:
```
casting_agency
```

Go to:
https://dev-bfn-8r1t.eu.auth0.com/authorize?audience=casting_agency&
response_type=token&client_id=5tHDsFBmk1BCUrvSvJS4DAmHYLoych1E&redirect_uri=https://127.0.0.1:8080/logout

change the token variable in test_app.py, and in postman(export after)

Scale up the minimap to 2 in VSCode for comment headlines to take effect.