from aiogram import types, Router
from create_bot import bot
from keyboards import kb_client

router = Router()


# обработка всех остальных сообщений
@router.message()
async def other_send(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text='Пожалуйста, воспользуйтесь кнопками меню.', reply_markup=kb_client)
