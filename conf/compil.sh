#!/usr/bin/env bash
#
# Installation du service Alexa
#

# Paramètres
app_name=alexa
app_path=/home/billerot/Git/alexa-flask
app_port=8088
app_user=alexa
app_user=billerot

# uitilisation de @ pour séparer les expressions
# car $app_path contient des /
sed "s@__APP_NAME__@$app_name@g" app.service > alexa.service
sed "s@__APP_PATH__@$app_path@g" -i alexa.service
sed "s@__APP_USER__@$app_user@g" -i alexa.service
sed "s@__APP_GROUP__@$app_group@g" -i alexa.service

sed "s@__APP_NAME__@$app_name@g" gunicorn_model.py > gunicorn.py
sed "s@__APP_PATH__@$app_path@g" -i gunicorn.py
sed "s@__APP_PORT__@$app_port@g" -i gunicorn.py
sed "s@__APP_USER__@$app_user@g" -i gunicorn.py

sed "s@__APP_PATH__@$app_path@g" logging_model.conf > logging.conf
