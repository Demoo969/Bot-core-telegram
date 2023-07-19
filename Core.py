from aiogram import executor, types
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from dispatcher import dp,bot
from collections import deque
import filters
from functions import moderate, others
import asyncio,time
from config import *

user_stickers = {}
user_gifs = {}

#Хранит на каком этапе диалога находится клиент
class ClientState(StatesGroup):
    
    SELECT_ID = State()
    END = State()
   
async def on_startup(_):
    print('working:3')

class commands:
          
    @dp.message_handler(is_owner=True,commands=("msg","m","с"),commands_prefix=(".","/"))
    async def chat_menu(message: types.Message):
        # Создаем клавиатуру с двумя кнопками
        kb = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('Мира', callback_data='Mirai')
        button2 = types.InlineKeyboardButton('Лис', callback_data='Fox')
        button3 = types.InlineKeyboardButton('Тест', callback_data='Test')
        button4 = types.InlineKeyboardButton('Сброс', callback_data='cancel')
        kb.add(button1, button2, button3)
        kb.insert(button4)
        # Отправляем сообщение с инлайн-клавиатурой
        await message.reply("Выберите действие:", reply_markup=kb)

    @dp.callback_query_handler(lambda c: c.data) 
    async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
        global chat_id
        if callback_query.data == 'Mirai':
            chat_id=ids.mirai
            await bot.answer_callback_query(callback_query.id, text='Done', show_alert=False)
            await state.set_state(ClientState.SELECT_ID)
        elif callback_query.data == 'Fox':
            chat_id=ids.fox
            await bot.answer_callback_query(callback_query.id, text='Done', show_alert=False)
            await state.set_state(ClientState.SELECT_ID)
        elif callback_query.data == 'Test':
            chat_id=ids.test
            await bot.answer_callback_query(callback_query.id, text='Done', show_alert=False)
            await state.set_state(ClientState.SELECT_ID)
            
    @dp.callback_query_handler(lambda c: c.data == 'cancel', state=ClientState.SELECT_ID)
    async def cancel(callback_query: types.CallbackQuery, state: FSMContext):
        await state.set_state(ClientState.END)  
        await bot.answer_callback_query(callback_query.id, text='Айди сброшен можете менять чат', show_alert=False)
        
    @dp.message_handler(content_types=[types.ContentType.TEXT, types.ContentType.STICKER], state=ClientState.SELECT_ID)
    async def send_message_or_sticker(message: types.Message, state: FSMContext):
        if message.text == "#":
            await message.answer("Отправка сообщений отменена.")
            await state.set_state(ClientState.END)
        elif message.text is not None:
            chat_name = await others.get_chat_name(chat_id)
            if message.content_type == types.ContentType.TEXT:
                await message.answer(f"Текстовое сообщение отправлено в {chat_name}")
                await bot.send_message(chat_id=chat_id, text=message.text)
            elif message.content_type == types.ContentType.STICKER:
                await message.answer(f"Стикер отправлен в {chat_name}")
                await bot.send_sticker(chat_id=chat_id, sticker=message.sticker.file_id)
              
    @dp.message_handler(is_owner=True,commands=("del","d","delete"),commands_prefix=(".","\\","/"))   
    async def msg_del(message: types.Message):
        args = message.text.split(' ', 1)
        param= int(args[1])
        await moderate.delete_lmessages(message.chat.id, message.message_id, param)

class speaking:
    @dp.message_handler(content_types=types.ContentType.TEXT)
    async def handle_message(message: types.Message):
        if any(keyw in message.text.lower() for keyw in keywords.hello):
            if message.from_user.id==BOT_OWNER:
                await message.reply("<b>Привет хозяин</b>")
                await bot.send_sticker(message.chat.id, sticker=stickers.smile)
            else:
                await message.reply(f"<b>Привет {message.from_user.first_name}</b>")
                await asyncio.sleep(0.5)
                box=await bot.send_sticker(message.chat.id, sticker=stickers.box)
                await asyncio.sleep(2)
                await box.delete()
        elif  any(k in message.text.lower() for k in keywords.fuck):
            await message.reply(f"<b>Пик будет не скоро !!! \nА вообще заходите на <a href='https://www.youtube.com/@LightFoxx/streams'>youtube</a> и смотрите там, если по записям стримов набирается 100 глав то видео выйдет в ближайшее время!!!</b>")
        elif  any(k in message.text.lower() for k in keywords.stream):
            await message.reply("стримы каждую неделю в<b> пн,ср,пт в 18.00 по Москве</b>, иногда проходят игровые стрими за этим уже следить на канале LightFox")
        elif message.from_user.id==BOT_OWNER and message.text.lower() == "скажи айди":
            msg=await message.answer(f"айди чата: {message.chat.id}")
            await asyncio.sleep(3)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            await msg.delete()
       
#выше все импорты и глобальный  user_stickers                 
class stickers:
    @dp.message_handler(content_types=["sticker"])
    async def agro_stick(message: types.Message):
        user_id= message.from_user.id 
        if user_id not in user_stickers:
            user_stickers[user_id] = deque(maxlen=MAX_STICKERS)
        # Добавляем текущий стикер в список
        user_stickers[user_id].append(message.sticker.file_unique_id)  
        if len(user_stickers[user_id]) == MAX_STICKERS:
            if len(set(user_stickers[user_id])) == 1:
                # Если все стикеры одинаковые, удаляем их
                await moderate.delete_lmessages(message.chat.id, message.message_id, MAX_STICKERS)
                msg = await message.answer("Спамить вредно для здоровья!!!")
                await asyncio.sleep(3)  
                await msg.delete()
            
        if message.from_user.id != BOT_OWNER and message.sticker.file_unique_id == stickers.ranni_id:
            await message.reply("Не тронь мой стикер, а то заколдую!!!!")
            await bot.send_sticker(message.chat.id, sticker=stickers.stk1) 
        elif message.from_user.id == BOT_OWNER and message.sticker.file_unique_id == stickers.ranni_id:
            if not message.reply_to_message:
                await message.reply("так не сработает (")
                return   
            else:
                await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(), until_date=int(time.time()) + 2*60)
                await message.answer("Заколдован сюка!")
        # else: 
        #     msg=await message.reply("Прикольный стикер :3")
        #     await asyncio.sleep(5)
        #     await msg.delete()
class animations:
    @dp.message_handler(content_types=["animation"])
    async def agro_animatons(message: types.Message):
        user_id = message.from_user.id
        if user_id not in user_gifs:
            user_gifs[user_id] = deque(maxlen=MAX_ANIMATIONS)
        # Добавляем текущую гифку в список
        user_gifs[user_id].append(message.animation.file_unique_id)
        if len(user_gifs[user_id]) == MAX_ANIMATIONS:
            if len(set(user_gifs[user_id])) == 1:
                # Если все гифки одинаковые, удаляем их
                await moderate.delete_lmessages(message.chat.id, message.message_id, MAX_ANIMATIONS)
                msg = await message.answer("Спамить вредно для здоровья!!!")
                await asyncio.sleep(3)
                await msg.delete()
 
if __name__ == '__main__':
   executor.start_polling(dp, on_startup=on_startup)
   

   
