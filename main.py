import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import aiohttp
import logging
import sqlite3

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)


class Form(StatesGroup):
    name = State()
    age = State()
    grade = State()

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer("Привет, cтудент! Как тебя зовут?")
    await state.set_state(Form.name)

@dp.message(Form.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(Form.age)

@dp.message(Form.age)
async def age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("На каком курсе ты учишься?")
    await state.set_state(Form.grade)

@dp.message(Form.grade)
async def grade(message: Message, state: FSMContext):
    await state.update_data(grade=message.text)
    data = await state.get_data()
    conn = sqlite3.connect('school_data.db')
    cursor = conn.cursor()

    cursor.execute(''' INSERT INTO students (name, age, grade) VALUES (?, ?, ?)''',
            (data['name'], data['age'], data['grade'])
                   )
    conn.commit()
    conn.close()
    await message.answer("Спасибо! Ты попал в Базу Данных! 😎")
    await state.clear()


@dp.message(Command(commands='help'))
async def help(message: Message):
    await message.answer("Помощь рядом")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())