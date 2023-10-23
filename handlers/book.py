from aiogram import types, Router, F
from aiogram.filters.text import Text
from create_bot import bot
from keyboards import kb_client, kb_client_ret, kb_book_1, kb_book_2, kb_book_3
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder
from configurebot import cfg
from datetime import datetime, timedelta
from pytz import timezone


class NegativeDateError(Exception):
    pass


class FSMbook(StatesGroup):
    step1 = State()
    step2 = State()
    step3 = State()
    step4 = State()
    step5 = State()
    step6 = State()
    step7 = State()
    step8 = State()
    step9 = State()


router = Router()
group_id = cfg['group_id']


# Обработка кнопки возврата в главное меню
@router.message(Text(text="Вернуться в главное меню", ignore_case=True))
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(text="Вы вернулись в главное меню", reply_markup=kb_client)


@router.message(Text(text='Отправить заявку', ignore_case=True))
async def command_book(message: types.Message, state: FSMContext):
    await message.answer('''Если вы уже определились с необходимым снаряжением, то <b>нажмите кнопку "Продолжить"</b>. \
Если еще нет, то посмотрите наш прайс-лист <b>в главном меню.</b>''', parse_mode='HTML', reply_markup=kb_book_1)
    await state.set_state(FSMbook.step1)


# Отбраковка сообщений которые не являются текстовыми
@router.message(FSMbook.step1, F.content_type != 'text')
async def book_step(message: types.Message, state: FSMContext):
    await message.answer('Пожалуйста, воспользуйтесь кнопками меню.')


# Обработка кнопки продолжить в оформлении заявки
@router.message(FSMbook.step1)
async def book_step(message: types.Message, state: FSMContext):
    if message.text == 'Продолжить':
        await message.answer('Вы раньше пользовались услугами нашего проката?', reply_markup=kb_book_2)
        await state.set_state(FSMbook.step2)
    else:
        await message.answer('Пожалуйста, воспользуйтесь кнопками меню.')


# Обработка да/нет на постоянного клиента
@router.message(FSMbook.step2)
async def book_step(message: types.Message, state: FSMContext):
    if message.text in ('Да', 'Нет'):
        await state.update_data(user_id=message.chat.id)
        await state.update_data(old_client=message.text)
        await state.set_state(FSMbook.step3)
        await message.answer('Введите ваши ФИО согласно образцу:\n<b>Иванов Иван Иванович</b>',
                             parse_mode='HTML', reply_markup=kb_client_ret)
    else:
        await message.answer('Пожалуйста, воспользуйтесь кнопками меню.')


# Отбраковка не текстовых сообщений на шаге ввода ФИО
@router.message(FSMbook.step3, F.content_type != 'text')
async def book_step(message: types.Message, state: FSMContext):
    await message.answer('Пожалуйста, введите ваши ФИО согласно образцу:\n<b>Иванов Иван Иванович</b>',
                         parse_mode='HTML')


