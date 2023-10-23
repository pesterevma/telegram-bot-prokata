from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# формирование основной клавиатуры клиента
b1 = KeyboardButton(text='Отправить заявку')
b2 = KeyboardButton(text='Прайс-лист')
b3 = KeyboardButton(text='Контакты')
b4 = KeyboardButton(text='Условия проката')
b5 = KeyboardButton(text='Задать вопрос')

kb = [[b1], [b2, b4], [b3, b5]]

kb_client = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

# формирование кнопки возврата в главное меню для клиента
b6 = KeyboardButton(text='Вернуться в главное меню')
kb_ret = [[b6]]

kb_client_ret = ReplyKeyboardMarkup(keyboard=kb_ret, resize_keyboard=True)

# формирование клавиатуры для шага 1 оформления заявки
b7 = KeyboardButton(text='Продолжить')
kb_b_1 = [[b7], [b6]]

kb_book_1 = ReplyKeyboardMarkup(keyboard=kb_b_1, resize_keyboard=True)

# формирование клавиатуры для шага 2 оформления заявки
b8 = KeyboardButton(text='Да')
b9 = KeyboardButton(text='Нет')
kb_b_2 = [[b8, b9], [b6]]

kb_book_2 = ReplyKeyboardMarkup(keyboard=kb_b_2, resize_keyboard=True)

# формирование клавиатуры для последнего шага оформления заявки
b10 = KeyboardButton(text='Отправить')
kb_b_3 = [[b10], [b6]]

kb_book_3 = ReplyKeyboardMarkup(keyboard=kb_b_3, resize_keyboard=True)

# формирование клавиатуры для выхода из прайс-листа
b11 = KeyboardButton(text='Закрыть прайс-лист')
kb_exit_price = [[b11]]

exit_price = ReplyKeyboardMarkup(keyboard=kb_exit_price, resize_keyboard=True)
