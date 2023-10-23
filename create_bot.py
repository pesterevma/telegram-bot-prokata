from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from configurebot import cfg

storage = MemoryStorage()

bot = Bot(token=cfg['token'])
dp = Dispatcher(storage=storage)

