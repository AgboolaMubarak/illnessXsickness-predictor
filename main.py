import numpy as np
import pandas as pd
from flask import Flask, request, make_response
from flask_restful import Api, Resource

import json
from flask_cors import cross_origin
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

import random

import telebot
from modelling import *
from telebot import types

API_KEY = "5680510057:AAEpB_SAi6qFXpaW6D88uoIVq_pBoR3quz4"
bot = telebot.TeleBot(API_KEY)

button = types.KeyboardButton("Enter Symptoms")
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button)


@bot.message_handler(commands=["start"])
def greet(message):
    bot.reply_to(message, "Hello, my name is DisDetbot, and I can diagnose illnesses based on the information "
                          "provided about symptoms.")
    bot.reply_to(message, "In order for me to diagnose your illness, "
                          "I need you to list at least five symptoms.", reply_markup=keyboard)


@bot.message_handler()
def GetSymptom(message):
    mess = bot.send_message(message.chat.id, "Enter symptom 1")
    bot.register_next_step_handler(mess, Set_Symptom)


def Set_Symptom(message):
    open('problem.txt', 'w').write(message.text.lower())
    messu = bot.send_message(message.chat.id, 'Enter symptom 2!')
    bot.register_next_step_handler(messu, Set_Symptom2)


def Set_Symptom2(message):
    open('problem1.txt', 'w').write(message.text.lower())
    messup = bot.send_message(message.chat.id, 'Enter symptom 3!')
    bot.register_next_step_handler(messup, Set_Symptom3)


def Set_Symptom3(message):
    open('problem3.txt', 'w').write(message.text.lower())
    messupp = bot.send_message(message.chat.id, 'Enter symptom 4!')
    bot.register_next_step_handler(messupp, Set_Symptom4)


def Set_Symptom4(message):
    open('problem4.txt', 'w').write(message.text.lower())
    messuppp = bot.send_message(message.chat.id, 'Enter symptom 5!')
    bot.register_next_step_handler(messuppp, Set_Symptom5)


def Set_Symptom5(message):
    open('problem5.txt', 'w').write(message.text.lower())
    try:
        rep = SVM()
        bot.send_message(message.chat.id, "Based on your symptom profile, " + rep + "  is a strong possibility")
        val = random.randint(7, 9)
        bot.send_message(message.chat.id,
                         "An appointment has been booked at the Unilag Health Center for you tommorow at "
                         + str(val) + "am")
    except Exception:
        bot.send_message(message.chat.id, "Some of the symptoms you entered are not decodable by the model;"
                                          " please try again with an underscore between compound words.")
        raise


bot.infinity_polling()
# app = Flask(__name__)

# @app.route('/')
# def index():
#     return "<h1>Welcome!</h1>"
#
