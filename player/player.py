# -*- coding: utf-8 -*-
import logging
from flask import Flask, Blueprint
from flask import request, g, current_app
import pygame
import time
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

player = Blueprint('main', __name__, url_prefix="/player")
#Initialisation Pygame
pygame.mixer.init()

@player.route('/')
def accueil():
  return 'Player à votre écoute\n'

@player.route('/play/<mediafile>')
def play(mediafile):
  logger.info(mediafile)
  logger.info(current_app.config)
  if "son" in current_app.config:
    current_app.config["son"].stop()
  filePath = os.path.join(player.root_path, 'media', mediafile)
  son = pygame.mixer.Sound(filePath)
  son.play(-1)
  current_app.config["son"] = son
  return 'Media: play {}\n'.format(mediafile)

@player.route('/stop')
def stop():
  logger.info("stop")
  logger.info(current_app.config)
  if "son" in current_app.config:
    current_app.config["son"].stop()
  return 'Media: stop\n'

# Tests unitaires
if __name__ == '__main__':
  # global app
  app = Flask(__name__)
  app.register_blueprint(player)
  app.run()