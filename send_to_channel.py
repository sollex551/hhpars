import asyncio
import json
import logging


from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
import re

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from eses import generate_photo
import csv

from parser import return_description_by_id


logging.basicConfig(level=logging.INFO)

bot = Bot(token="6621530107")

dp = Dispatcher()

FILENAME = "users.csv"


def check_id():
    with open("vacancy_info.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    print("✅ cmd_start() вызван!")
    existing_links = set()
    return_description_by_id()
    with open(FILENAME, "r", newline="") as file:
        reader = csv.reader(file)
        existing_links = {row[0] for row in reader}

    for vacancy in check_id():
        if vacancy['Ссылка'] in existing_links:
            continue
        await bot.send_message(1037572930, f"Отправка началась!")

        description = vacancy['Описание'].replace('<ul>', '').replace('</ul>', '') \
            .replace('<li>', '•').replace('</li>', '\n')

        if len(description) > 512:
            description = description[:820].rstrip() + f'<a href="{vacancy["Ссылка"]}">... Читать дальше</a>'

        text = f"Нужен <strong> {vacancy['Вакансия']} </strong> в компанию <strong> {vacancy['Компания']} </strong> \n"
        text += f"<strong>Город: </strong>{vacancy['Город']}\n"
        text += f"\n{description}\n\n"
        text += f"<strong> Зарплата: </strong>{vacancy['Зарплата']}"

        generate_photo(vacancy['Зарплата'], vacancy['Вакансия'])
        button = InlineKeyboardButton(text="Перейти к вакансии", url=vacancy["Ссылка"])
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])


        photo = FSInputFile("new_img.jpg")

        await bot.send_photo(chat_id=-1002241525430, photo=photo, caption=text, reply_markup=keyboard,
                             parse_mode=ParseMode.HTML)


        with open(FILENAME, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([vacancy['Ссылка']])

        existing_links.add(vacancy['Ссылка'])


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
