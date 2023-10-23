from aiogram import types, Router
from aiogram.filters.text import Text
from create_bot import bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from configurebot import cfg, docs, photo
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboards import exit_price, kb_client, inline_kb_g, inline_kb_b, inline_kb_y, inline_kb_ow, inline_kb_ot,\
    inline_kb_or, inline_kb_ob


class FSMprice(StatesGroup):
    exit = State()


router = Router()
group_id = cfg['group_id']
dict_kb = {'inline_kb_g': inline_kb_g, 'inline_kb_b': inline_kb_b, 'inline_kb_y': inline_kb_y,
           'inline_kb_ow': inline_kb_ow, 'inline_kb_ot': inline_kb_ot, 'inline_kb_or': inline_kb_or,
           'inline_kb_ob': inline_kb_ob}


# Обработка кнопки Прайс-лист
@router.message(Text(text='Прайс-лист', ignore_case=True))
async def command_price(message: types.Message, state: FSMContext):
    user_id = message.chat.id
    price_id = message.message_id
    await state.update_data(user_id=user_id)
    await state.update_data(price_id=price_id)
    await message.answer('Вы зашли в прайс-лист, для выхода нажмите <b>Закрыть прайс-лист</b>.',
                         reply_markup=exit_price, parse_mode='HTML')

    await bot.send_message(chat_id=user_id, text='Выберите подраздел:', reply_markup=inline_kb_g)
    await state.set_state(FSMprice.exit)


# Обработка кнопки выхода из прайс-листа
@router.message(FSMprice.exit)
async def menu(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    user_id = user_data['user_id']
    price_id = user_data['price_id']
    msg_id = message.message_id
    if message.text == 'Закрыть прайс-лист':
        try:
            for m_id in range(price_id, msg_id + 1):
                await bot.delete_message(chat_id=user_id, message_id=m_id)
        except:
            pass
        await message.answer('Вы вернулись в главное меню.', reply_markup=kb_client)
        await state.clear()
    else:
        await message.answer('Пожалуйста, воспользуйтесь кнопками меню.', reply_markup=exit_price)


# Обработка кнопки скачать прайс-лист
@router.callback_query(Text(startswith='g_3_Скачать полный прайс-лист'))
async def price(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    user_id = user_data['user_id']

    msg = await bot.send_document(chat_id=user_id , document=docs['price'])

    ret_del = InlineKeyboardButton(text='Вернуться назад', callback_data=f'del/inline_kb_g/{msg.message_id}')
    inline_kb_del = InlineKeyboardMarkup(inline_keyboard=[[ret_del]], resize_keyboard=True)

    await callback.message.edit_text(f'Скачайте прикрепленный ниже файл', reply_markup=inline_kb_del)


# Обработка кнопки вернуться назад с удалением
@router.callback_query(Text(startswith='del/'))
async def ret_del(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    user_id = user_data['user_id']

    next_menu = dict_kb[callback.data.split('/')[1]]
    del_msg = callback.data.split('/')[2]

    await bot.delete_message(chat_id=user_id, message_id=del_msg)
    await callback.message.edit_text('Выберите подраздел:', reply_markup=next_menu)


# Обработка кнопки вернуться назад внутри меню
@router.callback_query(Text(startswith='ret'))
async def ret(callback: types.CallbackQuery, state: FSMContext):
    next_menu = dict_kb[f'inline_kb_{callback.data.split("_")[1]}']
    await callback.message.edit_text('Выберите подраздел:', reply_markup=next_menu)


# Обработка кнопки Туристическое снаряжение
@router.callback_query(Text(startswith='g_1_'))
async def price(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Выберите подраздел:', reply_markup=inline_kb_b)


# Обработка кнопки Лыжи и сноуборды
@router.callback_query(Text(startswith='g_2_'))
async def price(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Выберите подраздел:', reply_markup=inline_kb_y)


# Обработка кнопки Палатки
@router.callback_query(Text(startswith='b_1_'))
async def price(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Выберите подраздел:', reply_markup=inline_kb_ot)


# Обработка кнопки Спальники
@router.callback_query(Text(startswith='b_7_'))
async def price(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Выберите подраздел:', reply_markup=inline_kb_ob)


# Обработка кнопки Водный туризм
@router.callback_query(Text(startswith='b_8_'))
async def price(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Выберите подраздел:', reply_markup=inline_kb_ow)


# Обработка кнопки Горное снаряжение
@router.callback_query(Text(startswith='b_9_'))
async def price(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Выберите подраздел:', reply_markup=inline_kb_or)


# Обработка всех остальных кнопок
@router.callback_query(Text(startswith=('b_', 'y_', 'ot_', 'or_', 'ob_', 'ow_')))
async def price(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    user_id = user_data['user_id']
    pos = callback.data.split('_')[2]
    ret_menu = callback.data.split('_')[0]
    msg = await bot.send_photo(chat_id=user_id, photo=photo[pos])
    ret = InlineKeyboardButton(text='Вернуться назад', callback_data=f'del/inline_kb_{ret_menu}/{msg.message_id}')
    inline_kb_del = InlineKeyboardMarkup(inline_keyboard=[[ret]], resize_keyboard=True)
    await callback.message.edit_text(f'Ниже представлена категория "{pos}"', reply_markup=inline_kb_del)
