import json
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware

API_TOKEN = 'token'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# загрузка списка тем и формул из файла json
with open('formulas.json', 'r', encoding='utf-8') as file:
    formulas_data = json.load(file)


# обработчик /start
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for class_name in formulas_data:
        keyboard.add(types.KeyboardButton(class_name))
    await message.answer("Выберите класс:", reply_markup=keyboard)

# Обработчик выбора класса
@dp.message_handler(lambda message: message.text in formulas_data.keys())
async def choose_class(message: types.Message):
    class_name = message.text
    topics = formulas_data[class_name]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for topic in topics:
        keyboard.add(types.KeyboardButton(topic))
    await message.answer("Выберите тему:", reply_markup=keyboard)

# Обработчик выбора темы
@dp.message_handler(lambda message: any(topic in message.text for topic in [item for sublist in formulas_data.values() for item in sublist]))
async def choose_topic(message: types.Message):
    for class_name, topics in formulas_data.items():
        for topic, formulas in topics.items():
            if topic == message.text:
                for formula in formulas:
                    await message.answer(f"Формула {topic}: \n {formula}")

if __name__ == '__main__':
    asyncio.run(dp.start_polling())
