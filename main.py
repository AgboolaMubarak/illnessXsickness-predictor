import os
from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler, CommandHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton
import random
from modelling import *

telegram_bot_token = "5680510057:AAEpB_SAi6qFXpaW6D88uoIVq_pBoR3quz4"

updater = Updater(token=telegram_bot_token, use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text="Hello, my name is DisDetbot, and I can diagnose "
                                                   "illnesses based on the information provided about symptoms.")
    context.bot.send_message(chat_id=chat_id, text="In order for me to diagnose your illness,"
                                                   "I need you to list at least five symptoms.",
                             reply_markup=symptom_keyboard())
    return FIRST_STEP


def symptom_keyboard():
    keyboard = [[KeyboardButton('Enter Symptoms')]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)


def GetSymptom(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text="Enter symptom 1")
    return SECOND_STEP


def SetSymptom(update, context):
    chat_id = update.effective_chat.id
    open('trip.txt', 'w').write(update.message.text)
    with open('trip.txt') as f:
        txt = f.readlines()
    if " " in txt[0]:
        result = re.sub(r"\s+", '_', txt[0])
        open('problem.txt', 'w').write(result.lower())
        context.bot.send_message(chat_id=chat_id, text="Enter symptom 2")
    else:
        open('problem.txt', 'w').write(update.message.text.lower())
        context.bot.send_message(chat_id=chat_id, text="Enter symptom 2")

    return THIRD_STEP


def SetSymptom2(update, context):
    chat_id = update.effective_chat.id
    open('trip2.txt', 'w').write(update.message.text)
    with open('trip2.txt') as f:
        txt = f.readlines()
    if " " in txt[0]:
        result = re.sub(r"\s+", '_', txt[0])
        open('problem1.txt', 'w').write(result.lower())
        context.bot.send_message(chat_id=chat_id, text="Enter symptom 3")
    else:
        open('problem1.txt', 'w').write(update.message.text.lower())
        context.bot.send_message(chat_id=chat_id, text="Enter symptom 3")
    return FOURTH_STEP


def SetSymptom3(update, context):
    chat_id = update.effective_chat.id
    open('trip3.txt', 'w').write(update.message.text)
    with open('trip3.txt') as f:
        txt = f.readlines()
    if " " in txt[0]:
        result = re.sub(r"\s+", '_', txt[0])
        open('problem3.txt', 'w').write(result.lower())
        context.bot.send_message(chat_id=chat_id, text="Enter symptom 4")

    else:
        open('problem3.txt', 'w').write(update.message.text.lower())
        context.bot.send_message(chat_id=chat_id, text="Enter symptom 4")
    return FIFTH_STEP


def SetSymptom4(update, context):
    chat_id = update.effective_chat.id
    open('trip4.txt', 'w').write(update.message.text)
    with open('trip4.txt') as b:
        txt = b.readlines()
    if " " in txt[0]:
        result = re.sub(r"\s+", '_', txt[0])
        open('problem4.txt', 'w').write(result.lower())
        context.bot.send_message(chat_id=chat_id, text="Enter symptom 5")
    else:
        open('problem4.txt', 'w').write(update.message.text.lower())
        context.bot.send_message(chat_id=chat_id, text="Enter symptom 5")
    return SIXTH_STEP


def SetSymptom5(update, context):
    chat_id = update.effective_chat.id
    open('trip3.txt', 'w').write(update.message.text)
    with open('trip3.txt') as f:
        txt = f.readlines()
    if " " in txt[0]:
        result = re.sub(r"\s+", '_', txt[0])
        open('problem5.txt', 'w').write(result.lower())
    else:
        open('problem4.txt', 'w').write(update.message.text.lower())
        context.bot.send_message(chat_id=chat_id, text="Enter symptom 5")

    try:

        rep = SVM()
        context.bot.send_message(update.message.chat.id,
                                 "Based on your symptom profile, " + rep + "  is a strong possibility")
        val = random.randint(7, 9)
        context.bot.send_message(update.message.chat.id,
                                 "An appointment has been booked at the Unilag Health Center for you tommorow at "
                                 + str(val) + "am")
        return SIXTH_STEP

    except Exception:
        context.bot.send_message(update.message.chat.id,
                                 "Some of the symptoms you entered are not decodable by the model;"
                                 " please check your spelling")
    return FIRST_STEP

    raise


def cancel(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text='invalid values')
    return ConversationHandler.END


FIRST_STEP, SECOND_STEP, THIRD_STEP, FOURTH_STEP, FIFTH_STEP, SIXTH_STEP = range(6)

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],

    states={

        FIRST_STEP: [MessageHandler(Filters.text & ~Filters.command, GetSymptom)],

        SECOND_STEP: [MessageHandler(Filters.text & ~Filters.command, SetSymptom)],

        THIRD_STEP: [MessageHandler(Filters.text & ~Filters.command, SetSymptom2)],

        FOURTH_STEP: [MessageHandler(Filters.text & ~Filters.command, SetSymptom3)],

        FIFTH_STEP: [MessageHandler(Filters.text & ~Filters.command, SetSymptom4)],

        SIXTH_STEP: [MessageHandler(Filters.text & ~Filters.command, SetSymptom5)],

    },

    fallbacks=[CommandHandler('cancel', cancel)]
)
dispatcher.add_handler(conv_handler)

updater.start_webhook(listen="0.0.0.0",
                      port=int(os.environ.get('PORT', 5000)),
                      url_path=telegram_bot_token,
                      webhook_url="https://dashboard.heroku.com/apps/illness-detector-bot/" + telegram_bot_token
                      )
updater.bot.setWebhook('https://dashboard.heroku.com/apps/illness-detector-bot/' + telegram_bot_token)

updater.idle()

