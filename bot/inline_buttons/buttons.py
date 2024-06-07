from aiogram import types

greeteng_actions_list_kb = [
    [types.KeyboardButton(text='Начать прогнозирование')]
]

greeteng_actions_list = types.ReplyKeyboardMarkup(keyboard=greeteng_actions_list_kb, resize_keyboard=True)

main_menu_actions_list_kb = [
    [types.KeyboardButton(text='МСК'),
    types.KeyboardButton(text='Центр')],

    [types.KeyboardButton(text='СЗ'),
    types.KeyboardButton(text='НН')],

    [types.KeyboardButton(text='Юг'),
    types.KeyboardButton(text='Урал')],

    [types.KeyboardButton(text='Сиб'),
    types.KeyboardButton(text='ДВ')],

    [types.KeyboardButton(text='Главное меню')]
]

main_menu_actions_list = types.ReplyKeyboardMarkup(keyboard=main_menu_actions_list_kb, resize_keyboard=True)

return_actions_list_kb = [
    [types.KeyboardButton(text='Главное меню')]
]

return_actions_list = types.ReplyKeyboardMarkup(keyboard=return_actions_list_kb, resize_keyboard=True)

get_answers_list_kb = [
    [types.KeyboardButton(text='Объем, который необходимо зарезервировать для каждого месяца')],
    [types.KeyboardButton(text='График для получения')],
    [types.KeyboardButton(text='График для отправки')],
    [types.KeyboardButton(text='Главное меню')]
]

get_answers_list = types.ReplyKeyboardMarkup(keyboard=get_answers_list_kb, resize_keyboard=True)
