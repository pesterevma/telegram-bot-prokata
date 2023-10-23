from aiogram import types, Router, F
from aiogram.filters.command import Command
from aiogram.filters.text import Text
from create_bot import bot
from keyboards import kb_client, kb_client_ret
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder
from configurebot import cfg, docs
from pytz import timezone
# from aiogram.types import FSInputFile


class FSMclient(StatesGroup):
    question = State()


class FSMreq(StatesGroup):
    req = State()


router = Router()
group_id = cfg['group_id']


# обработка команд start и help
@router.message(Command('start', 'help'))
async def command_start(message: types.Message):
    await message.answer('''
<b>Здравствуйте!</b>
С помощью нашего бота вы можете ознакомиться с <b>прайс-листом</b> проката, <b>задать вопрос</b> и <b>отправить заявку</b> \
для бронирования снаряжения.
Ваша заявка будет принята нашим менеджером в рабочее время, и вы получите ответ в этот чат.
Часы работы и адрес проката вы можете узнать в разделе <b>контакты</b>.''',
                         reply_markup=kb_client, parse_mode='HTML')


# обработка инлайн кнопки "ответить" начало
@router.callback_query(Text(startswith="rс"))
async def send_manager_answer(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    user_id = callback.data.split('_')[0][2:]
    await state.update_data(user_id=user_id)
    number_q = callback.data.split('_')[1].rstrip()
    await state.update_data(number_q=number_q)
    await bot.send_message(chat_id=user_id,
                           text=f"Напишите ниже ваш ответ в продолжение вопроса/заявки\n<b>#{number_q}</b>:", parse_mode='HTML')
    await state.set_state(FSMreq.req)


# обработка инлайн кнопки "ответить" Отбраковка сообщений которые не являются текстовыми
@router.message(FSMreq.req, F.content_type != 'text')
async def book_step(message: types.Message, state: FSMContext):
    await message.answer('Отправьте ответ <b>текстовым сообщением</b>', parse_mode='HTML')


# обработка инлайн кнопки "ответить" продолжение
@router.message(FSMreq.req)
async def load_answer(message: types.Message, state: FSMContext):
    answer = message.text
    user_data = await state.get_data()
    await message.reply(f'✅ Ваш ответ успешно отправлен!', parse_mode='HTML')
    # создание инлайн клавиатуры
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Ответить",
                                           callback_data=f'ra{message.chat.id}_{user_data["number_q"]}'))
    builder.add(types.InlineKeyboardButton(text="Пригласить в ЛС",
                                           callback_data=f'ls{message.chat.id}_{user_data["number_q"]}'))

    await bot.send_message(chat_id=group_id, text=f"✉ | Дополнение к вопросу/заявке <b>#{user_data['number_q']}</b>:\n\
<b>{answer}</b>", parse_mode='HTML', reply_markup=builder.as_markup())
    # завершение машины состояний
    await state.clear()


@router.message(Text(text='Контакты', ignore_case=True))
async def command_contact(message: types.Message):
    await message.answer('''
<b>Адрес:</b> г. Екатеринбург ул. Кулибина, 1а
<b>Время работы:</b> Пн-Пт с 12:00 до 20:00
<b>Телефон:</b> +7(982)730-32-31
<b>E-mail:</b> prokat@manaraga.ru''', parse_mode='HTML')


# Обработка кнопки возврата в главное меню
@router.message(Text(text="Вернуться в главное меню", ignore_case=True))
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(text="Вы вернулись в главное меню", reply_markup=kb_client)


# Обработка кнопки задать вопрос, запускаем машину состояний
@router.message(Text(text='Задать вопрос', ignore_case=True))
async def command_question(message: types.Message, state: FSMContext):
    await message.answer(
        '''Отправьте ваш вопрос, наш менеджер пришлёт ответ в этот чат в рабочее время.''',
        reply_markup=kb_client_ret)
    await state.set_state(FSMclient.question)


# Отбраковка сообщений которые не являются текстовыми
@router.message(FSMclient.question, F.content_type != 'text')
async def load_question(message: types.Message, state: FSMContext):
    await message.answer('''Пожалуйста, сформулируйте ваш вопрос в виде текстового сообщения.''')


# Обработка кнопки задать вопрос, продолжение
@router.message(FSMclient.question)
async def load_question(message: types.Message, state: FSMContext):
    if (message.chat.username == None):
        who = f'Ник не установлен, ID: {message.chat.id}'
    else:
        who = f'@{message.chat.username}, ID: {message.chat.id}'
    date = message.date
    date_ekb = date.astimezone(timezone('Asia/Yekaterinburg'))
    formatted_date = date_ekb.strftime("%d%H%M%S")
    number_q = f'q{str(message.chat.id)[-3:]}{formatted_date}'
    question = message.text
    await message.reply(f'Ваш вопрос <b>#{number_q}</b> принят, ожидайте ответа.', parse_mode='HTML', reply_markup=kb_client)
    # создание инлайн клавиатуры
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Ответить на вопрос", callback_data=f'q{message.chat.id}'))
    builder.add(types.InlineKeyboardButton(text="Пригласить в ЛС", callback_data=f'ls{message.chat.id}_{number_q}'))

    await bot.send_message(chat_id=group_id, text=
                           f"✉ | Новый вопрос <b>#{number_q}</b>\nОт: {who}\nВопрос: <b>{question}</b>",
                           parse_mode='HTML', reply_markup=builder.as_markup())
    # завершение машины состояний
    await state.clear()


@router.message(Text(text='Условия проката', ignore_case=True))
async def command_rules(message: types.Message):
    await message.answer('Пожалуйста, ознакомьтесь с условиями проката.')
    await bot.send_document(chat_id=message.chat.id,
                            document=docs['rules'])


# ПОМОЖЕТ ПОЛУЧИТЬ АЙДИ ДОКУМЕНТА:
# @router.message(Command('get_doc_id'))
# async def get_doc_id(message: types.Message):
#     price_list = FSInputFile('files/Прокат_Прайс_лист_V15_1_.xlsx')  # подгружаем файл из моей директории
#     id_price_list = await bot.send_document(chat_id=message.chat.id, document=price_list)
#                                                                      # этот метод поможет получить file_id
#     id_p = id_price_list.document.file_id  # это сам file_id
#     await message.answer(f'Айди документа: {id_p}') # выводим file_id записываем его вручную, или потом автоматом
#                                                     # дальше файлы подгружаем через file_id


# ПОМОЖЕТ ПОЛУЧИТЬ АЙДИ ЧАТА:
# @router.message(Command('get_chat_id'))
# async def get_chat_id(message: types.Message):
#     await message.reply("Chat id = ")
#     chat_id = message.chat.id  # работает и для приватного(лс) чата и для общих чатов (групп)
#     await message.reply(str(chat_id))


# ПОМОЖЕТ ПОЛУЧИТЬ АЙДИ фото:
# @router.message(Command('get_photo_id'))
# async def get_photo_id(message: types.Message):
#     price_list = FSInputFile('files/price_png/png final/структура прайс-листа.PNG')  # подгружаем photo из моей директории
#     id_price_list = await bot.send_photo(chat_id=message.chat.id, photo=price_list)
#                                                                      # этот метод поможет получить photo_id
#     id_p = id_price_list.photo[-1].file_id  # это сам photo_id
#     await message.answer(f'Айди документа: {id_p}') # выводим photo_id записываем его вручную, или потом автоматом
#                                                     # дальше photo подгружаем через photo_id

