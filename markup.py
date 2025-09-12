from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram import types


b3 = types.KeyboardButton(text="Редактировать")
b4 = types.KeyboardButton(text="Отправить")
b5 = types.KeyboardButton(text="Посмотреть")
b6 = types.KeyboardButton(text="Завершена")


kb_proverka = types.ReplyKeyboardMarkup()
kb_proverka = types.ReplyKeyboardMarkup(resize_keyboard=True)
kb_proverka.add(b3,b4)

kb_textt = types.ReplyKeyboardMarkup()
kb_textt  = types.ReplyKeyboardMarkup(resize_keyboard=True)
kb_textt.add(b5)

kb_gotovo = types.ReplyKeyboardMarkup()
kb_gotovo  = types.ReplyKeyboardMarkup(resize_keyboard=True)
kb_gotovo.add(b6)


keyboard = types.InlineKeyboardMarkup()
keyboard.add(types.InlineKeyboardButton(text='Олег Савельев', callback_data='oleg'))
keyboard.add(types.InlineKeyboardButton(text='Андрей Савельев', callback_data='andrey'))


keyboard_gotovo = types.InlineKeyboardMarkup()
keyboard_gotovo.add(types.InlineKeyboardButton(text='Принять', callback_data='oleg_sotr'))

keyboard_completed = types.InlineKeyboardMarkup()
keyboard_completed.add(types.InlineKeyboardButton(text='Выполнено', callback_data='completed'))


get_all_zaivki = types.InlineKeyboardMarkup()
get_all_zaivki.add(types.InlineKeyboardButton(text='Принять все заявки', callback_data='get_all_zaivki'))

# keyboard_admin = types.InlineKeyboardMarkup()
# keyboard_admin.add(types.InlineKeyboardButton(text='1. Посмотреть'))
# keyboard_admin.add(types.InlineKeyboardButton(text='2. Смотреть новые заявки'))
# keyboard_admin.add(types.InlineKeyboardButton(text='3. Все назначеные заявки'))
# keyboard_admin.add(types.InlineKeyboardButton(text='4. Стоп'))

keyboard_admin = types.ReplyKeyboardMarkup()
keyboard_admin = types.ReplyKeyboardMarkup(row_width=0.1,resize_keyboard=True)
keyboard_admin.row(
        types.KeyboardButton(text="1. Посмотреть"),
        types.KeyboardButton(text="2. Смотреть новые заявки"))
kb_admin3 = types.KeyboardButton(text='3. Все назначеные заявки')
kb_admin4 = types.KeyboardButton(text='4. Список команд')
kb_admin5 = types.KeyboardButton(text='5. Стоп')
keyboard_admin.add( kb_admin3, kb_admin4)

# keyboard_sotrudnik = types.InlineKeyboardMarkup()
# keyboard_sotrudnik.add(types.InlineKeyboardButton(text='1. Посмотреть новые заявки'))
# keyboard_sotrudnik.add(types.InlineKeyboardButton(text='2. Смотреть все новые заявки заявки'))
# keyboard_sotrudnik.add(types.InlineKeyboardButton(text='3. Новые заявка по выбору'))
# keyboard_sotrudnik.add(types.InlineKeyboardButton(text='4. Все выполняющиеся заявки'))
# keyboard_sotrudnik.add(types.InlineKeyboardButton(text='5. Стоп'))

keyboard_sotrudnik = types.ReplyKeyboardMarkup()
keyboard_sotrudnik = types.ReplyKeyboardMarkup(row_width=0.1,resize_keyboard=True)
keyboard_sotrudnik.row(
        types.KeyboardButton(text='1. Посмотреть новые заявки'),
        types.KeyboardButton(text='2. Смотреть все новые заявки заявки'))
kb_sotrudnik3 = types.KeyboardButton(text='3. Все назначеные заявки')
kb_sotrudnik4 = types.KeyboardButton(text='4. Стоп')
keyboard_sotrudnik.add(kb_sotrudnik3,kb_sotrudnik4)

keyboard_menu = types.ReplyKeyboardMarkup()
keyboard_menu = types.ReplyKeyboardMarkup(row_width=0.1,resize_keyboard=True)
kb_menu1 = types.KeyboardButton(text='/Зарегистрироваться')
kb_menu2 = types.KeyboardButton(text='/Подать заявку')
keyboard_menu.add( kb_menu1, kb_menu2)
#@dp.message_handler(text= ["Завершена"], state=None)
# async def gotovo(message: types.Message, state: FSMContext):
#     cur.execute("UPDATE zaivka SET status = 'Завершена' WHERE id = (SELECT id FROM zaivka WHERE status = 'Новая_заявка' ORDER BY id ASC LIMIT 1)")


def get_menu_kb() -> ReplyKeyboardMarkup():
        kb = ReplyKeyboardMarkup(keyboard = [
                [KeyboardButton(text='/Зарегистрироваться'),
                 KeyboardButton(text='/Подать заявку')]
                ],resize_keyboard=True)

        return kb


def get_cancel_kb() -> ReplyKeyboardMarkup():
        kb = ReplyKeyboardMarkup(keyboard = [
                [KeyboardButton('/cancel')]
        ],resize_keyboard=True)

        return kb

def get_delete_kb() -> ReplyKeyboardMarkup():
        kb = ReplyKeyboardMarkup(keyboard = [
                [KeyboardButton('/delete')]
        ],resize_keyboard=True)

        return kb

def delete_kb() -> ReplyKeyboardMarkup():
        kb = ReplyKeyboardMarkup(keyboard = [
                [KeyboardButton('Пользователя'),
                  KeyboardButton('Заявку')]
        ],resize_keyboard=True)

        return kb