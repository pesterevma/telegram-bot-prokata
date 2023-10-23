from aiogram import types
from create_bot import bot
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from configurebot import cfg
from aiogram.filters import Text
from keyboards import kb_admin, kb_admin_ret, kb_client
import json
from aiogram.utils.keyboard import InlineKeyboardBuilder


class FSMadmin(StatesGroup):
    answer = State()
    answer_book = State()
    ld_rules = State()
    ld_price = State()
    ld_price_png = State()
    ld_price_png2 = State()


class FSMreqa(StatesGroup):
    reqa = State()


router = Router()
group_id = cfg['group_id']
adm_id = cfg['adm_id']
mng_id = cfg['mng_id']


# запуск админской клавиатуры
@router.message((F.text == '/admin') & (F.from_user.id.in_(adm_id)))
async def admin_kb(message: types.Message):
    await message.answer('↓ Вам доступно меню администратора ↓', reply_markup=kb_admin)


# Обработка кнопки возврата в главное меню
@router.message((F.text == 'Вернуться в меню администратора') & (F.from_user.id.in_(adm_id)))
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer('↓ Вам доступно меню администратора ↓', reply_markup=kb_admin)


# Обработка кнопки выхода из админки
@router.message((F.text == 'Выйти из меню администратора') & (F.from_user.id.in_(adm_id)))
async def cmd_cancel(message: types.Message):
    await message.answer('Вы вернулись в меню для клиентов', reply_markup=kb_client)


# загрузка условий проката
@router.message((F.text == 'Загрузить условия проката') & (F.from_user.id.in_(adm_id)))
async def load_rules(message: types.Message, state: FSMContext):
    await message.answer('Отправьте в чат обновленный файл условий проката', reply_markup=kb_admin_ret)
    await state.set_state(FSMadmin.ld_rules)


# загрузка условий проката продолжение
@router.message(FSMadmin.ld_rules)
async def load_rules(message: types.Message, state: FSMContext):
    if message.document:
        id_rules = message.document.file_id
        with open('docs.json', 'r', encoding='utf-8') as file:
            docs = json.load(file)
        with open('docs.json', 'w', encoding='utf-8') as file:
            docs['rules'] = str(id_rules)
            json.dump(docs, file)
        await message.answer(f'Файл успешно обновлен, изменения вступят в силу \
после перезапуска бота вручную через "bot_run.bat"', reply_markup=kb_admin)
        await state.clear()
    else:
        await message.answer('Необходимо отправить документ, попробуйте снова')


# загрузка прайс-листа Excel
@router.message((F.text == 'Загрузить прайс-лист Excel') & (F.from_user.id.in_(adm_id)))
async def load_rules(message: types.Message, state: FSMContext):
    await message.answer('Отправьте в чат обновленный файл прайс-листа', reply_markup=kb_admin_ret)
    await state.set_state(FSMadmin.ld_price)


# загрузка прайс-листа Excel продолжение
@router.message(FSMadmin.ld_price)
async def load_rules(message: types.Message, state: FSMContext):
    if message.document:
        id_price = message.document.file_id
        with open('docs.json', 'r', encoding='utf-8') as file:
            docs = json.load(file)
        with open('docs.json', 'w', encoding='utf-8') as file:
            docs['price'] = str(id_price)
            json.dump(docs, file)
        await message.answer(f'Файл успешно обновлен, изменения вступят в силу \
после перезапуска бота вручную через "bot_run.bat"', reply_markup=kb_admin)
        await state.clear()
    else:
        await message.answer('Необходимо отправить документ, попробуйте снова')


# загрузка прайс-листа PNG
@router.message((F.text == 'Загрузить прайс-лист PNG') & (F.from_user.id.in_(adm_id)))
async def load_png(message: types.Message, state: FSMContext):
    admin_id = message.chat.id
    with open('photo.json', 'r', encoding='utf-8') as file:
        photo = json.load(file)
    await state.update_data(admin_id=admin_id)
    await bot.send_photo(chat_id=admin_id, photo=photo['Структура прайс-листа'], caption='Структура прайс-листа')
    await message.answer('Введите номер картинки которую хотите заменить (от 0 до 29):', reply_markup=kb_admin_ret)
    await state.set_state(FSMadmin.ld_price_png)


