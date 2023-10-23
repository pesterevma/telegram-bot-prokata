from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# создание green клавиатуры
g_1 = InlineKeyboardButton(text='Туристическое снаряжение', callback_data='g_1_Туристическое снаряжение')
g_2 = InlineKeyboardButton(text='Лыжи и сноуборды', callback_data='g_2_Лыжи и сноуборды')
g_3 = InlineKeyboardButton(text='Скачать полный прайс-лист', callback_data='g_3_Скачать полный прайс-лист')

kb_g = [[g_1], [g_2], [g_3]]
inline_kb_g = InlineKeyboardMarkup(inline_keyboard=kb_g, resize_keyboard=True)


# создание blue клавиатуры
b_1 = InlineKeyboardButton(text='Палатки', callback_data='b_1_Палатки')
b_2 = InlineKeyboardButton(text='Тенты-шатры', callback_data='b_2_Тенты-шатры')
b_3 = InlineKeyboardButton(text='Тенты', callback_data='b_3_Тенты')
b_4 = InlineKeyboardButton(text='Рюкзаки', callback_data='b_4_Рюкзаки')
b_5 = InlineKeyboardButton(text='Групповое снаряжение', callback_data='b_5_Групповое снаряжение')
b_6 = InlineKeyboardButton(text='Коврики туристические', callback_data='b_6_Коврики туристические')
b_7 = InlineKeyboardButton(text='Спальники', callback_data='b_7_Спальники')
b_8 = InlineKeyboardButton(text='Водный туризм', callback_data='b_8_Водный туризм')
b_9 = InlineKeyboardButton(text='Горное снаряжение', callback_data='b_9_Горное снаряжение')
b_10 = InlineKeyboardButton(text='Кемпинговое снаряжение', callback_data='b_10_Кемпинговое снаряжение')
b_11 = InlineKeyboardButton(text='Прочее снаряжение', callback_data='b_11_Прочее снаряжение')
b_ret = InlineKeyboardButton(text='Вернуться назад', callback_data='ret_g_Вернуться назад')

kb_b = [[b_1, b_2], [b_3, b_4], [b_5, b_6], [b_7, b_8], [b_9, b_10], [b_11], [b_ret]]
inline_kb_b = InlineKeyboardMarkup(inline_keyboard=kb_b, resize_keyboard=True)


# создание yellow клавиатуры
y_1 = InlineKeyboardButton(text='Сноуборды', callback_data='y_1_Сноуборды')
y_2 = InlineKeyboardButton(text='Беговые и турист. лыжи', callback_data='y_2_Беговые и турист. лыжи')
y_3 = InlineKeyboardButton(text='Бублики', callback_data='y_3_Бублики')
y_4 = InlineKeyboardButton(text='Одежда', callback_data='y_4_Одежда')
y_ret = InlineKeyboardButton(text='Вернуться назад', callback_data='ret_g_Вернуться назад')

kb_y = [[y_1], [y_2], [y_3], [y_4], [y_ret]]
inline_kb_y = InlineKeyboardMarkup(inline_keyboard=kb_y, resize_keyboard=True)


# создание orange tent клавиатуры
ot_1 = InlineKeyboardButton(text='2-х местные', callback_data='ot_1_2-х местные')
ot_2 = InlineKeyboardButton(text='3-х местные', callback_data='ot_2_3-х местные')
ot_3 = InlineKeyboardButton(text='4-х местные', callback_data='ot_3_4-х местные')
ot_4 = InlineKeyboardButton(text='5-8 местные', callback_data='ot_4_5-8 местные')
ot_ret = InlineKeyboardButton(text='Вернуться назад', callback_data='ret_b_Вернуться назад')

kb_ot = [[ot_1], [ot_2], [ot_3], [ot_4], [ot_ret]]
inline_kb_ot = InlineKeyboardMarkup(inline_keyboard=kb_ot, resize_keyboard=True)


# создание orange bag клавиатуры
ob_1 = InlineKeyboardButton(text='Лето / осень', callback_data='ob_1_Лето / осень')
ob_2 = InlineKeyboardButton(text='Зима', callback_data='ob_2_Зима')
ob_ret = InlineKeyboardButton(text='Вернуться назад', callback_data='ret_b_Вернуться назад')

kb_ob = [[ob_1], [ob_2], [ob_ret]]
inline_kb_ob = InlineKeyboardMarkup(inline_keyboard=kb_ob, resize_keyboard=True)


# создание orange water клавиатуры
ow_1 = InlineKeyboardButton(text='Катамараны / байдарки', callback_data='ow_1_Катамараны / байдарки')
ow_2 = InlineKeyboardButton(text='SUP серфинг', callback_data='ow_2_SUP серфинг')
ow_3 = InlineKeyboardButton(text='Спасжилеты', callback_data='ow_3_Спасжилеты')
ow_4 = InlineKeyboardButton(text='Гермомешки', callback_data='ow_4_Гермомешки')
ow_ret = InlineKeyboardButton(text='Вернуться назад', callback_data='ret_b_Вернуться назад')

kb_ow = [[ow_1], [ow_2], [ow_3], [ow_4], [ow_ret]]
inline_kb_ow = InlineKeyboardMarkup(inline_keyboard=kb_ow, resize_keyboard=True)


# создание orange rock клавиатуры
or_1 = InlineKeyboardButton(text='Ледорубы', callback_data='or_1_Ледорубы')
or_2 = InlineKeyboardButton(text='Каски', callback_data='or_2_Каски')
or_3 = InlineKeyboardButton(text='Беседки', callback_data='or_3_Беседки')
or_4 = InlineKeyboardButton(text='Кошки', callback_data='or_4_Кошки')
or_5 = InlineKeyboardButton(text='Снегоступы', callback_data='or_5_Снегоступы')
or_6 = InlineKeyboardButton(text='Очки', callback_data='or_6_Очки')
or_7 = InlineKeyboardButton(text='Палки треккинговые', callback_data='or_7_Палки треккинговые')
or_8 = InlineKeyboardButton(text='Лавинное снаряжение', callback_data='or_8_Лавинное снаряжение')
or_9 = InlineKeyboardButton(text='Прочее железо', callback_data='or_9_Прочее железо')
or_ret = InlineKeyboardButton(text='Вернуться назад', callback_data='ret_b_Вернуться назад')

kb_or = [[or_1, or_2], [or_3, or_4], [or_5, or_6], [or_7], [or_8], [or_9], [or_ret]]
inline_kb_or = InlineKeyboardMarkup(inline_keyboard=kb_or, resize_keyboard=True)
