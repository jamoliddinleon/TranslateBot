import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from database import *
from inline_btn import *
from utils import translate_text

BOT_TOKEN = "6584939843:AAFkLCKoevx3FTTS96JdubSN8kZKIg4ck5E"
ADMINS = [961500998]
logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode='html')
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)


async def command_menu(dp: Dispatcher):
    await create_tables()
    await dp.bot.set_my_commands(
        [
            types.BotCommand('start', 'Ishga tushirish'),
            types.BotCommand('help', 'yordam'),
        ]
    )


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await add_user(
        user_id=message.from_user.id,
        username=message.from_user.username
    )
    await message.answer("Salom.Men Engu Tarjimon bot")


@dp.message_handler(commands=['stat'])
async def get_user_stat_handler(message: types.Message):
    if message.from_user.id in ADMINS:
        counts = await get_all_users()
        await message.answer(f"Bot azolar soni: {counts} ta")


@dp.message_handler(content_types=['text'])
async def get_user_text_handler(message: types.Message):
    btn = await translate_langs_btn()
    await message.answer(text=message.text, reply_markup=btn)


@dp.callback_query_handler(text_contains='lang')
async def selected_lang_callback(call: types.CallbackQuery):
    lang = call.data.split(':')[-1]
    text = call.message.text

    result_text = await translate_text(text=text, lang=lang)

    btn = await translate_langs_btn()
    await call.message.edit_text(text=result_text, reply_markup=btn)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=command_menu)