# загрузка прайс-листа PNG продолжение
@router.message(FSMadmin.ld_price_png)
async def load_png(message: types.Message, state: FSMContext):
    with open('photo.json', 'r', encoding='utf-8') as file:
        photo = json.load(file)
        title = list(photo.keys())
    try:
        if int(message.text) in range(30):
            name = title[int(message.text)]
            await state.update_data(name=name)
            await message.answer(f'Отправьте картинку "{name}":')
            await state.set_state(FSMadmin.ld_price_png2)
        else:
            await message.answer('Необходимо ввести номер от 0 до 29')
    except:
        await message.answer('Необходимо ввести номер от 0 до 29')


# загрузка прайс-листа PNG продолжение2
@router.message(FSMadmin.ld_price_png2)
async def load_png(message: types.Message, state: FSMContext):
    if message.photo:
        id_photo = message.photo[-1].file_id
        user_data = await state.get_data()
        name = user_data['name']
        with open('photo.json', 'r', encoding='utf-8') as file:
            photo = json.load(file)
        with open('photo.json', 'w', encoding='utf-8') as file:
            photo[name] = str(id_photo)
            json.dump(photo, file)
        await message.answer(f'Картинка успешно обновлена, изменения вступят в силу \
после перезапуска бота вручную через "bot_run.bat"', reply_markup=kb_admin)
        await state.clear()
    else:
        await message.answer('Необходимо отправить картинку, попробуйте снова')


# обработка инлайн кнопки "ответить на вопрос" начало
@router.callback_query(Text(startswith="q"))
async def send_manager_answer(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    user_id = callback.data[1:]
    await state.update_data(user_id=user_id)
    number_q = callback.message.text.split('#')[1][:12]
    await state.update_data(number_q=number_q)
    await bot.send_message(chat_id=group_id,
                           text=f"Напишите ниже ответ на вопрос\n<b>#{number_q}</b>:\n\
<b>{callback.message.text.split('Вопрос: ')[1]}</b>", parse_mode='HTML')
    await state.set_state(FSMadmin.answer)


# Обработка сообщений с фото
@router.message(FSMadmin.answer, F.content_type == 'photo')
async def load_answer(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    caption = message.caption
    user_data = await state.get_data()
    await message.reply(f'✅ Вы успешно ответили на вопрос <b>#{user_data["number_q"]}</b>!', parse_mode='HTML')
    # создание инлайн кнопки
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Ответить",
        callback_data=f'rс{user_data["user_id"]}_{user_data["number_q"]}'))
    if caption == None:
        caption = 'Смотрите прикрепленную фотографию.'
    await bot.send_message(chat_id=user_data['user_id'], text=f'✉ Новое уведомление!\n\
Ответ на ваш вопрос <b>#{user_data["number_q"]}</b> от менеджера проката:\n<b>{caption}</b>',
                           parse_mode='HTML', reply_markup=builder.as_markup())
    await bot.send_photo(chat_id=user_data['user_id'], photo=photo)
    await state.clear()


# Обработка сообщений с документом
@router.message(FSMadmin.answer, F.content_type == 'document')
async def load_answer(message: types.Message, state: FSMContext):
    document = message.document.file_id
    caption = message.caption
    user_data = await state.get_data()
    await message.reply(f'✅ Вы успешно ответили на вопрос <b>#{user_data["number_q"]}</b>!', parse_mode='HTML')
    # создание инлайн кнопки
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Ответить",
        callback_data=f'rс{user_data["user_id"]}_{user_data["number_q"]}'))
    if caption == None:
        caption = 'Смотрите прикрепленный документ.'
    await bot.send_message(chat_id=user_data['user_id'], text=f'✉ Новое уведомление!\n\
Ответ на ваш вопрос <b>#{user_data["number_q"]}</b> от менеджера проката:\n<b>{caption}</b>',
                           parse_mode='HTML', reply_markup=builder.as_markup())
    await bot.send_document(chat_id=user_data['user_id'], document=document)
    await state.clear()


# Отбраковка сообщений которые не являются текстом/фото/документом
@router.message(FSMadmin.answer, F.content_type != 'text')
async def book_step(message: types.Message, state: FSMContext):
    await message.answer('Отправьте ответ <b>текстовым сообщением, картинкой или документом</b>', parse_mode='HTML')


