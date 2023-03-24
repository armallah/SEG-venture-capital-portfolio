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

## Sources
The packages used by this application are specified in `requirements.txt`
