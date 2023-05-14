
from aiogram import Bot, Dispatcher, executor, types, filters
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

inline_buttons = types.InlineKeyboardMarkup()
b1 = types.InlineKeyboardButton(text='Один', callback_data='sendone')
b2 = types.InlineKeyboardButton(text='Несколько', callback_data='sendmany')
b3 = types.InlineKeyboardButton(text='Передумал', callback_data='break')

inline_buttons.add(b1, b2)
inline_buttons.row(b3)



kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttonslist = [types.KeyboardButton(text='button1'),
types.KeyboardButton(text='Номер телефона', request_contact=True),
types.KeyboardButton(text='button3'),]

kb.add(*buttonslist)


@dp.message_handler(commands=['start'])
async def cmd_handler(message: types.Message):
    await message.answer('Its help bot', reply_markup=kb)
    
@dp.message_handler(commands=['welcome', 'about'])
async def cmd_handler(message: types.Message):
    await message.answer('Its help bot')

@dp.message_handler(lambda message: message.text and 'hello' in message.text.lower())
@dp.edited_message_handler(lambda message: message.text and 'hello' in message.text.lower())
async def msg_handler(message: types.Message):
    await message.answer('И тебе привет')


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def audio_handler(message: types.Message):

    await message.answer('Крутая фотка')

@dp.message_handler(content_types=types.ContentType.CONTACT)
async def audio_handler(message: types.Message):

    await message.answer('номер получен', reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(filters.Text(contains='мем'))
async def cmd_handler(message: types.Message):
    await message.answer('была нажата кнопка мем', reply_markup=inline_buttons)

@dp.callback_query_handler(filters.Text(contains='sendmany'))
async def some_callback_handler(callback_query: types.CallbackQuery):
    media = types.MediaGroup()
    media.attach_photo(photo=types.InputFile('../img/1.jpg'), caption='первый')
    media.attach_photo(photo=types.InputFile('../img/2.jpg'), caption='второй')
    await callback_query.message.answer_media_group(media=media)

    listofphotos = [
        types.InputMediaPhoto(types.InputFile('../img/1.jpg')),
        types.InputMediaPhoto(types.InputFile('../img/2.jpg'), caption='второе'),
        types.InputMediaPhoto(types.InputFile('../img/3.jpg'), caption='третий')
    ]

    await callback_query.message.answer_media_group(listofphotos)
    await callback_query.answer()


# @dp.message_handler()
# async def echo(message: types.Message):

    # await message.answer('Hello')
    # await bot.send_message(chat_id=message.from_user.id, text='Hello')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

