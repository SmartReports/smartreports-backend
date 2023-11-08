pip install -r requirements.txt
pip freeze > requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py migrate --run-syncdb 
python manage.py runserver 