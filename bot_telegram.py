import asyncio
from create_bot import dp, bot
from handlers import book, price, client, admin, other

# регистрация всех хэндлеров
dp.include_router(book.router)
dp.include_router(price.router)
dp.include_router(client.router)
dp.include_router(admin.router)
dp.include_router(other.router)


async def on_startup():
    print('Бот успешно вышел в онлайн')

# Запуск процесса получения новых сообщений с сервера
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(on_startup())
    asyncio.run(main())
