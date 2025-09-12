#!venv/bin/python
import logging
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, callback_query
import asyncio
import time
import requests
import sqlite3
from markup import *
from config import token
from aiogram.dispatcher import filters

from aiogram.dispatcher.filters import Command
from aiogram.types import Message



class FSMAdmin(StatesGroup):
    kafedra = State()
    kabinet = State()
    name = State()
    surname = State()
    refactor_kafedra = State()
    refactor_kabinet = State()
    refactor_name = State()
    refactor_surname = State()
    mark_data = State()
    date_time = State()
    text = State()
    nomer = State()
    kabinet2 = State()
    add = State()
storage = MemoryStorage()


bot = Bot(token)# Объект бота
dp = Dispatcher(bot, storage=storage)# Диспетчер для бота
logging.basicConfig(level=logging.INFO)# Включаем логирование, чтобы не пропустить важные сообщения



#*****************************************************************************************************************************************************************************************
@dp.message_handler(commands=["start"])
async def command_start(message: types.Message):
    sotrudnik = await sotrudnik_id()
    admin = await admin_id()
    print(sotrudnik, admin)
    print(message.from_user.id)
    if str(message.from_user.id) == sotrudnik:
        # Если пользователь с id сотрудника, отправляем ему специальную клавиатуру
        await message.answer("Добрый день!, вас приветствует отдел технического обслуживания", reply_markup=keyboard_sotrudnik)
    elif str(message.from_user.id) ==  admin:
        # Если пользователь с id администратора, отправляем ему специальную клавиатуру
        await message.answer("Добрый день!, вас приветствует отдел технического обслуживания", reply_markup=keyboard_admin)
    else:
        # Иначе отправляем общую клавиатуру для всех
        await message.answer("Добрый день!, вас приветствует отдел технического обслуживания", reply_markup=get_menu_kb())

#*****************************************************************************************************************************************************************************************
@dp.message_handler(commands= ["add"])
async def command_add(message: types.Message):
    await message.answer('Напишите Фамилию и имя сотрудника')
    await FSMAdmin.add.set()

@dp.message_handler(state=FSMAdmin.add)
async def command_add(message: types.Message,state: FSMContext):
    async with state.proxy() as data:
        data["add"] = message.text.split()
        add = data["add"]
        print(add)
        name = add[0]
        surname = add[1]
        cur.execute("UPDATE users SET right='Сотрудник' WHERE name =? AND surname =?", (name, surname,))
        await message.answer(f"Сотрудник {add}, добавлен")

