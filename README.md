# Case  &middot; [![Django 2.2.4](https://img.shields.io/badge/Django-2.2.4-brightgreen)](https://docs.djangoproject.com/en/2.2/releases/2.2.4/) [![Python 3.7.2](https://img.shields.io/badge/python-3.7.2-blue.svg)](https://www.python.org/downloads/release/python-372/)

Case is a web application written using the Django Framework for Dr. Kenneth Lee and students studying Pharmacy at the University of Western Australia.

The purpose of the application is to allow students to populate a database with case studies that they have experienced, so that other users can attempt the case. Additionally it gives students an opportunity to try more cases, than currently available in the course.

## Authors
- [Haolin Wu](https://github.com/Dragonite)
- [Jonathan Neo](https://github.com/jonathanneo)
- [Tim Ings](https://github.com/tim-ings)
- [Jaydeep Gajera](https://github.com/JD-08)
- [Hugo Zhang](https://github.com/hugozhangc)
- [Aaron Jenkins](https://github.com/)

## License

This project is licensed under the  [MIT License](https://github.com/320011/case/blob/master/LICENSE).

## Deployment

### Database Server

1. Install postgres 9.5 or greater

2. Set up postgres database for case with associated user

3. Allow postgres connections to the app server

### App Server:

Distribution: Red Hat Enterprise 7

1. Install EPEL repo

```bash
yum install epel-release
````

2. Install required packages

```bash
yum install python-pip python-devel gcc nginx
```
    
3. Clone the project

```bash
git clone https://github.com/320011/case
```
    
4. Set up and activate a virtualenv inside case root

```bash
pip install virtualenv
virtualenv venv
. venv/bin/activate
```

5. Install pip requirements (including production specific)

```bash
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```
    
6. Create `local_settings.py` file in the same directory as `settings.py` and populate it with required data

````python
import os

ALLOWED_HOSTS = ["example.com"]

DEBUG = False

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_ROOT = "/path/to/static/for/nginx"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db_name',
        'USER': 'db_user',
        'PASSWORD': 'db_pass',
        'HOST': 'db_host',
    }
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'my.smtp.server'
EMAIL_HOST_USER = "case@example.com"
EMAIL_HOST_PASSWORD = "email_app_password"
EMAIL_PORT = 587
````

7. Collect static files for Nginx to serve

```bash
python manage.py collectstatic
```

8. Create systemd daemon for gunicorn

```bash
vim /etc/systemd/system/gunicorn.service
```

```
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=case_linux_user
Group=nginx
WorkingDirectory=/path/to/repo/core
ExecStart=/path/to/repo/venv/bin/gunicorn --workers 3 --bind unix:/path/to/repo/case.sock core.wsgi:application

[Install]
WantedBy=multi-user.target
```

9. Create an Nginx server block inside `http {...}` (or use SSL here)

```bash
vim /etc/nginx/nginx.conf
```
    
```c
http {
    ...
    
    server {
        listen 80;
        server_name example.com;

        location = /favicon.ico {
            alias /path/to/staticfiles/favicon.ico;
        }
        location /static/ {
            alias /path/to/staticfiles/;
        }

        location / {
            proxy_set_header Host $http_host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_pass http://unix:/path/to/repo/case.sock;
        }
    }
    
    ...
}
```

10. Allow port 80 through the firewall

11. Grant nginx file permissions to execute (important) your staticfiles directory

12. Compile scss files into css. Follow the instructions [here](https://sass-lang.com/install) to download sass and compile

13. Once the database is running, migrate our django models to it

```bash
python manage.py makemigrations
python manage.py migrate
```

14. Start and enable systemd daemons

```bash
systemctl start gunicorn
systemctl enable gunicorn
systemctl start nginx
systemctl enable nginx
```
