command = '/home/billerot/Git/alexa-flask/venv/bin/gunicorn'
pythonpath = '/home/billerot/Git/alexa-flask'
workers = 3
user = 'billerot'
bind = '0.0.0.0:8088'
logconfig = "/home/billerot/Git/alexa-flask/conf/logging.conf"
capture_output = True
timeout = 90
