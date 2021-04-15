# Network Monitor
Application displays network speed (both download, and upload) from given time period. Uses Python and Django to implement Cron job, that stores data, and web app to display the data in browser. Data is stored in SQLite.


### Prerequisites
- Python
- Pip
- Virtualenv
- SQlite


### Create virtualenv (Virtualenv), actiavet and deactivate 
1. Create virtual environment `virtualenv venv`
2. Activate virtual environment `source venv/bin/activate`
3. Do 'stuff' (look below)
4. Deactivate virtual environment `deactivate`



### Running
1. Install dependencies: `pip3 install -r requrements.txt`
2. Migrate database: 
- `python3 manage.py migrate`
- `python3 manage.py makemigrations network`
3. Create Admin: `python3 manage.py createsuperuser`
4. Manage Cron jobs: 
- add cron job for persisting metrics: `python3 manage.py crontab add`
- make sure it is added: `python3 manage.py crontab show`
- remove added job (for stopping persisting metrics): `python3 manage.py crontab remove`
5. Start server `python3 manage.py runserver`
6. Navigate in browser to `http://127.0.0.1:8000` or `http://127.0.0.1:8000/admin`

