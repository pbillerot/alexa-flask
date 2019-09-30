# -*- coding: utf-8 -*-
"""
  Point d'entrée du skill Alexa

"""
import logging
from logging.handlers import RotatingFileHandler

import os
from flask import Flask
from flask_ask_sdk.skill_adapter import SkillAdapter

from alexa.skill import sb

# création de l'objet logger qui va nous servir à écrire dans les logs
logger = logging.getLogger()
# on met le niveau du logger à DEBUG, comme ça il écrit tout
logger.setLevel(logging.DEBUG)
# création d'un formateur qui va ajouter le temps, le niveau
# de chaque message quand on écrira un message dans le log
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
# création d'un handler qui va rediriger une écriture du log vers
# un fichier en mode 'append', avec 1 backup et une taille max de 5Mo
file_handler = RotatingFileHandler('log/alexa.log', 'a', 5000000, 1)
# on lui met le niveau sur DEBUG, on lui dit qu'il doit utiliser le formateur
# créé précédement et on ajoute ce handler au logger
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
# création d'un second handler qui va rediriger chaque écriture de log
# sur la console
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)

def create_app():
  app = Flask(__name__)
  skill_adapter = SkillAdapter(
    skill=sb.create(), 
    skill_id="amzn1.ask.skill.bd7515ac-93e7-48c6-b2b5-58dcd0fb0951", 
    app=app)
  skill_adapter.register(app=app, route="/alexa")
  logger.info("Alexa en marche...")
  return app

app = create_app()
