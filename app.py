# -*- coding: utf-8 -*-
"""
  https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/legacy.html
  https://developer.amazon.com/fr/docs/alexa-skills-kit-sdk-for-python/overview.html
  
"""

# This is a simple Hello World Alexa Skill, built using
# the implementation of handler classes approach in skill builder.
import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name, get_slot, get_slot_value
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.interfaces.audioplayer import (
    PlayDirective, PlayBehavior, AudioItem, Stream, AudioItemMetadata,
    StopDirective, ClearQueueDirective, ClearBehavior)
from ask_sdk_model.ui import StandardCard, Image

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response
from ask_sdk_model.slu.entityresolution import StatusCode

from flask import Flask, jsonify
from flask_ask_sdk.skill_adapter import SkillAdapter

import requests
import configparser
import os

from conf.app_conf import URL_PLAYER

currentDir = os.path.dirname(os.path.realpath(__file__))
config = configparser.ConfigParser()

# C'est une application Flask
app = Flask(__name__)
@app.route('/alexa') # capture du mode GET seulement
def accueil():
  message = "Alexa a votre ecoute..."
  info(message)
  return jsonify(message)
@app.route('/alexa/play/<fileName>')
def play(fileName):
  url = f"{URL_PLAYER}/play/{fileName}"
  message = f"Player {url}"
  info(message)
  requests.get(url=url)
  return jsonify(message)
@app.route('/alexa/stop')
def stop():
  url = f"{URL_PLAYER}/stop"
  message = f"Player {url}"
  info(message)
  requests.get(url=url)
  return jsonify(message)

sb = SkillBuilder()

# Initialisation du Skill
def create_skill():
  skill_adapter = SkillAdapter(
    skill=sb.create(), 
    skill_id="amzn1.ask.skill.bd7515ac-93e7-48c6-b2b5-58dcd0fb0951", 
    app=app)
  # Déclaration de la route
  skill_adapter.register(app=app, route="/alexa")

class ParoleIntentHandler(AbstractRequestHandler):
  def get_slot_id(self, slot):
    # debug(f"get_slot_id:{slot}")
    try:
      if slot.resolutions is not None:
        status = slot.resolutions.resolutions_per_authority[0].status.code
        # debug(f"for {slot.name} status={status}")
        if status == StatusCode.ER_SUCCESS_MATCH:
          id = slot.resolutions.resolutions_per_authority[0].values[0].value.id
          return id
        else:
          return None
      else:
        return None
    except:
      print(f"ERROR slot:{slot}")
      return None

  def can_handle(self, handler_input):
    return is_intent_name("ParoleIntent")(handler_input)

  def handle(self, handler_input):
      slots = handler_input.request_envelope.request.intent.slots
      slot_morceau = None
      slot_couplet = None
      slot_refrain = None
      morceau = "Morceau"
      couplet = "Couplet"
      refrain = "Refrain"
      if morceau in slots:
          slot_morceau = self.get_slot_id(slots[morceau])
      if couplet in slots:
          slot_couplet = self.get_slot_id(slots[couplet])
      if refrain in slots:
          slot_refrain = self.get_slot_id(slots[refrain])

      speech_text = "Paroles non trouvées"
      try:
          if slot_morceau is not None:
              config.read(currentDir + "/conf/songs.ini")
              if slot_couplet is not None:
                  speech_text = config.get(
                      slot_morceau, slot_couplet).replace("\n", ", ")
              if slot_refrain is not None:
                  speech_text = config.get(
                      slot_morceau, slot_refrain).replace("\n", ", ")
      except:
          speech_text = "Erreur recherche "

      debug(
          f"morceau: {slot_morceau} couplet:{slot_couplet} refrain:{slot_refrain}")

      handler_input.response_builder.speak(
          speech_text).set_should_end_session(False)
      return handler_input.response_builder.response
sb.add_request_handler(ParoleIntentHandler())

class TempoIntentHandler(AbstractRequestHandler):
  def get_slot_id(self, slot):
    # debug(f"get_slot_id:{slot}")
    try:
      if slot.resolutions is not None:
        status = slot.resolutions.resolutions_per_authority[0].status.code
        # debug(f"for {slot.name} status={status}")
        if status == StatusCode.ER_SUCCESS_MATCH:
          id = slot.resolutions.resolutions_per_authority[0].values[0].value.id
          return id
        else:
          return None
      else:
        return None
    except:
      print(f"ERROR slot:{slot}")
      return None

  def can_handle(self, handler_input):
    return is_intent_name("TempoIntent")(handler_input)

  def handle(self, handler_input):
      slots = handler_input.request_envelope.request.intent.slots
      # debug(slots)
      slot_tempo = None
      tempo = "Tempo"
      if tempo in slots:
        slot_tempo = self.get_slot_id(slots[tempo])

      speech_text = ""
      morceau = "???"
      try:
        if slot_tempo is not None:
          requests.get(url=f"{URL_PLAYER}/play/{slot_tempo}")
        else:
          speech_text = "Je n'ai pas trouvé le morceau"
      except:
          speech_text = "Ya un bug"

      debug(f"player: {slot_tempo}")

      handler_input.response_builder.speak(
          speech_text).set_should_end_session(False)
      return handler_input.response_builder.response
sb.add_request_handler(TempoIntentHandler())

class HelloIntentHandler(AbstractRequestHandler):
    """Handler for Hello Intent."""

    def can_handle(self, handler_input):
        return is_intent_name("HelloIntent")(handler_input)

    def handle(self, handler_input):
        debug("Hello")
        speech_text = "Bonjour, le métro est en gare"
        handler_input.response_builder.speak(
            speech_text).set_should_end_session(False)
        return handler_input.response_builder.response
sb.add_request_handler(HelloIntentHandler())

"""
  Request alexa obligatoire
"""
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        info("LaunchRequest Métro")
        speech_text = "Ok le métro est en gare"

        handler_input.response_builder.speak(
            speech_text).set_should_end_session(False)
        return handler_input.response_builder.response

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        debug("HelpIntent")
        speech_text = "Tu peux me dire bonjour!"

        handler_input.response_builder.speak(
            speech_text).set_should_end_session(False)
        return handler_input.response_builder.response

class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        debug("CancelOrStopIntent")
        speech_text = "Bye!"
        requests.get(url=f"{URL_PLAYER}/stop")
        handler_input.response_builder.speak(
            speech_text).set_should_end_session(True)
        return handler_input.response_builder.response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        debug("SessionEndedRequest")
        debug(handler_input)
        # requests.get(url=f"{URL_PLAYER}/stop")
        return handler_input.response_builder.response

class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """

    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        error(exception)
        speech = "Désolé, ya un bug dans le programme de Barbichu !!"
        handler_input.response_builder.speak(speech).ask(speech)
        requests.get(url=f"{URL_PLAYER}/stop")
        return handler_input.response_builder.response

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_exception_handler(CatchAllExceptionHandler())

def info(message):
  app.logger.info(message)
def error(message):
  app.logger.error(message)
def debug(message):
  app.logger.debug(message)

# Test unitaires
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8088, debug=True)

handler = sb.lambda_handler()
create_skill()
app.logger.setLevel(logging.DEBUG)
info("Alexa en marche...")

