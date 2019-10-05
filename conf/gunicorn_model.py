command = '__APP_PATH__/venv/bin/gunicorn'
pythonpath = '__APP_PATH__'
workers = 3
user = '__APP_USER__'
bind = '0.0.0.0:__APP_PORT__'
logconfig = "__APP_PATH__/conf/logging.conf"
capture_output = True
timeout = 90
