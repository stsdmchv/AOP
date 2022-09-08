# -*- coding: utf-8 -*-
# !usr/bin/env python3

import telebot
import constants
import requests
import logging
import time
from Models import TModel as TM

'''# pip install pyTelegramBotAPI'''
from telebot import apihelper
from telebot.types import Message
from telebot import types

bot = telebot.TeleBot(constants.TELEGRAM_TOKEN)


@bot.message_handler(func=lambda message: 'start' in message.text, content_types=['text'])
@bot.edited_message_handler(func=lambda message: 'start' in message.text, content_types=['text'])
def startC(message: Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('/start')
    keyboard.add(button)
    bot.send_message(message.chat.id, "Приветствую", reply_markup=keyboard)
    startKeyboard(message)


@bot.message_handler(func=lambda message: 'ping' in message.text, content_types=['text'])
@bot.edited_message_handler(func=lambda message: 'ping' in message.text, content_types=['text'])
def ping(message: Message):
    ip = requests.get('https://ramziv.com/ip').text
    bot.send_message(message.chat.id, ip)


@bot.message_handler(content_types=['text'])
@bot.edited_message_handler(content_types=['text'])
def question(message: Message):
    fd = ""
    try:
        f = open("phrases.txt")
        fd = f.read()
    except Exception as e:
        logging.exception(e)
    with open("phrases.txt", "w") as file:
        file.write(fd + "\n" + message.text)
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    button = types.InlineKeyboardButton(
        text='Искать', url=f'https://www.google.com/search?q={message.text}%20site:vsuet.ru')
    keyboard.add(button)
    bot.send_message(
        message.chat.id, "Привет! Не знаю о чем ты, но можно поискать на сайте!", reply_markup=keyboard)


def startKeyboard(message: Message):
    markup_start = types.InlineKeyboardMarkup(row_width=1)
    itembtn_1 = types.InlineKeyboardButton(text='Кем хочешь стать?',
                                           callback_data='start_wrk')
    itembtn_2 = types.InlineKeyboardButton(text='Какие ЕГЭ сдавал?',
                                           callback_data='start_ege')
    itembtn_3 = types.InlineKeyboardButton(text='Вопрос по направлению подготовки?',
                                           callback_data='start_napravlenie')
    itembtn_4 = types.InlineKeyboardButton(text='Как подать документы?',
                                           callback_data='start_documents')
    itembtn_5 = types.InlineKeyboardButton(text='Мне нужны даты!',
                                           callback_data='start_dates')
    markup_start.add(
        itembtn_1,
        itembtn_2,
        itembtn_3,
        itembtn_4,
        itembtn_5,
    )
    bot.send_message(
        message.chat.id, "\nКакой вопрос тебя интересует?", reply_markup=markup_start)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if ('.' in call.data):
        #imageSpeciality = TM.getImage(call.data)
        speciality = TM.getSpeciality(call.data)
        button = types.InlineKeyboardMarkup(row_width=1)
        urlbtn = types.InlineKeyboardButton(text='Посмотреть на сайте',
                                            url=TM.getUrl(call.data))
        button.add(urlbtn)
        """back = types.InlineKeyboardButton(text='Вернуться назад',
                                            callback_data='start')
        button.add(back)"""
        bot.send_photo(call.message.chat.id,
                       speciality, reply_markup=button)
    else:
        from collections import defaultdict
        selector = defaultdict(lambda: False,
                               {'start':             startKeyboard,
                                ###################################################
                                'start_wrk':         mWorkerFunction,
                                'wrk_it':            mWorkerITFunction,
                                'wrk_technolog':     mWorkerTechnologFunction,
                                'wrk_ekolog':        mWorkerEkologFunction,
                                'wrk_proiz_bez':     mWorkerBezopasnikFunction,
                                'wrk_econom':        mWorkerEconomistFunction,
                                'wrk_upravl':        mWorkerUpravaFunction,
                                'wrk_projector':     mWorkerProjectFunction,
                                'wrk_inji_meh':      mWorkerMIngeneerFunction,
                                'wrk_bio_ingener':   mWorkerBIngenerFunction,
                                'wrk_vet_expert':    mWorkerVetexpertFunction,
                                ###################################################
                                'start_ege':         mEgeFunction,
                                'physics':           mEgePhysics,
                                'CS':                mEgeComputerScience,
                                'chemical':          mEgeChemical,
                                'biology':           mEgeBiology,
                                'socialscience':     mEgeSocialscience,
                                ###################################################
                                'start_napravlenie': mNaprFunction,
                                'start_documents':   mDocumentsFunction,
                                'start_dates':       mDatesFunction,
                                })
        bot.edit_message_reply_markup(
            call.message.chat.id, call.message.message_id)
        selector[call.data](call.message)


def mWorkerFunction(message: Message):
    markup_start = types.InlineKeyboardMarkup(row_width=1)
    itembtn_1 = types.InlineKeyboardButton(text='ITшником',
                                           callback_data='wrk_it')
    itembtn_2 = types.InlineKeyboardButton(text='Инженером-технологом',
                                           callback_data='wrk_technolog')
    itembtn_3 = types.InlineKeyboardButton(text='Экологом',
                                           callback_data='wrk_ekolog')
    itembtn_4 = types.InlineKeyboardButton(text='Специалист по производственной безопасности',
                                           callback_data='wrk_proiz_bez')
    itembtn_5 = types.InlineKeyboardButton(text='Экономистом',
                                           callback_data='wrk_econom')
    itembtn_6 = types.InlineKeyboardButton(text='Управленцем',
                                           callback_data='wrk_upravl')
    itembtn_7 = types.InlineKeyboardButton(text='Проектировщиком',
                                           callback_data='wrk_projector')
    itembtn_8 = types.InlineKeyboardButton(text='Инженером-механиком',
                                           callback_data='wrk_inji_meh')
    itembtn_9 = types.InlineKeyboardButton(text='Биоинженером',
                                           callback_data='wrk_bio_ingener')
    itembtn_10 = types.InlineKeyboardButton(text='Ветеринарным экспертом',
                                            callback_data='wrk_vet_expert')
    itembtn_11 = types.InlineKeyboardButton(text='Вернуться назад',
                                            callback_data='start')
    markup_start.add(
        itembtn_1,
        itembtn_2,
        itembtn_3,
        itembtn_4,
        itembtn_5,
        itembtn_6,
        itembtn_7,
        itembtn_8,
        itembtn_9,
        itembtn_10,
        itembtn_11
    )
    bot.send_message(message.chat.id, "Выбери профессию:",
                     reply_markup=markup_start)


def mWorkerITFunction(message: Message):
    # 09.03.02 09.03.03 10.05.03 15.03.04 27.03.04 43.03.01
    # TODO: Сделать выдачу пдфки со всеми описаниями
    markup_start = types.InlineKeyboardMarkup(row_width=1)
    itembtn_1 = types.InlineKeyboardButton(text='Информационные системы и технологии',
                                           callback_data='09.03.02')
    itembtn_2 = types.InlineKeyboardButton(text='Прикладная информатика',
                                           callback_data='09.03.03')
    itembtn_3 = types.InlineKeyboardButton(text='Информационная безопасность автоматизированных систем',
                                           callback_data='10.05.03')
    itembtn_4 = types.InlineKeyboardButton(text='Автоматизация технологических процессов и производств',
                                           callback_data='15.03.04')
    itembtn_5 = types.InlineKeyboardButton(text='Управление в технических системах',
                                           callback_data='27.03.04')
    itembtn_6 = types.InlineKeyboardButton(text='Сервис',
                                           callback_data='43.03.01')
    itembtn_99 = types.InlineKeyboardButton(text='Вернуться назад',
                                            callback_data='start')
    markup_start.add(
        itembtn_1,
        itembtn_2,
        itembtn_3,
        itembtn_4,
        itembtn_5,
        itembtn_6,
        itembtn_99,
    )
    bot.send_message(message.chat.id, "Выбери специальность:",
                     reply_markup=markup_start)


def mWorkerTechnologFunction(message: Message):
    # 19.03.01 19.03.02 19.03.03 27.03.01 27.03.02 19.03.04 18.03.01 18.03.02 18.05.02-false 04.05.02
    markup_start = types.InlineKeyboardMarkup(row_width=1)
    itembtn_1 = types.InlineKeyboardButton(text='Фундаментальная и прикладная химия',
                                           callback_data='04.05.01')
    itembtn_2 = types.InlineKeyboardButton(text='Химическая технология',
                                           callback_data='18.03.01')
    itembtn_3 = types.InlineKeyboardButton(text='Энерго- и ресурсосберегающие процессы в химической технологии, нефтехимии и биотехнологии',
                                           callback_data='18.03.02')
    itembtn_4 = types.InlineKeyboardButton(text='Химическая технология материалов современной энергетики',
                                           callback_data='18.05.02')
    itembtn_5 = types.InlineKeyboardButton(text='Биотехнология',
                                           callback_data='19.03.01')
    itembtn_6 = types.InlineKeyboardButton(text='Продукты питания из растительного сырья',
                                           callback_data='19.03.02')
    itembtn_7 = types.InlineKeyboardButton(text='Продукты питания животного происхождения',
                                           callback_data='19.03.03')
    itembtn_8 = types.InlineKeyboardButton(text='Технология продукции и организация общественного питания',
                                           callback_data='19.03.04')
    itembtn_9 = types.InlineKeyboardButton(text='Стандартизация и метрология ',
                                           callback_data='27.03.01')
    itembtn_10 = types.InlineKeyboardButton(text='Управление качеством',
                                            callback_data='27.03.02')
    itembtn_99 = types.InlineKeyboardButton(text='Вернуться назад',
                                            callback_data='start')
    markup_start.add(
        itembtn_1,
        itembtn_2,
        itembtn_3,
        itembtn_4,
        itembtn_5,
        itembtn_6,
        itembtn_7,
        itembtn_8,
        itembtn_9,
        itembtn_10,
        itembtn_99
    )
    bot.send_message(message.chat.id, "Выбери специальность:",
                     reply_markup=markup_start)


def mWorkerEkologFunction(message: Message):
    # 18.03.02 18.05.02-false
    markup_start = types.InlineKeyboardMarkup(row_width=1)
    itembtn_1 = types.InlineKeyboardButton(text='Энерго- и ресурсосберегающие процессы в химической технологии, нефтехимии и биотехнологии',
                                           callback_data='18.03.02')
    itembtn_2 = types.InlineKeyboardButton(text='Химическая технология материалов современной энергетики',
                                           callback_data='18.05.02')
    itembtn_99 = types.InlineKeyboardButton(text='Вернуться назад',
                                            callback_data='start')
    markup_start.add(
        itembtn_1,
        itembtn_2,
        itembtn_99,
    )
    bot.send_message(message.chat.id, "Выбери специальность:",
                     reply_markup=markup_start)


def mWorkerBezopasnikFunction(message: Message):
    # 20.03.01
    markup_start = types.InlineKeyboardMarkup(row_width=1)
    itembtn_1 = types.InlineKeyboardButton(text='Техносферная безопасность',
                                           callback_data='20.03.01')
    itembtn_99 = types.InlineKeyboardButton(text='Вернуться назад',
                                            callback_data='start')
    markup_start.add(
        itembtn_1,
        itembtn_99,
    )
    bot.send_message(message.chat.id, "Выбери специальность:",
                     reply_markup=markup_start)


def mWorkerEconomistFunction(message: Message):
    # 38.05.01 38.03.01
    markup_start = types.InlineKeyboardMarkup(row_width=1)
    itembtn_1 = types.InlineKeyboardButton(text='Экономика',
                                           callback_data='38.03.01')
    itembtn_2 = types.InlineKeyboardButton(text='Экономическая безопасность',
                                           callback_data='38.05.01')
    itembtn_99 = types.InlineKeyboardButton(text='Вернуться назад',
                                            callback_data='start')
    markup_start.add(
        itembtn_1,
        itembtn_2,
        itembtn_99,
    )
    bot.send_message(message.chat.id, "Выбери специальность:",
                     reply_markup=markup_start)


def mWorkerUpravaFunction(message: Message):
    # 38.03.02 43.03.03 38.03.03 43.03.02
    markup_start = types.InlineKeyboardMarkup(row_width=1)
    itembtn_1 = types.InlineKeyboardButton(text='Менеджмент',
                                            callback_data='38.03.02')
    itembtn_2 = types.InlineKeyboardButton(text='Управление персоналом',
                                            callback_data='38.03.03')
    itembtn_3 = types.InlineKeyboardButton(text='Туризм',
                                            callback_data='43.03.02')
    itembtn_4 = types.InlineKeyboardButton(text='Гостиничное дело',
                                            callback_data='43.03.03')
    itembtn_99 = types.InlineKeyboardButton(text='Вернуться назад',
                                            callback_data='start')
    markup_start.add(
        itembtn_1,
        itembtn_2,
        itembtn_3,
        itembtn_4,
        itembtn_99
    )
    bot.send_message(message.chat.id, "Выбери специальность:",
                     reply_markup=markup_start)


def mWorkerProjectFunction(message: Message):
    # 15.05.01 15.03.03 13.03.01 18.03.02
    markup_start = types.InlineKeyboardMarkup(row_width=1)
    itembtn_1 = types.InlineKeyboardButton(text='Теплоэнергетика и теплотехника',
                                           callback_data='13.03.01')
    itembtn_2 = types.InlineKeyboardButton(text='Прикладная механика',
                                           callback_data='15.03.03')
    itembtn_3 = types.InlineKeyboardButton(text='Проектирование технологических машин и комплексов',
                                           callback_data='15.05.01')
    itembtn_4 = types.InlineKeyboardButton(text='Энерго- и ресурсосберегающие процессы в химической технологии, нефтехимии и биотехнологии',
                                           callback_data='18.03.02')
    itembtn_99 = types.InlineKeyboardButton(text='Вернуться назад',
                                            callback_data='start')
    markup_start.add(
        itembtn_1,
        itembtn_2,
        itembtn_3,
        itembtn_4,
        itembtn_99
    )
    bot.send_message(message.chat.id, "Выбери специальность:",
                     reply_markup=markup_start)


def mWorkerMIngeneerFunction(message: Message):
    # 15.03.02 15.03.03 16.03.03 18.03.02
    markup_start = types.InlineKeyboardMarkup(row_width=1)
    itembtn_1 = types.InlineKeyboardButton(text='Технологические машины и оборудование',
                                           callback_data='15.03.02')
    itembtn_2 = types.InlineKeyboardButton(text='Прикладная механика',
                                           callback_data='15.03.03')
    itembtn_3 = types.InlineKeyboardButton(text='Технологические машины и оборудование',
                                           callback_data='16.03.03')
    itembtn_4 = types.InlineKeyboardButton(text='Энерго- и ресурсосберегающие процессы в химической технологии, нефтехимии и биотехнологии',
                                           callback_data='18.03.02')
    itembtn_2 = types.InlineKeyboardButton(text='Химическая технология материалов современной энергетики',
                                           callback_data='18.05.02')
    itembtn_99 = types.InlineKeyboardButton(text='Вернуться назад',
                                            callback_data='start')
    markup_start.add(
        itembtn_1,
        itembtn_2,
        itembtn_3,
        itembtn_4,
        itembtn_99
    )
    bot.send_message(message.chat.id, "Выбери специальность:",
                     reply_markup=markup_start)


def mWorkerBIngenerFunction(message: Message):
    # 36.03.01 35.03.08
    markup_start = types.InlineKeyboardMarkup(row_width=1)
    itembtn_1 = types.InlineKeyboardButton(text='Водные биоресурсы и аквакультура',
                                           callback_data='35.03.08')
    itembtn_2 = types.InlineKeyboardButton(text='Ветеринарно-санитарная экспертиза',
                                           callback_data='36.03.01')
    itembtn_99 = types.InlineKeyboardButton(text='Вернуться назад',
                                            callback_data='start')
    markup_start.add(
        itembtn_1,
        itembtn_2,
        itembtn_99
    )
    bot.send_message(message.chat.id, "Выбери специальность:",
                     reply_markup=markup_start)


def mWorkerVetexpertFunction(message: Message):
    # 06.05.01
    markup_start = types.InlineKeyboardMarkup(row_width=1)
    itembtn_1 = types.InlineKeyboardButton(text='Биоинженерия и биоинформатика',
                                           callback_data='06.05.01')
    itembtn_99 = types.InlineKeyboardButton(text='Вернуться назад',
                                            callback_data='start')
    markup_start.add(
        itembtn_1,
        itembtn_99
    )
    bot.send_message(message.chat.id, "Выбери специальность:",
                     reply_markup=markup_start)

###################################################################################################


def mEgeFunction(message: Message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    itembtn_1 = types.InlineKeyboardButton(text='Физика',
                                           callback_data='physics')
    itembtn_2 = types.InlineKeyboardButton(text='Информатика',
                                           callback_data='CS')
    itembtn_3 = types.InlineKeyboardButton(text='Химия',
                                           callback_data='chemical')
    itembtn_4 = types.InlineKeyboardButton(text='Биология',
                                           callback_data='biology')
    itembtn_5 = types.InlineKeyboardButton(text='Обществознание',
                                           callback_data='socialscience')
    itembtn_99 = types.InlineKeyboardButton(text='Вернуться назад',
                                            callback_data='start')
    keyboard.add(
        itembtn_1,
        itembtn_2,
        itembtn_3,
        itembtn_4,
        itembtn_5,
        itembtn_99
    )
    bot.send_message(message.chat.id, "Выбери предмет:",
                     reply_markup=keyboard)


def mEgePhysics(message: Message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    itembtn_1 = types.InlineKeyboardButton(text='Информационные системы и технологии',
                                           callback_data='09.03.02')
    itembtn_2 = types.InlineKeyboardButton(text='Теплоэнергетика и теплотехника',
                                           callback_data='13.03.01')
    itembtn_3 = types.InlineKeyboardButton(text='Прикладная механика',
                                           callback_data='15.03.03')
    itembtn_4 = types.InlineKeyboardButton(text='Автоматизация технологических процессов и производств',
                                           callback_data='15.03.04')
    itembtn_5 = types.InlineKeyboardButton(text='Проектирование технологических машин и комплексов',
                                           callback_data='15.05.01')
    itembtn_6 = types.InlineKeyboardButton(text='Стандартизация и метрология ',
                                           callback_data='27.03.01')
    itembtn_7 = types.InlineKeyboardButton(text='Управление качеством',
                                           callback_data='27.03.02')
    itembtn_8 = types.InlineKeyboardButton(text='Управление в технических системах',
                                           callback_data='27.03.04')
    itembtn_99 = types.InlineKeyboardButton(text='Вернуться назад',
                                            callback_data='start')
    keyboard.add(
        itembtn_1,
        itembtn_2,
        itembtn_3,
        itembtn_4,
        itembtn_5,
        itembtn_6,
        itembtn_7,
        itembtn_8,
        itembtn_99
    )
    bot.send_message(message.chat.id, "Выбери направление:",
                     reply_markup=keyboard)


def mEgeComputerScience(message: Message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    itembtn_1 = types.InlineKeyboardButton(text='Прикладная информатика',
                                           callback_data='09.03.03')
    itembtn_2 = types.InlineKeyboardButton(text='Информационная безопасность автоматизированных систем',
                                           callback_data='10.05.03')
    itembtn_99 = types.InlineKeyboardButton(text='Вернуться назад',
                                            callback_data='start')
    keyboard.add(
        itembtn_1,
        itembtn_2,
        itembtn_99
    )
    bot.send_message(message.chat.id, "Выбери направление:",
                     reply_markup=keyboard)


def mEgeChemical(message: Message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    itembtn_1 = types.InlineKeyboardButton(text='Фундаментальная и прикладная химия',
                                           callback_data='04.05.01')
    itembtn_2 = types.InlineKeyboardButton(text='Химическая технология',
                                           callback_data='18.03.01')
    itembtn_3 = types.InlineKeyboardButton(text='Энерго- и ресурсосберегающие процессы в химической технологии, нефтехимии и биотехнологии',
                                           callback_data='18.03.02')
    itembtn_4 = types.InlineKeyboardButton(text='Химическая технология материалов современной энергетики',
                                           callback_data='18.05.02')
    itembtn_5 = types.InlineKeyboardButton(text='Биотехнология',
                                           callback_data='19.03.01')
    itembtn_6 = types.InlineKeyboardButton(text='Продукты питания из растительного сырья',
                                           callback_data='19.03.02')
    itembtn_7 = types.InlineKeyboardButton(text='Продукты питания животного происхождения',
                                           callback_data='19.03.03')
    itembtn_8 = types.InlineKeyboardButton(text='Технология продукции и организация общественного питания',
                                           callback_data='19.03.04')
    itembtn_9 = types.InlineKeyboardButton(text='Техносферная безопасность',
                                           callback_data='20.03.01')
    itembtn_99 = types.InlineKeyboardButton(text='Вернуться назад',
                                            callback_data='start')
    keyboard.add(
        itembtn_1,
        itembtn_2,
        itembtn_3,
        itembtn_4,
        itembtn_5,
        itembtn_6,
        itembtn_7,
        itembtn_8,
        itembtn_9,
        itembtn_99
    )
    bot.send_message(message.chat.id, "Выбери направление:",
                     reply_markup=keyboard)


def mEgeBiology(message: Message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    itembtn_1 = types.InlineKeyboardButton(text='Биоинженерия и биоинформатика',
                                           callback_data='06.05.01')
    itembtn_2 = types.InlineKeyboardButton(text='Водные биоресурсы и аквакультура',
                                           callback_data='35.03.08')
    itembtn_3 = types.InlineKeyboardButton(text='Ветеринарно-санитарная экспертиза',
                                           callback_data='36.03.01')
    itembtn_99 = types.InlineKeyboardButton(text='Вернуться назад',
                                            callback_data='start')
    keyboard.add(
        itembtn_1,
        itembtn_2,
        itembtn_3,
        itembtn_99
    )
    bot.send_message(message.chat.id, "Выбери направление:",
                     reply_markup=keyboard)


def mEgeSocialscience(message: Message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    itembtn_1 = types.InlineKeyboardButton(text='Экономика',
                                           callback_data='38.03.01')
    itembtn_2 = types.InlineKeyboardButton(text='Менеджмент',
                                           callback_data='38.03.02')
    itembtn_3 = types.InlineKeyboardButton(text='Экономическая безопасность',
                                           callback_data='38.05.01')
    itembtn_4 = types.InlineKeyboardButton(text='Сервис',
                                           callback_data='43.03.01')
    itembtn_5 = types.InlineKeyboardButton(text='Гостиничное дело',
                                           callback_data='43.03.03')
    itembtn_99 = types.InlineKeyboardButton(text='Вернуться назад',
                                            callback_data='start')
    keyboard.add(
        itembtn_1,
        itembtn_2,
        itembtn_3,
        itembtn_4,
        itembtn_5,
        itembtn_99
    )
    bot.send_message(message.chat.id, "Выбери направление:",
                     reply_markup=keyboard)


# TODO
def mNaprFunction(message: Message):
    napravleniya = (
        ('15.03.04', 'Автоматизация технологических процессов и производств'),
        ('06.05.01', 'Биоинженерия и биоинформатика'),
        ('19.03.01', 'Биотехнология'),
        ('36.03.01', 'Ветеринарно-санитарная экспертиза'),
        ('35.03.08', 'Водные биоресурсы и аквакультура'),
        ('43.03.03', 'Гостиничное дело'),
        ('10.05.03', 'Информационная безопасность автоматизированных систем'),
        ('09.03.02', 'Информационные системы и технологии'),
        ('38.03.02', 'Менеджмент'),
        ('09.03.03', 'Прикладная информатика'),
        ('15.03.03', 'Прикладная механика'),
        ('19.03.03', 'Продукты питания животного происхождения'),
        ('19.03.02', 'Продукты питания из растительного сырья'),
        ('15.05.01', 'Проектирование технологических машин и комплексов'),
        ('43.03.01', 'Сервис'),
        ('27.03.01', 'Стандартизация и метрология '),
        ('13.03.01', 'Теплоэнергетика и теплотехника'),
        ('15.03.02', 'Технологические машины и оборудование'),
        ('16.03.03', 'Технологические машины и оборудование'),
        ('19.03.04', 'Технология продукции и организация общественного питания'),
        ('20.03.01', 'Техносферная безопасность'),
        ('27.03.04', 'Управление в технических системах'),
        ('27.03.02', 'Управление качеством'),
        ('04.05.01', 'Фундаментальная и прикладная химия'),
        ('18.03.01', 'Химическая технология'),
        ('18.05.02', 'Химическая технология материалов современной энергетики'),
        ('38.03.01', 'Экономика'),
        ('38.05.01', 'Экономическая безопасность'),
        ('18.03.02', 'Энерго- и ресурсосберегающие процессы в химической технологии, нефтехимии и биотехнологии'),
    )
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    iterator = 1
    for item in napravleniya:
        s, n = item
        itembtn = types.InlineKeyboardButton(text=f'{n}',
                                             callback_data=f'{s}')
        keyboard.add(itembtn)
    itembtn_99 = types.InlineKeyboardButton(text='Вернуться назад',
                                            callback_data='start')
    keyboard.add(itembtn_99)
    bot.send_message(message.chat.id, "Выбери направление:",
                     reply_markup=keyboard)


# TODO
def mDocumentsFunction(message: Message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    itembtn_99 = types.InlineKeyboardButton(text='Вернуться назад',
                                            callback_data='start')
    keyboard.add(itembtn_99)
    bot.send_document(
        message.chat.id,
        TM.getInstruction(),
        caption="Инструкция по подаче документов",
        reply_markup=keyboard)


# TODO
def mDatesFunction(message: Message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    itembtn_99 = types.InlineKeyboardButton(text='Вернуться назад',
                                            callback_data='start')
    keyboard.add(itembtn_99)
    bot.send_document(
        message.chat.id,
        TM.getDates(1),
        caption="Расписание экзаменов в 2020 году",)
    bot.send_document(
        message.chat.id,
        TM.getDates(0),
        caption="Сроки приема документов в 2020 году",
        reply_markup=keyboard)


'''bot.polling(timeout=60)'''

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.exception(e)
        time.sleep(1)