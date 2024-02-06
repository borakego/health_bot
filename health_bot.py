from random import seed, randrange
import time
import telebot
from telebot import types
import datetime

TOKEN = '6303505767:AAFiHZDMaTeCA0VdLgrOLXJyT4lr7fCJuIg'


bot = telebot.TeleBot(TOKEN) # инициализируем нашего бота

users_info = dict()

class Weight:
    def __init__(self, user_id, weight):
        self.user_id = user_id
        self.start_weight = weight
        self.cur_weight = self.start_weight
    
    def update_weight(self, new_weight):
        dif_weight =  new_weight - self.cur_weight
        self.cur_weight = new_weight
        return dif_weight

    def check_weight(self):
        return self.cur_weight

    def overall_dif(self):
        return self.cur_weight - self.start_weight

class Water:
    def __init__(self, user_id, volume):
        self.user_id = user_id
        self.volume = volume
    
    def update_volume(self, volume):
        self.volume += volume
        return self.volume

    def check_volume(self):
        return self.volume

class Menstruation:
    def __init__(self, user_id, cycle_start, cycle_duration=28):
        self.user_id = user_id
        self.cycle_start = cycle_start
        self.cycle_duration = cycle_duration

    def next_menstruation(self):
        today = datetime.datetime.today()
        today = datetime.date(today.year, today.month, today.day)
        next_cycle = self.cycle_start
        while next_cycle < today:
            next_cycle += datetime.timedelta(days=self.cycle_duration)
        return next_cycle
        


class Pregnancy:
    def __init__(self, user_id, pregnancy_start):
        self.user_id = user_id
        self.pregnancy_start = pregnancy_start

    def ultrasound(self):
        start = self.pregnancy_start + datetime.timedelta(days=7 * 7)
        end = start + datetime.timedelta(days=1 * 7)
        return [start, end]

    def screaning1(self):
        start = self.pregnancy_start + datetime.timedelta(days=11 * 7)
        end = start + datetime.timedelta(days=3 * 7)
        return [start, end]

    def screaning2(self):
        start = self.pregnancy_start + datetime.timedelta(days=18 * 7)
        end = start + datetime.timedelta(days=3 * 7)
        return [start, end]

    def screaning3(self):
        start = self.pregnancy_start + datetime.timedelta(days=32 * 7)
        end = start + datetime.timedelta(days=3 * 7)
        return [start, end]

    def birth(self):
        start = self.pregnancy_start + datetime.timedelta(days=38 * 7)
        end = start + datetime.timedelta(days=5 * 7)
        return [start, end]

item_1 = types.KeyboardButton("вес")
item_2 = types.KeyboardButton("вода")
item_3 = types.KeyboardButton("календарь беременности")
item_4 = types.KeyboardButton("календарь месячных")

