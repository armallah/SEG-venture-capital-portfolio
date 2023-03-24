# SEG-venture-capital-portfolio
The Code of Duty Major Group Project Year2Sem2

## Authors
SPARSH PATEL
ROHAN DESAI
PRATAP GUHA
THATCHATHON LEELAWAT
ABDUL (Abdul Rahman) MALLAH
UMAIR QURESHI
SHAAN VIERU

## Instructions

```
 $ virtualenv venv
 $ source venv/bin/activate
```

Install all required packages:

```
 $ pip3 install -r requirements.txt
```

Make necessary migrations:
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
