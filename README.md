alexa-flask
===========

Service Alexa écrit en Flask Python


Python dans un environnement virtuel 3.6
----------------------------------------
```
virtualenv -p python3 venv
source venv/bin/activate
pip install flask ask-sdk flask-ask-sdk
pip install gunicorn
pip install pygame
# Pour environnement de Dev VSCodium
pip install pylint rope
```

Tests unitaires
---------------
    source venv/bin/activate
    gunicorn --bind 127.0.0.1:8088 app:app

