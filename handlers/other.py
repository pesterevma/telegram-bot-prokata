from aiogram import types, Router, F
from create_bot import bot
from keyboards import kb_client, kb_manager
from configurebot import cfg

router = Router()
group_id = cfg['group_id']
adm_id = cfg['adm_id']


# обработка всех остальных сообщений у менеджера
@router.message((F.from_user.id.in_(adm_id)) & (F.chat.type.in_({"group"})))
async def other_send(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text='Пожалуйста, воспользуйтесь инлайн-кнопками.', reply_markup=kb_manager)


# обработка всех остальных сообщений у клиента
@router.message()
async def other_send(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text='Пожалуйста, воспользуйтесь кнопками меню.', reply_markup=kb_client)

