import os
from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler, CommandHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton
import random
from modelling import *
import json

telegram_bot_token = "5680510057:AAEpB_SAi6qFXpaW6D88uoIVq_pBoR3quz4"

thesymptoms = {}


def start(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text="Hello, my name is DisDetbot, and I can diagnose "
                                                   "illnesses based on the information provided about symptoms.")
    context.bot.send_message(chat_id=chat_id, text="click button below keyboard to enter symptoms",
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
    # with open("trips.json", "w") as outfile:
    #     diction = {chat_id: update.message.text.lower()}
    #     json.dump(diction, outfile)
    diction = {chat_id: update.message.text.lower()}
    # with open('trip.txt') as f:
    txt = diction[chat_id]
    if " " in txt:
        result = re.sub(r"\s+", '_', txt)
        bin = chat_id + 1
        thesymptoms[str(bin)] = result
        context.bot.send_message(chat_id=chat_id, text="Enter symptom 2")
    else:
        bin = chat_id + 1
        thesymptoms[str(bin)] = update.message.text.lower()
        context.bot.send_message(chat_id=chat_id, text="Enter symptom 2")

    return THIRD_STEP


# function to add to JSON
def write_json(new_data, chat_id, filename='data.json'):
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        ben = "symp" + str(chat_id)
        file_data[ben] = new_data
        json.dump(file_data, file, indent=4)


def SetSymptom2(update, context):
    chat_id = update.effective_chat.id
    kit = chat_id + 3
    diction = {kit: update.message.text.lower()}
    txt = diction[kit]

    if " " in txt:
        result = re.sub(r"\s+", '_', txt)
        bin = chat_id + 2
        thesymptoms[str(bin)] = result
        context.bot.send_message(chat_id=chat_id, text="Enter symptom 3")
    else:
        bin = chat_id + 2
        thesymptoms[str(bin)] = update.message.text.lower()
        context.bot.send_message(chat_id=chat_id, text="Enter symptom 3")
    return FOURTH_STEP


def SetSymptom3(update, context):
    chat_id = update.effective_chat.id

    kit = chat_id + 4
    diction = {kit: update.message.text.lower()}
    txt = diction[kit]

    if " " in txt:
        result = re.sub(r"\s+", '_', txt)
        bin = chat_id + 3
        thesymptoms[str(bin)] = result
        context.bot.send_message(chat_id=chat_id, text="Enter symptom 4")

    else:
        bin = chat_id + 3
        thesymptoms[str(bin)] = update.message.text.lower()
        context.bot.send_message(chat_id=chat_id, text="Enter symptom 4")
    return FIFTH_STEP


def SetSymptom4(update, context):
    chat_id = update.effective_chat.id

    kit = chat_id + 5
    diction = {kit: update.message.text.lower()}
    txt = diction[kit]
    if " " in txt:
        result = re.sub(r"\s+", '_', txt)
        bin = chat_id + 4
        thesymptoms[str(bin)] = result
        context.bot.send_message(chat_id=chat_id, text="Enter symptom 5")
    else:
        bin = chat_id + 4
        thesymptoms[str(bin)] = update.message.text.lower()
        context.bot.send_message(chat_id=chat_id, text="Enter symptom 5")
    return SIXTH_STEP


def SetSymptom5(update, context):
    chat_id = update.effective_chat.id
    kit = chat_id + 6
    diction = {kit: update.message.text.lower()}
    txt = diction[kit]

    if " " in txt:
        result = re.sub(r"\s+", '_', txt)
        bin = chat_id + 5
        thesymptoms[str(bin)] = result
        with open("data.json", "w") as outfile:
            json.dump(thesymptoms, outfile)
        # open('problem5.txt', 'w').write(result.lower())
    else:
        bin = chat_id + 5
        thesymptoms[str(bin)] = update.message.text.lower()
        with open("data.json", "w") as outfile:
            json.dump(thesymptoms, outfile)
        # open('problem5.txt', 'w').write(update.message.text.lower())

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
                                 " please check your spelling and try again")
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




def main():
    updater = Updater(token=telegram_bot_token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(conv_handler)

    updater.start_webhook(listen="0.0.0.0",
                          port=int(os.environ.get('PORT', 5000)),
                          url_path=telegram_bot_token,
                          webhook_url="https://illness-detector-bot.herokuapp.com/" + telegram_bot_token
                          )
    updater.bot.setWebhook('https://illness-detector-bot.herokuapp.com/' + telegram_bot_token)

    updater.idle()


if __name__ == "__main__":
    main()