# Запрос ФИО
@router.message(FSMbook.step3)
async def book_step(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Введите ваш номер сотового согласно образцу:\n<b>89827303231</b>', parse_mode='HTML')
    await state.set_state(FSMbook.step4)


# Отбраковка не текстовых сообщений на шаге ввода номера сотового
@router.message(FSMbook.step4, F.content_type != 'text')
async def book_step(message: types.Message, state: FSMContext):
    await message.answer('Пожалуйста, введите ваш номер сотового телефона согласно образцу:\n<b>89827303231</b>',
                         parse_mode='HTML')


# Запрос сотового
@router.message(FSMbook.step4)
async def book_step(message: types.Message, state: FSMContext):
    if message.text.isdigit() and len(message.text) == 11:
        await state.update_data(phone=message.text)
        user_data = await state.get_data()
        if user_data['old_client'] == 'Да':
            await message.answer(f'Введите дату, в которую вы хотите получить снаряжение, \
согласно образцу:\n<b>{datetime.strftime(datetime.now(), "%d.%m.%y")}</b> (день.месяц.год)', parse_mode='HTML')
            await state.set_state(FSMbook.step6)
        else:
            await message.answer('Введите ваш адрес регистрации \
согласно образцу:\n<b>Екатеринбург, Кулибина, 1а, 100</b>', parse_mode='HTML')
            await state.set_state(FSMbook.step5)
    else:
        await message.answer('Пожалуйста, введите ваш номер сотового телефона согласно образцу:\n<b>89827303231</b>',
                             parse_mode='HTML')


# Отбраковка не текстовых сообщений на шаге ввода адреса
@router.message(FSMbook.step5, F.content_type != 'text')
async def book_step(message: types.Message, state: FSMContext):
    await message.answer('Пожалуйста, введите ваш адрес регистрации \
согласно образцу:\n<b>Екатеринбург, Кулибина, 1а, 100</b>', parse_mode='HTML')


# Запрос адреса
@router.message(FSMbook.step5)
async def book_step(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer(f'Введите дату, в которую вы хотите получить снаряжение, \
согласно образцу:\n<b>{datetime.strftime(datetime.now(), "%d.%m.%y")}</b> (день.месяц.год)', parse_mode='HTML')
    await state.set_state(FSMbook.step6)


# Отбраковка не текстовых сообщений на шаге ввода даты начала
@router.message(FSMbook.step6, F.content_type != 'text')
async def book_step(message: types.Message, state: FSMContext):
    await message.answer(f'Пожалуйста, введите дату, в которую вы хотите получить снаряжение, \
согласно образцу:\n<b>{datetime.strftime(datetime.now(), "%d.%m.%y")}</b> (день.месяц.год)', parse_mode='HTML')


# Запрос даты начала
@router.message(FSMbook.step6)
async def book_step(message: types.Message, state: FSMContext):
    try:
        start = datetime.strptime(message.text, '%d.%m.%y')
        now = datetime.now()
        if start.date() < now.date():
            raise NegativeDateError
        await state.update_data(start=start)
        await message.answer(f'Введите дату, в которую вы хотите сдать снаряжение, \
согласно образцу:\n<b>{datetime.strftime(start + timedelta(1), "%d.%m.%y")}</b> (день.месяц.год)', parse_mode='HTML')
        await state.set_state(FSMbook.step7)
    except NegativeDateError:
        await message.answer('К сожалению, вы не можете вернуться в прошлое 😔')
        await message.answer(f'Пожалуйста, введите дату, в которую вы хотите получить снаряжение, \
согласно образцу:\n<b>{datetime.strftime(datetime.now(), "%d.%m.%y")}</b> (день.месяц.год)', parse_mode='HTML')
    except:
        await message.answer(f'Пожалуйста, введите дату, в которую вы хотите получить снаряжение, \
согласно образцу:\n<b>{datetime.strftime(datetime.now(), "%d.%m.%y")}</b> (день.месяц.год)', parse_mode='HTML')


# Отбраковка не текстовых сообщений на шаге ввода даты конца
@router.message(FSMbook.step7, F.content_type != 'text')
async def book_step(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    start = user_data['start']
    await message.answer(f'Пожалуйста, введите дату, в которую вы хотите сдать снаряжение, \
согласно образцу:\n<b>{datetime.strftime(start + timedelta(1), "%d.%m.%y")}</b> (день.месяц.год)', parse_mode='HTML')


# Запрос даты конца
@router.message(FSMbook.step7)
async def book_step(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    start = user_data['start']
    try:
        end = datetime.strptime(message.text, '%d.%m.%y')
        if end.date() < start.date():
            raise NegativeDateError
        await state.update_data(end=end)
        await message.answer('Отправьте одним <b>текстовым сообщением</b> \
список необходимого вам снаряжения в свободной форме', parse_mode='HTML')
        await state.set_state(FSMbook.step8)
    except NegativeDateError:
        await message.answer('Дата сдачи не может быть раньше даты выдачи 😔')
        await message.answer(f'Пожалуйста, введите дату, в которую вы хотите сдать снаряжение, \
согласно образцу:\n<b>{datetime.strftime(start + timedelta(1), "%d.%m.%y")}</b> (день.месяц.год)', parse_mode='HTML')
    except:
        await message.answer(f'Пожалуйста, введите дату, в которую вы хотите сдать снаряжение, \
согласно образцу:\n<b>{datetime.strftime(start + timedelta(1), "%d.%m.%y")}</b> (день.месяц.год)', parse_mode='HTML')


# Отбраковка не текстовых сообщений на шаге ввода списка снаряжения
@router.message(FSMbook.step8, F.content_type != 'text')
async def book_step(message: types.Message, state: FSMContext):
    await message.answer('Отправьте одним <b>текстовым сообщением</b> \
список необходимого вам снаряжения в свободной форме.', parse_mode='HTML')


# Запрос списка снаряжения
@router.message(FSMbook.step8)
async def book_step(message: types.Message, state: FSMContext):
    await state.update_data(equip=message.text)
    user_data = await state.get_data()
    await message.answer('''Пожалуйста, проверьте вашу заявку и <b>нажмите кнопку "Отправить"</b>.
*Если вы обнаружили ошибку, пожалуйста, <b>вернитесь в главное меню</b> и оформите заявку заново.''', parse_mode='HTML')
    book = f'''
<b>Ваша заявка:</b>   
<b>ФИО:</b> {user_data['name']}
<b>Тел.:</b> {user_data['phone']}'''
    if user_data['old_client'] == 'Нет':
        book += f'''\n<b>Адрес:</b> {user_data['address']}'''
    book += f'''
<b>Даты проката:</b> {datetime.strftime(user_data['start'], "%d.%m.%y")} - {datetime.strftime(user_data['end'], "%d.%m.%y")}
<b>Снаряжение:</b> {user_data['equip']}'''
    await message.answer(book, parse_mode='HTML', reply_markup=kb_book_3)
    await state.set_state(FSMbook.step9)


# Обработка отправки заявки
@router.message(FSMbook.step9)
async def book_step(message: types.Message, state: FSMContext):
    if message.text == 'Отправить':
        user_data = await state.get_data()
        user_id = user_data['user_id']
        date = message.date
        date_ekb = date.astimezone(timezone('Asia/Yekaterinburg'))
        formatted_date = date_ekb.strftime("%d%H%M%S")
        number_b = f'b{str(message.chat.id)[-3:]}{formatted_date}'
        await bot.send_message(chat_id=user_id,
                               text=f'Ваша заявка <b>#{number_b}</b> отправлена, наш менеджер пришлёт ответ в этот чат в рабочее время.',
                               parse_mode='HTML', reply_markup=kb_client)
        book = f'''
<b>ID:</b> {user_data['user_id']}       
<b>ФИО:</b> {user_data['name']}
<b>Постоянный клиент:</b> {user_data['old_client']}
<b>Тел.:</b> {user_data['phone']}'''
        if user_data['old_client'] == 'Нет':
            book += f'''\n<b>Адрес:</b> {user_data['address']}'''
        book += f'''
<b>Даты проката:</b> {datetime.strftime(user_data['start'], "%d.%m.%y")} - {datetime.strftime(user_data['end'], "%d.%m.%y")}
<b>Снаряжение:</b> {user_data['equip']}'''
        # создание инлайн клавиатуры
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(text="Ответить на заявку", callback_data=f'b{user_data["user_id"]}'))
        builder.add(types.InlineKeyboardButton(text="Пригласить в ЛС", callback_data=f'ls{message.chat.id}_{number_b}'))

        await bot.send_message(chat_id=group_id, text=f"✉ | Новая заявка <b>#{number_b}</b>:{book}",
                               parse_mode='HTML', reply_markup=builder.as_markup())
        # завершение машины состояний
        await state.clear()
    else:
        await message.answer('Пожалуйста, воспользуйтесь кнопками меню.')