@bot.message_handler(commands=['start'])
def hello_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(item_1, item_2, item_3, item_4)
    bot.send_message(message.chat.id, "Добро пожаловать!", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def message_reply(message):
    if message.text == "вес":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item_weight_start = types.KeyboardButton("начать отслеживать вес")
        item_weight_update = types.KeyboardButton("обновить вес")
        item_weight_check = types.KeyboardButton("посмотреть текущий вес")
        item_weight_overall = types.KeyboardButton("изменение веса за всё время")

        if message.from_user.id in users_info and 'weight' in users_info[message.from_user.id]:
            markup.add(item_weight_start, item_weight_update, item_weight_check, item_weight_overall)
        else:
            markup.add(item_weight_start)
        bot.send_message(message.chat.id, "Выберите опцию", reply_markup=markup)
            
                
    elif message.text == "вода":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item_water_start = types.KeyboardButton("начать отслеживать воду")
        item_water_update = types.KeyboardButton("добавить воду")
        item_water_check = types.KeyboardButton("текущий объём воды")

        if message.from_user.id in users_info and 'water' in users_info[message.from_user.id]:
            markup.add(item_water_start, item_water_update, item_water_check)
        else:
            markup.add(item_water_start)
        bot.send_message(message.chat.id, "Выберите опцию", reply_markup=markup)
    
    elif message.text == "календарь месячных":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item_menstruation_start = types.KeyboardButton("начать вести календарь месячных")
        item_menstruation_next_mens = types.KeyboardButton("следующая менструация")

        if message.from_user.id in users_info and 'menstruation' in users_info[message.from_user.id]:
            markup.add(item_menstruation_start, item_menstruation_next_mens)
        else:
            markup.add(item_menstruation_start)
        bot.send_message(message.chat.id, "Выберите опцию", reply_markup=markup)
    
    elif message.text == "календарь беременности":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item_pregnancy_start = types.KeyboardButton("начало беременности")
        item_pregnancy_ultrasound = types.KeyboardButton("УЗИ")
        item_pregnancy_screaning1 = types.KeyboardButton("первый скрининг")
        item_pregnancy_screaning2 = types.KeyboardButton("второй скрининг")
        item_pregnancy_screaning3 = types.KeyboardButton("третий скрининг")
        item_pregnancy_birth = types.KeyboardButton("роды")

        if message.from_user.id in users_info and 'pregnancy' in users_info[message.from_user.id]:
            markup.add(item_pregnancy_start, item_pregnancy_ultrasound, item_pregnancy_screaning1,
                       item_pregnancy_screaning2, item_pregnancy_screaning3, item_pregnancy_birth)
        else:
            markup.add(item_pregnancy_start)
        bot.send_message(message.chat.id, "Выберите опцию", reply_markup=markup)
        
    elif message.text == "начать отслеживать вес":
        send = bot.send_message(message.chat.id, "Введите свой текущий вес")
        bot.register_next_step_handler(send, waiting_for_start_weight)
        
    
    elif message.text == "обновить вес":
        send = bot.send_message(message.chat.id, "Введите свой текущий вес")
        send = bot.register_next_step_handler(send, waiting_for_update_weight)
        
        
    elif message.text == "посмотреть текущий вес":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(item_1, item_2, item_3, item_4)
        weight = users_info[message.from_user.id]['weight'].check_weight()
        bot.send_message(message.chat.id, f"Ваш вес: {weight}", reply_markup=markup)

    elif message.text == "изменение веса за всё время":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(item_1, item_2, item_3, item_4)
        dif_weight = users_info[message.from_user.id]['weight'].overall_dif()
        if dif_weight > 0:
            bot.send_message(message.chat.id, f"Ваш вес увеличился на {dif_weight}")
            
        elif dif_weight == 0:
            bot.send_message(message.chat.id, f"Ваш вес не изменился")
            
        else:
            dif_weight *= -1
            bot.send_message(message.chat.id, f"Ваш вес уменьшился на {dif_weight}")
        bot.send_message(message.chat.id, "Продолжим!", reply_markup=markup)
    
    elif message.text == "начать отслеживать воду":
        send = bot.send_message(message.chat.id, "Введите объём выпитой воды")
        bot.register_next_step_handler(send, waiting_for_start_water)

    elif message.text == "добавить воду":
        send = bot.send_message(message.chat.id, "Введите свой текущий вес")
        send = bot.register_next_step_handler(send, waiting_for_update_water)
    
    elif message.text == "текущий объём воды":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(item_1, item_2, item_3, item_4)
        water = users_info[message.from_user.id]['water'].check_volume()
        bot.send_message(message.chat.id, f"Общий объём: {water}", reply_markup=markup)

    elif message.text == "начать вести календарь месячных":
        send = bot.send_message(message.chat.id, "Введите дату начала цикла (format: YYYY MM DD)")
        bot.register_next_step_handler(send, waiting_for_start_menstruation1)

    elif message.text == "следующая менструация":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(item_1, item_2, item_3, item_4)
        menstruation = users_info[message.from_user.id]['menstruation'].next_menstruation()
        bot.send_message(message.chat.id, f"Следующая менструация: {menstruation}", reply_markup=markup)

    elif message.text == "начало беременности":
        send = bot.send_message(message.chat.id, "Введите первый день беременности (format: YYYY MM DD)")
        bot.register_next_step_handler(send, waiting_for_start_pregnancy)

    elif message.text == "УЗИ":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(item_1, item_2, item_3, item_4)
        pregnancy = users_info[message.from_user.id]['pregnancy'].ultrasound()
        bot.send_message(message.chat.id, f"На УЗИ стоит идти с {pregnancy[0]} по {pregnancy[1]}", reply_markup=markup)

    elif message.text == "первый скрининг":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(item_1, item_2, item_3, item_4)
        pregnancy = users_info[message.from_user.id]['pregnancy'].screaning1()
        bot.send_message(message.chat.id, f"На первый скрининг стоит идти с {pregnancy[0]} по {pregnancy[1]}", reply_markup=markup)

    elif message.text == "второй скрининг":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(item_1, item_2, item_3, item_4)
        pregnancy = users_info[message.from_user.id]['pregnancy'].screaning2()
        bot.send_message(message.chat.id, f"На второй скрининг стоит идти с {pregnancy[0]} по {pregnancy[1]}", reply_markup=markup)

    elif message.text == "третий скрининг":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(item_1, item_2, item_3, item_4)
        pregnancy = users_info[message.from_user.id]['pregnancy'].screaning3()
        bot.send_message(message.chat.id, f"На третий скрининг стоит идти с {pregnancy[0]} по {pregnancy[1]}", reply_markup=markup)

    elif message.text == "роды":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(item_1, item_2, item_3, item_4)
        pregnancy = users_info[message.from_user.id]['pregnancy'].birth()
        bot.send_message(message.chat.id, f"Скорее всего, роды пройдут в промежутке между {pregnancy[0]} и {pregnancy[1]}", reply_markup=markup)
        
        
        

def waiting_for_start_weight(message):
    bot.send_message(message.chat.id, "got it")
    weight = Weight(message.from_user.id, float(message.text))
    if message.from_user.id in users_info:
        users_info[message.from_user.id].update({'weight': weight})
    else:
        users_info.update({message.from_user.id: {'weight': weight}})
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(item_1, item_2, item_3, item_4)
    bot.send_message(message.chat.id, "Продолжим!", reply_markup=markup)

def waiting_for_update_weight(message):
    bot.send_message(message.chat.id, "got it")
    dif_weight = users_info[message.from_user.id]['weight'].update_weight(float(message.text))
    if dif_weight > 0:
        bot.send_message(message.chat.id, f"Ваш вес увеличился на {dif_weight}")
        
    elif dif_weight == 0:
        bot.send_message(message.chat.id, f"Ваш вес не изменился")
        
    else:
        dif_weight *= -1
        bot.send_message(message.chat.id, f"Ваш вес уменьшился на {dif_weight}")
    users_info[message.from_user.id].update({'weight': users_info[message.from_user.id]['weight']})
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(item_1, item_2, item_3, item_4)
    bot.send_message(message.chat.id, "Продолжим!", reply_markup=markup)

def waiting_for_start_water(message):
    bot.send_message(message.chat.id, "got it")
    water = Water(message.from_user.id, float(message.text))
    if message.from_user.id in users_info:
        users_info[message.from_user.id].update({'water': water})
    else:
        users_info.update({message.from_user.id: {'water': water}})
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(item_1, item_2, item_3, item_4)
    bot.send_message(message.chat.id, "Продолжим!", reply_markup=markup)

def waiting_for_update_water(message):
    bot.send_message(message.chat.id, "got it")
    volume = users_info[message.from_user.id]['water'].update_volume(float(message.text))
    bot.send_message(message.chat.id, f"Общий объём: {volume}")
    users_info[message.from_user.id].update({'water': users_info[message.from_user.id]['water']})
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(item_1, item_2, item_3, item_4)
    bot.send_message(message.chat.id, "Продолжим!", reply_markup=markup)
    
def waiting_for_start_menstruation1(message):
    bot.send_message(message.chat.id, "got it")
    t = message.text.split(" ")
    date = datetime.date(int(t[0]), int(t[1]), int(t[2]))
    menstruation = Menstruation(message.from_user.id, date)
    if message.from_user.id in users_info:
        users_info[message.from_user.id].update({'menstruation': menstruation})
    else:
        users_info.update({message.from_user.id: {'menstruation': menstruation}})
    send = bot.send_message(message.chat.id, "Введите длительность цикла (в среднем 28)")
    bot.register_next_step_handler(send, waiting_for_start_menstruation2)

def waiting_for_start_menstruation2(message):
    bot.send_message(message.chat.id, "got it")
    menstruation = users_info[message.from_user.id]['menstruation']
    menstruation.cycle_duration = int(message.text)
    send = bot.send_message(message.chat.id, "Введите длительность менструации (в среднем 5)")
    bot.register_next_step_handler(send, waiting_for_start_menstruation3)

def waiting_for_start_menstruation3(message):
    bot.send_message(message.chat.id, "got it")
    menstruation = users_info[message.from_user.id]['menstruation']
    menstruation.menstruation_duration = int(message.text)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(item_1, item_2, item_3, item_4)
    bot.send_message(message.chat.id, "Продолжим!", reply_markup=markup)

def waiting_for_start_pregnancy(message):
    bot.send_message(message.chat.id, "got it")
    t = message.text.split(" ")
    date = datetime.date(int(t[0]), int(t[1]), int(t[2]))
    pregnancy = Pregnancy(message.from_user.id, date)
    if message.from_user.id in users_info:
        users_info[message.from_user.id].update({'pregnancy': pregnancy})
    else:
        users_info.update({message.from_user.id: {'pregnancy': pregnancy}})
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(item_1, item_2, item_3, item_4)
    bot.send_message(message.chat.id, "Продолжим!", reply_markup=markup)


bot.polling(none_stop=True, interval=0) #запускаем нашего бота
