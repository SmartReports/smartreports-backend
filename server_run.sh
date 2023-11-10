pip3 install -r requirements.txt
pip3 freeze > requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate --fake
python3 manage.py migrate --run-syncdb
python3 manage.py runserver 
