from contextvars import Token
from aiogram import executor,Bot,Dispatcher,types
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold,hlink
from wildberes import save_exel
import pandas



TOKEN = "2082282627:AAHRXZs3GItp0wjaZPxmKmz_kkiEvQzgAdY"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message:types.message):
    start_buttons = ["Xiaomi","Adidas","Apple"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer("Привет,я парсер магазина wildberes",reply_markup=keyboard)
@dp.message_handler(Text(equals="Xiaomi"))
async def get_discount_xiaomi(message:types.Message):
    await message.answer("Please waiting...")
    
    save_exel(data=None)
    data = pandas.read_excel('data.xlsx')
    for item in data:
        card = f"{hlink(item.get('title'),item.get('link'))}\n"\
            f"{hbold('Категория:')} {item.get('brand')}\n"\
            f"{hbold('Прайс: ')} {item.get('price')}\n" \
            f"{hbold('Скидка на товар:')} {item.get('discount')}"
        await message.answer(card)
        


def main():
    executor.start_polling(dp)




if __name__ == "__main__":
    main()
    

