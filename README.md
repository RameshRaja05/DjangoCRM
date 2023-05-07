
# DjangoCRM

DjangoCRM is an open source CRM (Customer Relationship Management) system based on Django framework. It has all the basic features of a CRM to start with, such as contacts, accounts, leads, opportunities, cases, invoices, and planner. You can use DjangoCRM to manage your customers, sales, and tasks easily and efficiently.

## Features

- User authentication and authorization
- User profile and settings
- Contacts management
- Accounts management
- Leads management
- Opportunities management
- Cases management
- Status management


## Installation

To install DjangoCRM, you need to have Python 3.8+ installed on your system. You also need to install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

Then, you need to set up some environment variables in a .env file in the project root directory.

In template.env file you can find what are the api keys you need to get start with.

Next, you need to create a database and a user for DjangoCRM in PostgreSQL:

```bash
sudo -u postgres psql
CREATE DATABASE djangocrm;
CREATE USER djangocrm WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE djangocrm TO djangocrm;
\q
```

Then, you need to run the database migrations and create a superuser account:

```bash
python manage.py migrate
python manage.py createsuperuser
```

Finally, you can run the development server:

```bash
python manage.py runserver
```

You can access the DjangoCRM web interface at http://localhost:8000.

## Usage

To use DjangoCRM, you need to register a new account with a company name and an email address. You can use test as the company name if you are running the project locally. Then, you can log in with your credentials and start using the CRM features.

You can add, edit, delete, and view contacts, accounts, leads. You can also send emails to your contacts and leads, and track their status.

You can also customize your profile and settings by clicking on your username in the top right corner. You can change your password, email preferences.

## License

DjangoCRM is licensed under the MIT License. See the LICENSE file for more information.


(1) django-crm · PyPI. https://pypi.org/project/django-crm/.
(2) MicroPyramid/Django-CRM: Open Source CRM based on Django - Github. https://github.com/MicroPyramid/Django-CRM.
(3) Django CRM — Django-CRM 0.7.0 documentation. https://django-crm.readthedocs.io/en/latest/.

##Mentions

## Learn more about Django

It's inspired from this youtube channel Justdjango's tutorial get started with django. It's a 9 hour long video. He walks through all important concepts such as Authentication,Authorization,Permisssion,Reset password. Feel free to check it out.



If you want to learn more about Django and how to build web applications with it, you can check out the YouTube channel JustDjango. JustDjango is a learning resource dedicated to web development with a focus on Django. It has many videos and courses that cover various topics and projects related to Django, such as ecommerce, chat, authentication, payments, and more. You can find the channel here: https://www.youtube.com/channel/UCRM1gWNTDx0SHIqUJygD-kQ


(1) JustDjango - YouTube. https://www.youtube.com/channel/UCRM1gWNTDx0SHIqUJygD-kQ.
(2) Learn web development with Django | JustDjango. https://justdjango.com/blog.
(3) GITHUB repo -https://github.com/justdjango/getting-started-with-django
(4) Specific video link -https://youtu.be/fOukA4Qh9QA
