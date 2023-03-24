# SEG-venture-capital-portfolio
The Code of Duty Major Group Project Year2Sem2

## Authors
- SPARSH PATEL
- ROHAN DESAI
- PRATAP GUHA
- THATCHATHON LEELAWAT
- ABDUL (Abdul Rahman) MALLAH
- UMAIR QURESHI
- SHAAN VIERU

## Deployed version of the application
The deployed version of the application can be found at [*<http://tlthon.pythonanywhere.com/>*](http://tlthon.pythonanywhere.com/).

## Instructions

```
 $ virtualenv venv
 $ source venv/bin/activate
```

Install all required packages:

```
 $ pip3 install -r requirements.txt
```

Make necessary migrations(If "python" doesn't work, please use "python3"):
```
 $ python manage.py makemigrations manager
 or
 $ python manage.py makemigrations
```

Apply migrations:
```
 $ python manage.py migrate --run-syncdb
```


Run django server:
```
 $ python manage.py runserver
```

Run test:
```
 $ python manage.py test
```
Login:
- Click the login button on the Wayra homepage.
- To log in as an admin, the username is admin@wayra.co, and the password is password.
- To log in as a viewer, you need to log in as an admin, go to the "Accounts" page from the side-bar, click "Add New Account", then "Viewing Account" and enter the details you'd like for your viewing account before clicking submit. You should then be free to logout, and log in as a viewer, where your username is the email address, and the password is the password.

## Sources
The packages used by this application are specified in `requirements.txt`