# обработка инлайн кнопки "ответить на вопрос" продолжение
@router.message(FSMadmin.answer)
async def load_answer(message: types.Message, state: FSMContext):
    answer = message.text
    user_data = await state.get_data()
    await message.reply(f'✅ Вы успешно ответили на вопрос <b>#{user_data["number_q"]}</b>!', parse_mode='HTML')
    # создание инлайн кнопки
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Ответить",
        callback_data=f'rс{user_data["user_id"]}_{user_data["number_q"]}'))

    await bot.send_message(chat_id=user_data['user_id'], text=f'✉ Новое уведомление!\n\
Ответ на ваш вопрос <b>#{user_data["number_q"]}</b> от менеджера проката:\n<b>{answer}</b>',
                           parse_mode='HTML', reply_markup=builder.as_markup())
    await state.clear()


# обработка инлайн кнопки "ответить на заявку" начало
@router.callback_query(Text(startswith="b"))
async def send_manager_answer(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    user_id = callback.data[1:]
    await state.update_data(user_id=user_id)
    number_b = callback.message.text.split('#')[1][:12]
    await state.update_data(number_b=number_b)
    await bot.send_message(chat_id=group_id,
                           text=f"Напишите ниже ответ на заявку <b>#{number_b}</b>:\nID:\
{callback.message.text.split('ID:')[1]}", parse_mode='HTML')
    await state.set_state(FSMadmin.answer_book)


# Обработка сообщений с фото
@router.message(FSMadmin.answer_book, F.content_type == 'photo')
async def load_answer(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    caption = message.caption
    user_data = await state.get_data()
    await message.reply(f'✅ Вы успешно ответили на заявку <b>#{user_data["number_b"]}</b>!', parse_mode='HTML')
    # создание инлайн кнопки
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Ответить",
        callback_data=f'rс{user_data["user_id"]}_{user_data["number_b"]}'))
    if caption == None:
        caption = 'Смотрите прикрепленную фотографию.'
    await bot.send_message(chat_id=user_data["user_id"], text=f'✉ Новое уведомление!\n\
Ответ на вашу заявку <b>#{user_data["number_b"]}</b> от менеджера проката:\n<b>{caption}</b>', parse_mode='HTML',
                           reply_markup=builder.as_markup())
    await bot.send_photo(chat_id=user_data['user_id'], photo=photo)
    await state.clear()


# Обработка сообщений с документом
@router.message(FSMadmin.answer_book, F.content_type == 'document')
async def load_answer(message: types.Message, state: FSMContext):
    document = message.document.file_id
    caption = message.caption
    user_data = await state.get_data()
    await message.reply(f'✅ Вы успешно ответили на заявку <b>#{user_data["number_b"]}</b>!', parse_mode='HTML')
    # создание инлайн кнопки
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Ответить",
        callback_data=f'rс{user_data["user_id"]}_{user_data["number_b"]}'))
    if caption == None:
        caption = 'Смотрите прикрепленный документ.'
    await bot.send_message(chat_id=user_data["user_id"], text=f'✉ Новое уведомление!\n\
Ответ на вашу заявку <b>#{user_data["number_b"]}</b> от менеджера проката:\n<b>{caption}</b>', parse_mode='HTML',
                           reply_markup=builder.as_markup())
    await bot.send_document(chat_id=user_data['user_id'], document=document)
    await state.clear()


# Отбраковка сообщений которые не являются текстом/фото/документом
@router.message(FSMadmin.answer_book, F.content_type != 'text')
async def book_step(message: types.Message, state: FSMContext):
    await message.answer('Отправьте ответ <b>текстовым сообщением, картинкой или документом</b>', parse_mode='HTML')


# обработка инлайн кнопки "ответить на заявку" продолжение
@router.message(FSMadmin.answer_book)
async def load_answer(message: types.Message, state: FSMContext):
    answer = message.text
    user_data = await state.get_data()
    await message.reply(f'✅ Вы успешно ответили на заявку <b>#{user_data["number_b"]}</b>!', parse_mode='HTML')
    # создание инлайн кнопки
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Ответить",
        callback_data=f'rс{user_data["user_id"]}_{user_data["number_b"]}'))

    await bot.send_message(chat_id=user_data["user_id"], text=f'✉ Новое уведомление!\n\
Ответ на вашу заявку <b>#{user_data["number_b"]}</b> от менеджера проката:\n<b>{answer}</b>', parse_mode='HTML',
                           reply_markup=builder.as_markup())
    await state.clear()


