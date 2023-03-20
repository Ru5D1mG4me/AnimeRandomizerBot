from config import API_TOKEN
import functions
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ParseMode
from aiogram import executor


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton(text='Random'))


@dp.message_handler(commands='start')
async def send_welcome(message: Message):
    await message.answer('Hello. I\'m AnimeRandomizerBot.\nI can tell you what anime to watch.\nClick on the <b>Random</b> button.',
                         parse_mode=ParseMode.HTML, 
                         reply_markup=keyboard)


@dp.message_handler(commands='help')
async def send_help(message: Message):
    await message.answer('Click on the <b>Random</b> button to get anime with full details.',
                         parse_mode=ParseMode.HTML)


@dp.message_handler(lambda message: message.text == "Random")
async def button_click(message: Message):
    await message.answer('<b>Randomizing...</b>', parse_mode=ParseMode.HTML)
    random_anime = functions.get_random_anime()
    photo_url = functions.get_picture_url(random_anime)
    text_message = (f'<b>Name:</b> {functions.get_name(random_anime)}' + 
    f'\n<b>Premiered</b>: {functions.get_premiered(random_anime)}' + 
    f'\n<b>Type</b>: {functions.get_type(random_anime)}' + 
    f'\n<b>Rating</b>: {functions.get_rating(random_anime)}' + 
    f'\n<b>Score</b>: {functions.get_score(random_anime)}' + 
    f'\n<b>Episodes</b>: {functions.get_episodes(random_anime)}' + 
    f'\n<b>Genres</b>: {functions.get_genres(random_anime)}')
    await message.answer_photo(photo_url, text_message, parse_mode=ParseMode.HTML, 
                               reply_markup=keyboard)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)