@dp.message_handler(commands=["Зарегистрироваться"], state="*")
async def command_b1vpr1_1(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    result = await user_is_not_none(user_id)
    if result == True:
        await message.answer('Введите кафедру')
        await FSMAdmin.kafedra.set()
    if result == False:
        await message.answer('Вы уже проходили регистрацию!', reply_markup=keyboard_menu)


@dp.message_handler(content_types=['text'],state=FSMAdmin.kafedra)
async def kafedra(message: types.Message, state: FSMContext):
    print('1')
    async with state.proxy() as data:
        data['kafedra'] = message.text
        await FSMAdmin.next()
        await message.answer('Введите кабинет')


@dp.message_handler(content_types=['text'],state=FSMAdmin.kabinet)
async def kabinet(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['kabinet'] = message.text
        await FSMAdmin.next()
        await message.answer('Введите имя')


@dp.message_handler(content_types=['text'],state=FSMAdmin.name)
async def name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
        await FSMAdmin.next()
        await message.answer('А теперь введите фамилию')


@dp.message_handler(content_types=['text'], state=FSMAdmin.surname)
async def surname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['surname'] = message.text
    async with state.proxy() as data:
        kafedra = data['kafedra']
        kabinet = data['kabinet']
        name = data['name']
        surname = data['surname']
        user_id = message.from_user.id
        cur.execute(f'''SELECT id FROM users WHERE id_user = {user_id}''')
        data = cur.fetchone()
        if data is None:
            stud_id = message.from_user.id
            cur.execute('INSERT INTO users (id_user,kafedra,kabinet,name,surname) VALUES(?,?,?,?,?)', (stud_id, kafedra,kabinet,name, surname))
            await message.answer("Регистрация прошла успешно!", reply_markup=keyboard_menu)
        base.commit()


#*****************************************************************************************************************************************************************************************
@dp.message_handler(commands=['cancel'], state='*')
async def cmd_cancel(message: types.Message,state: FSMContext):
    if state is None:
        return

    await state.finish()
    sotrudnik = await sotrudnik_id()
    admin = await admin_id()
    if str(message.from_user.id) == sotrudnik:
        # Если пользователь с id сотрудника, отправляем ему специальную клавиатуру
        await message.answer('Вы отменили действие!', reply_markup=keyboard_sotrudnik)
    elif str(message.from_user.id) ==  admin:
        # Если пользователь с id администратора, отправляем ему специальную клавиатуру
        await message.answer('Вы отменили действие!', reply_markup=keyboard_admin)
    else:
        await message.answer('Вы отменили действие!')
#*****************************************************************************************************************************************************************************************
class Delete(StatesGroup):
    wait_for_name = State()
    wait_for_zaivka = State()

@dp.message_handler(filters.IDFilter(user_id=5373281109), Command('delete'))
async def delete_row(message: types.Message, state: FSMContext):
    await message.answer('Что удалить?', reply_markup=delete_kb())
    async with state.proxy() as data:
        data['wait_for_name'] = True
    await Delete.wait_for_name.set()


@dp.message_handler(filters.IDFilter(user_id=5373281109), state=Delete.wait_for_name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if data.get('wait_for_name'):
            await message.answer("Напишите имя и фамилию пользователя\n"
                             "Пример: <<Савельев Олег>>")
            data['wait_for_name'] = False
        else:
            name_surname = message.text.split()
            if len(name_surname) == 2:
                name = name_surname[0]
                surname = name_surname[1]
                print(name, surname)
                cur.execute("DELETE FROM users WHERE name = ? AND surname = ?", (name, surname,))
                if cur.rowcount > 0:
                    await message.answer(f"Пользователь {name} {surname} удален")
                    await state.finish()
                    base.commit()
                else:
                    await message.answer(f"Пользователь {name} {surname} не найден")
                await state.finish()
                base.commit()
            else:
                await message.answer("Ошибка: неверный формат имени и фамилии")
                await state.finish()
                base.commit()

@dp.message_handler(filters.IDFilter(user_id=5373281109),state=Delete.wait_for_zaivka)
async def process_zaivka(message: types.Message, state: FSMContext):
    admin_id_value = await admin_id()
    count = await count_new_zaivki()
    if message.text == '2. Смотреть новые заявки' and count != 0:
        count = await count_new_zaivki()
        cur.execute("SELECT *, ROW_NUMBER() OVER(ORDER BY id) AS row_number FROM zaivka WHERE sotrudnik = 'Неназначен' AND status = 'Новая_заявка'")
        rows = cur.fetchall()
        print(rows)
        for row in rows:
            user_id = row[1]
            date_time = row[2]
            text = row[3]
            nomer_zaivki = row[7]
            print(nomer_zaivki)
            await bot.send_message(admin_id_value,
                                       f'Номер заявки № {nomer_zaivki}\nНовая заявка от пользователя {user_id}:\n{date_time}\n{text}')
        await message.answer('Введите номер заявки, которую хотите удалить', reply_markup=get_cancel_kb())
    base.commit()

@dp.message_handler(commands=['profil'])
async def profil(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    print(user_id)
    cur.execute("SELECT * FROM users WHERE id_user=?", (user_id,))
    result = cur.fetchone()
    print(result)
    if result is not None:
        output_string  =  f"Пользователь: {result[4]} {result[5]}\n\n" \
                                    f"Кафедра: {result[2]}\n\n" \
                                    f"Кабинет: {result[3]}"
        await message.answer(output_string)
    base.commit()
    await state.finish()


@dp.message_handler(Command('refactor'), state=None)
async def refactor_start(message: Message, state: FSMContext):
    await message.answer('Введите имя')
    await FSMAdmin.refactor_name.set()

@dp.message_handler(content_types=['text'], state=FSMAdmin.refactor_name)
async def refactor_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['refactor_name'] = message.text
        await FSMAdmin.next()
        await message.answer('Введите фамилию')

@dp.message_handler(content_types=['text'], state=FSMAdmin.refactor_surname)
async def refactor_surname(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['refactor_surname'] = message.text
        # await FSMAdmin.next()
        await FSMAdmin.refactor_kafedra.set()
        await message.answer('Введите кафедру')

@dp.message_handler(content_types=['text'], state=FSMAdmin.refactor_kafedra)
async def refactor_kafedra(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['refactor_kafedra'] = message.text
        await FSMAdmin.next()
        await message.answer('Введите кабинет')

@dp.message_handler(content_types=['text'], state=FSMAdmin.refactor_kabinet)
async def refactor_kabinet(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['refactor_kabinet'] = message.text
        name = data['refactor_name']
        surname = data['refactor_surname']
        kafedra = data['refactor_kafedra']
        kabinet = data['refactor_kabinet']
        user_id = message.from_user.id
        cur.execute(f"SELECT id FROM users WHERE id_user = {user_id}")
        data = cur.fetchone()
        cur.execute("UPDATE users SET name = ?, surname = ?, kafedra = ?, kabinet = ?  WHERE id_user=?", (name, surname, kafedra, kabinet, user_id,))
        await message.answer("Настройки применены")
        base.commit()
        await state.finish()

#*****************************************************************************************************************************************************************************************

@dp.message_handler(commands=["/Подать заявку"], state='*')
async def command_z(message: types.Message, state: FSMContext):
    sotrudnik = await sotrudnik_id()
    admin_id_value = await admin_id()
    if str(message.from_user.id) == sotrudnik and admin_id_value:
        print('False')
    else:
        user_id = message.from_user.id
        cur.execute(f'''SELECT id FROM zaivka WHERE id_user = {user_id}''')
        data = cur.fetchone()
        await message.answer('Введите текст')
        await state.set_state("FSMAdmin:text")

@dp.message_handler(content_types=['text'], state=FSMAdmin.text)
async def text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        await FSMAdmin.kabinet2.set()
        await message.answer('Кабинет')


@dp.message_handler(content_types=['text'], state=FSMAdmin.kabinet2)
async def kabinet2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['kabinet2'] = message.text
    async with state.proxy() as data:
        named_tuple = time.localtime()
        data['date_time'] = time.strftime("%m.%d.%Y, %H:%M:%S", named_tuple)
    async with state.proxy() as data:
        date_time = data['date_time']
        text = data['text']
        kabinet = data['kabinet2']
        user_id = message.from_user.id
        cur.execute(f'''SELECT id FROM zaivka WHERE id_user = {user_id}''')
        data = cur.fetchone()
        stud_id = message.from_user.id
        cur.execute('INSERT INTO zaivka (id_user,date_time, text, kabinet) VALUES(?,?,?,?)', (stud_id, date_time, text, kabinet))
        base.commit()
        await message.answer("Заявка прошла успешно!")
        count = await count_new_zaivki()
        admin_id_value = await admin_id()
        await bot.send_message(admin_id_value, f"Накопилось {count} новых заявок", reply_markup=keyboard_admin)
        base.commit()
        await state.finish()

#*****************************************************************************************************************************************************************************************


@dp.message_handler(state='*')
async def message_menu(message: types.Message, state: FSMContext):
    admin_id_value = await admin_id()
    count = await count_new_zaivki()
    count_vpl = await  count_vpl_zaivk()
    # тут преобразуется объект message.from_user.id в строку иначе условие не выполняется
    if str(message.from_user.id) == admin_id_value:
        if message.text == '1. Посмотреть' and count != 0:
            cur.execute("SELECT * FROM zaivka WHERE sotrudnik ='Неназначен' AND status='Новая_заявка' ORDER BY id ASC LIMIT 1")
            rows = cur.fetchall()
            for row in rows:
                user_id = row[1]
                date_time = row[2]
                text = row[3]
                await bot.send_message(admin_id_value, f'Новая заявка от пользователя {user_id}:\n{date_time}\n{text}',reply_markup=keyboard)
            base.commit()
        elif message.text == '2. Смотреть новые заявки' and count != 0:
            count = await count_new_zaivki()
            if count == 1:
                cur.execute(
                        "SELECT *, ROW_NUMBER() OVER(ORDER BY id) AS row_number FROM zaivka WHERE sotrudnik = 'Неназначен' AND status = 'Новая_заявка'")
                rows = cur.fetchall()
                for row in rows:
                    user_id = row[1]
                    date_time = row[2]
                    text = row[3]
                    nomer_zaivki = row[6]
                    await bot.send_message(admin_id_value,f'Номер заявки № {nomer_zaivki}\nНовая заявка от пользователя {user_id}:\n{date_time}\n{text}', reply_markup=keyboard)
                base.commit()
            else:
                cur.execute(
                    "SELECT *, ROW_NUMBER() OVER(ORDER BY id) AS row_number FROM zaivka WHERE sotrudnik = 'Неназначен' AND status = 'Новая_заявка'")
                rows = cur.fetchall()
                print(rows)
                for row in rows:
                    user_id = row[1]
                    date_time = row[2]
                    text = row[3]
                    nomer_zaivki = row[7]
                    print(nomer_zaivki)
                    await bot.send_message(admin_id_value,f'Номер заявки № {nomer_zaivki}\nНовая заявка от пользователя {user_id}:\n{date_time}\n{text}')
                await message.answer('Введите номер заявки, которую хотите вывести',reply_markup=get_cancel_kb())
                await state.set_state('get_nomer_zaivki')
                await state.update_data(count=count)
                base.commit()
        elif message.text == '3. Все назначеные заявки' and count_vpl != 0:
            cur.execute("SELECT * FROM zaivka WHERE status = 'Выполняется' OR status = 'Новая_заявка' AND sotrudnik NOT IN ('Неназначен')")
            rows = cur.fetchall()
            print(rows)
            for row in rows:
                user_id = row[1]
                date_time = row[2]
                text = row[3]
                sotrudnik = row[4]
                status = row[6]
                cur.execute("SELECT name, surname FROM users WHERE id_user = ?", (user_id,))
                rows2 = cur.fetchall()
                for row2 in rows2:
                    name = row2[0]
                    print(name)
                    surname = row2[1]
                await bot.send_message(admin_id_value,f'Новая заявка от:  {name} {surname}:\n{date_time}\n{text}\nСотрудник: {sotrudnik}\nСтатус: {status}')

        elif message.text == '4. Список команд':
            await bot.send_message(admin_id_value,f'/delete - Удалить пользователя или заявку\n/cancel - Отменить действие\n/add - Добавить сотрудника\n/profil - Профиль\n/refactor - Изменить профиль')
        elif message.text == '5. Стоп':
            await message.answer('Стоп')
            base.commit()
            await state.finish()
        elif count == 0:
            await message.answer('Заявок нет ')
            await state.finish()
            base.commit()




    sotrudnik = await sotrudnik_id()
    count_str = await count_new_zaivki_str()
    print(count_str)
    # тут преобразуется объект message.from_user.id в строку иначе условие не выполняется
    if str(message.from_user.id) == sotrudnik:
        if message.text == '1. Посмотреть новые заявки' and count_str != 0:
            cur.execute("SELECT * FROM zaivka WHERE sotrudnik ='Олег Савельев' AND status='Новая_заявка' ORDER BY id ASC LIMIT 1")
            rows = cur.fetchall()
            for row in rows:
                user_id = row[1]
                date_time = row[2]
                text = row[3]
                await bot.send_message(sotrudnik, f'Новая заявка от пользователя {user_id}:\n{date_time}\n{text}',reply_markup=keyboard_gotovo)
                base.commit()
        elif message.text == '2. Смотреть все новые заявки заявки' and count_str != 0:
            cur.execute("SELECT *, ROW_NUMBER() OVER(ORDER BY id) AS row_number FROM zaivka WHERE sotrudnik = 'Олег Савельев' AND status = 'Новая_заявка'")
            rows = cur.fetchall()
            for row in rows:
                user_id = row[1]
                date_time = row[2]
                text = row[3]
                nomer_zaivki = row[7]
                await bot.send_message(sotrudnik,f'Номер заявки № {nomer_zaivki}\nНовая заявка от пользователя {user_id}:\n{date_time}\n{text}')
            await bot.send_message(sotrudnik, "Принять все заявки?", reply_markup=get_all_zaivki)
            count_str = await count_new_zaivki_str()
            await state.update_data(count_str=count_str)
            base.commit()
        elif message.text == '3. Все выполняющиеся заявки':
            cur.execute("SELECT *, ROW_NUMBER() OVER(ORDER BY id) AS row_number FROM zaivka WHERE sotrudnik = 'Олег Савельев' AND status = 'Выполняется'")
            rows = cur.fetchall()
            for row in rows:
                user_id = row[1]
                date_time = row[2]
                text = row[3]
                nomer_zaivki = row[7]
                await bot.send_message(sotrudnik,f'Номер заявки № {nomer_zaivki}\nНовая заявка от пользователя {user_id}:\n{date_time}\n{text}')
                count_done = await count_done_zaivki_count_vpl()
                await state.update_data(count_done=count_done)
            await message.answer('Введите номер заявки, которую хотите вывести',reply_markup=get_cancel_kb())
            await state.set_state('process_done_nomer_zaivki_sotrudnik')
            base.commit()
        elif message.text == '4. Стоп':
            await message.answer('Стоп')
            base.commit()
            await state.finish()
        elif count_str == 0:
            await message.answer('Заявок нет')
            await state.finish()
            base.commit()


# *****************************************************************************************************************************************************************************************

# Обработчик для состояния get_nomer_zaivki
@dp.message_handler(state='get_nomer_zaivki')
async def process_nomer_zaivki(message: types.Message, state: FSMContext):
    data = await state.get_data()
    count = data.get('count')
    nomer_zaivki = message.text
    print(message.text)
    if not nomer_zaivki.isdigit() or int(nomer_zaivki) < 1 or int(nomer_zaivki) > count:
        await message.answer('Введите корректный номер заявки',reply_markup=get_cancel_kb())
        return
    if message.text == 'Стоп':
        await message.answer('Стоп')
        await state.finish()
        base.commit()
    cur.execute(
        f"SELECT *, ROW_NUMBER() OVER (ORDER BY id) AS row_number FROM zaivka WHERE sotrudnik ='Неназначен' AND status='Новая_заявка' LIMIT 1 OFFSET {int(nomer_zaivki) - 1}")
    row = cur.fetchone()
    admin_id_value = await admin_id()
    if row is None:
        await message.answer('Заявка не найдена')
        return
    user_id = row[1]
    date_time = row[2]
    text = row[3]
    nomer_zaivki = row[7]
    await bot.send_message(admin_id_value, f'Номер заявки № {nomer_zaivki}\nНовая заявка от пользователя {user_id}:\n{date_time}\n{text}',
        reply_markup=keyboard)
    await state.finish()
    base.commit()


#*****************************************************************************************************************************************************************************************


nomer_zaivki_bd = None

@dp.message_handler(state='process_done_nomer_zaivki_sotrudnik')
async def process_done_nomer_zaivki_sotrudnik(message: types.Message, state: FSMContext):
    global nomer_zaivki_bd
    sotrudnik = await sotrudnik_id()
    data = await state.get_data()
    count_done = data.get('count_done')
    nomer_zaivki = message.text
    if not nomer_zaivki.isdigit() or int(nomer_zaivki) < 1 or int(nomer_zaivki) > count_done:
        await message.answer('Введите корректный номер заявки')
        return
    cur.execute(f"SELECT *, ROW_NUMBER() OVER (ORDER BY id) AS row_number FROM zaivka WHERE sotrudnik ='Олег Савельев' AND status='Выполняется' LIMIT 1 OFFSET {int(nomer_zaivki) - 1}")
    row = cur.fetchone()
    if row is None:
        await message.answer('Заявка не найдена')
        return
    user_id = row[1]
    date_time = row[2]
    text = row[3]
    nomer_zaivki = row[7]
    nomer_zaivki_bd =  nomer_zaivki
    await bot.send_message(sotrudnik,f'Номер заявки № {nomer_zaivki}\nНовая заявка от пользователя {user_id}:\n{date_time}\n{text}',reply_markup=keyboard_completed)
    await state.finish()
    base.commit()

#*****************************************************************************************************************************************************************************************


#Обработчик нажатия на кнопку "Олег Савельев"
@dp.callback_query_handler(lambda c: c.data == 'oleg')
async def oleg_callback(query: CallbackQuery):
    sotrudnik_name = "Олег Савельев"
    # задает в заявке име выполняещего ее
    cur.execute("UPDATE zaivka SET sotrudnik = ? WHERE id = (SELECT id FROM zaivka WHERE sotrudnik = 'Неназначен' ORDER BY id ASC LIMIT 1)",(sotrudnik_name,))

    cur.execute("SELECT COUNT(*) FROM zaivka WHERE sotrudnik ='Олег Савельев' AND status='Новая_заявка'")
    rows = cur.fetchall()
    for row in rows:
        count_ctr = row[0]
    # достает из бд id сотрудника
    sotrudnik = await sotrudnik_id()
    await bot.send_message(sotrudnik,f"Накопилось {count_ctr} новых заявок", reply_markup=keyboard_sotrudnik)
    base.commit()

#*****************************************************************************************************************************************************************************************


@dp.callback_query_handler(lambda c: c.data == 'oleg_sotr',)
async def process_vpl_new_zaivok(query: CallbackQuery):
    #await bot.answer_callback_query(callback_query.id, text='Заявка принята', show_alert=True)
    #message = await bot.send_message(chat_id=query.message.chat.id, text='Заявка принята')
    cur.execute("UPDATE zaivka SET status = 'Выполняется' WHERE id = (SELECT id FROM zaivka WHERE sotrudnik ='Олег Савельев' AND status='Новая_заявка' ORDER BY id ASC LIMIT 1)")
    base.commit()


@dp.callback_query_handler(lambda c: c.data == 'get_all_zaivki')
async def process_vpl_get_all_zaivki(query: CallbackQuery):
    cur.execute("UPDATE zaivka SET status = 'Выполняется' WHERE sotrudnik = 'Олег Савельев' AND status = 'Новая_заявка'")
    message = await bot.send_message(chat_id=query.message.chat.id, text='Заявки приняты')
    base.commit()


#*****************************************************************************************************************************************************************************************


@dp.callback_query_handler(lambda c: c.data == 'completed',)
async def process_completed_new_zaivok(query: CallbackQuery):
    nomer = nomer_zaivki_bd  # пример значения номера заявки
    cur.execute("UPDATE zaivka SET status = 'Выполнено' WHERE id = (SELECT id FROM(SELECT id, status, ROW_NUMBER() OVER(ORDER BY id) AS row_number FROM zaivka WHERE sotrudnik = 'Олег Савельев' AND status = 'Выполняется')  WHERE row_number = ?)", (nomer,))
    message = await bot.send_message(chat_id=query.message.chat.id, text='Заявка выполнена')
    base.commit()


#*****************************************************************************************************************************************************************************************

async def on_startup(_):
    await db_connect()
    print('SQL подключен')


async def admin_id():
    cur.execute("SELECT id_user FROM sotrudniki WHERE prava='admin'")
    result = cur.fetchone()
    admin_id = result[0]

    return admin_id


async def sotrudnik_id():
    cur.execute("SELECT id_user FROM sotrudniki WHERE prava='sotrudnik'")
    result = cur.fetchone()
    sotrudnik = result[0]

    return sotrudnik

async def count_new_zaivki():
    cur.execute("SELECT COUNT(*) FROM zaivka WHERE sotrudnik ='Неназначен' AND status='Новая_заявка'")
    result = cur.fetchone()
    count = result[0]

    return count


async def count_new_zaivki_str():
    cur.execute("SELECT COUNT(*) FROM zaivka WHERE sotrudnik ='Олег Савельев' AND status='Новая_заявка'")
    result = cur.fetchone()
    count_str = result[0]

    return count_str


async def count_done_zaivki_count_vpl():
    cur.execute("SELECT COUNT(*) FROM zaivka WHERE sotrudnik ='Олег Савельев' AND status='Выполняется'")
    result = cur.fetchone()
    count_done = result[0]

    return count_done


async def count_vpl_zaivk():
    cur.execute("SELECT COUNT(*) FROM zaivka WHERE status='Выполняется' OR status='Новая_заявка' AND sotrudnik NOT IN ('Неназначен')")
    result = cur.fetchone()
    count_vpl = result[0]

    return count_vpl

async def user_is_not_none(user_id):
    try:
        cur.execute(f"SELECT id FROM users WHERE id_user = {user_id}")
        data = cur.fetchone()
        if data is not None:
            return False
        else:
            return True
    except Exception as e:
        print(e)
        return False






async def db_connect() -> None:
    global base, cur

    base = sqlite3.connect('database.db')
    cur = base.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS zaivka("
                                "id INTEGER PRIMARY KEY, "
                                "id_user TEXT, "
                                "date_time TEXT, "
                                "text TEXT, "
                                "sotrudnik TEXT    DEFAULT 'Неназначен', "
                                "status TEXT    DEFAULT 'Новая_заявка'"
                                ");")

    cur.execute("CREATE TABLE IF NOT EXISTS users("
                                "id INTEGER PRIMARY KEY,"
                                "id_user TEXT,"
                                "kafedra TEXT,"
                                "kabinet TEXT,"
                                "name TEXT,"
                                "surname TEXT"
                                ");")

    base.commit()

#*****************************************************************************************************************************************************************************************
if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, timeout=50000, skip_updates=True, on_startup=on_startup)
