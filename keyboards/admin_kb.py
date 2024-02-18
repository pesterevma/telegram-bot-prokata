from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# формирование основной клавиатуры админа
b1 = KeyboardButton(text='Загрузить условия проката')
b2 = KeyboardButton(text='Загрузить прайс-лист Excel')
b3 = KeyboardButton(text='Загрузить прайс-лист PNG')
b4 = KeyboardButton(text='Выйти из меню администратора')

kb = [[b1], [b2], [b3], [b4]]

kb_admin = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

# формирование кнопки возврата в главное меню для админа
b5 = KeyboardButton(text='Вернуться в меню администратора')
kb_ret = [[b5]]

kb_admin_ret = ReplyKeyboardMarkup(keyboard=kb_ret, resize_keyboard=True)

# формирование клавиатуры менеджера
b1 = KeyboardButton(text='Отменить ввод')
kb = [[b1]]

kb_manager = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
