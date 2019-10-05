#!/usr/bin/env bash
#
# Installation du service Alexa
#

# Faire un compil.sh avant d'exécuter ce script

# Paramètres
app_name=alexa
app_path=/home/billerot/Git/alexa-flask
app_port=8088
app_user=alexa
app_user=billerot


# Création du user
sudo adduser --no-create-home $app_user
sudo adduser $app_user billerot

# Création du service
sudo systemctl stop alexa.service
sudo cp alexa.service /etc/systemd/system/alexa.service
#sudo systemctl daemon-reload
sudo systemctl enable alexa.service
sudo systemctl start alexa.service
sudo systemctl status alexa.service
# journalctl -xe
# Test
# curl http://0.0.0.0:$app_port/player/