# обработка инлайн кнопки "ответить" начало
@router.callback_query(Text(startswith="ra"))
async def send_manager_answer(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    user_id = callback.data.split('_')[0][2:]
    await state.update_data(user_id=user_id)
    number_q = callback.data.split('_')[1].rstrip()
    await state.update_data(number_q=number_q)
    await bot.send_message(chat_id=group_id,
                           text=f"Напишите ниже ваш ответ на дополнение к вопросу/заявке\n<b>#{number_q}</b>:", parse_mode='HTML')
    await state.set_state(FSMreqa.reqa)


# Обработка сообщений с фото
@router.message(FSMreqa.reqa, F.content_type == 'photo')
async def load_answer(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    caption = message.caption
    user_data = await state.get_data()
    await message.reply(f'✅ Ваш ответ успешно отправлен!', parse_mode='HTML')
    # создание инлайн кнопки
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Ответить",
        callback_data=f'rс{user_data["user_id"]}_{user_data["number_q"]}'))
    if caption == None:
        caption = 'Смотрите прикрепленную фотографию.'
    await bot.send_message(chat_id=user_data["user_id"], text=f'✉ Новое уведомление!\n\
Ответ на ваше дополнение к вопросу/заявке <b>#{user_data["number_q"]}</b> от менеджера проката:\n<b>{caption}</b>',
                           parse_mode='HTML', reply_markup=builder.as_markup())
    await bot.send_photo(chat_id=user_data['user_id'], photo=photo)
    await state.clear()


# Обработка сообщений с документом
@router.message(FSMreqa.reqa, F.content_type == 'document')
async def load_answer(message: types.Message, state: FSMContext):
    document = message.document.file_id
    caption = message.caption
    user_data = await state.get_data()
    await message.reply(f'✅ Ваш ответ успешно отправлен!', parse_mode='HTML')
    # создание инлайн кнопки
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Ответить",
        callback_data=f'rс{user_data["user_id"]}_{user_data["number_q"]}'))
    if caption == None:
        caption = 'Смотрите прикрепленный документ.'
    await bot.send_message(chat_id=user_data["user_id"], text=f'✉ Новое уведомление!\n\
Ответ на ваше дополнение к вопросу/заявке <b>#{user_data["number_q"]}</b> от менеджера проката:\n<b>{caption}</b>',
                           parse_mode='HTML', reply_markup=builder.as_markup())
    await bot.send_document(chat_id=user_data['user_id'], document=document)
    await state.clear()


# Отбраковка сообщений которые не являются текстом/фото/документом
@router.message(FSMreqa.reqa, F.content_type != 'text')
async def book_step(message: types.Message, state: FSMContext):
    await message.answer('Отправьте ответ <b>текстовым сообщением, картинкой или документом</b>', parse_mode='HTML')


# обработка инлайн кнопки "ответить" продолжение
@router.message(FSMreqa.reqa)
async def load_answer(message: types.Message, state: FSMContext):
    answer = message.text
    user_data = await state.get_data()
    await message.reply(f'✅ Ваш ответ успешно отправлен!', parse_mode='HTML')
    # создание инлайн кнопки
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Ответить",
        callback_data=f'rс{user_data["user_id"]}_{user_data["number_q"]}'))
    await bot.send_message(chat_id=user_data["user_id"], text=f'✉ Новое уведомление!\n\
Ответ на ваше дополнение к вопросу/заявке <b>#{user_data["number_q"]}</b> от менеджера проката:\n<b>{answer}</b>', parse_mode='HTML',
                           reply_markup=builder.as_markup())
    # завершение машины состояний
    await state.clear()


# обработка инлайн кнопки "пригласить в ЛС"
@router.callback_query(Text(startswith="ls"))
async def send_manager_answer(callback: types.CallbackQuery):
    await callback.answer()
    info = callback.data.split('_')
    user_id = info[0][2:]
    number_q = info[1]
# создание инлайн кнопки
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Написать менеджеру проката", url=f"tg://user?id={mng_id}"))
    await bot.send_message(chat_id=user_id, text=f'''
✉ Новое уведомление!
Для обсуждения вашего вопроса, пожалуйста, <b>напишите менеджеру проката</b>.
Для этого скопируйте ваш номер вопроса <code>#{number_q}</code>, <b>нажав на него</b>, и отправьте его \
менеджеру, воспользовавшись <b>кнопкой ниже</b>.
''', parse_mode='HTML', reply_markup=builder.as_markup())
    await bot.send_message(chat_id=group_id,
                           text=f'✅ Приглашение перейти в личные сообщения успешно отправлено пользователю ID: {user_id}',
                           parse_mode='HTML')
