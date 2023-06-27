from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from dispatcher import dp,bot
import filters
from config import stickers

async def on_startup(_):
    print('working:3')

@dp.message_handler(is_owner=True)
async def adm_message(message: types.Message):
    if "привет"or"Привет"in message.text:
        await message.answer("<b>Привет хозяиин</b>",)
        await bot.send_sticker(chat_id=message.from_user.id, sticker=stickers.smile)
@dp.message_handler()
async def message(message: types.Message):
    if "привет"or"Привет"in message.text:
        await message.answer("<b>Привет чалувек?</b>",)
        await bot.send_sticker(chat_id=message.from_user.id, sticker=stickers.box)
 
@dp.message_handler(is_ranni=True,content_types=["sticker"])
async def agrostick(message: types.Message):
        await bot.send_sticker(chat_id=message.from_user.id, sticker=stickers.stk1)   

@dp.message_handler(commands=("console"))
async def cmd_console(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Показать статус"),
            types.KeyboardButton(text="Показать баланс"),
            types.KeyboardButton(text="Показать профиль")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите действие"
    )
    await message.answer("Вас приветсвует терминал какие действия хотите выполнить", reply_markup=keyboard)

@dp.message_handler(text=("Показать статус"))
async def status(message: types.Message):
    charact=0
    Intelligence=4
    Strenght=2
    Reaction=3
    Composure=2
    Biotech=2
    await message.reply(
   
    "<b>|Характеристики игрока|============</b>\n"
    "<b>Очков характеристик для распределения:"f"{charact} </b>\n"
    "<b>Интеллект:"f"({Intelligence} из 10)</b>\n"
    "<b>Сила:"f"({Strenght} из 10)</b>\n"
    "<b>Реакция:"f"({Reaction} из 10)</b>\n"
    "<b>Хладнокровие:"f"({Composure} из 10)</b>\n"
    "<b>Биотехника:"f"({Biotech} из 10)</b>\n"
    "<b>=================================</b>"                     
    )
    
@dp.message_handler(text=("Показать профиль"))
async def profile(message: types.Message):
    await message.reply(
        "|Информация|=================\n"
        "Имя:"f"\n"
        "Возраст:"f"\n"
        "Рост:"f"\n"
        "Пол:"f"♀️♂️\n"
        "|Характер|===================="f"\n"
        "Описание характера вашего персонажа"f"\n" 
    )
@dp.message_handler(text=("Показать баланс"))
async def money(message: types.Message):
    await message.reply("")
    
if __name__ == '__main__':
   executor.start_polling(dp, on_startup=on_startup)
   