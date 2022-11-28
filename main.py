from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import KeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
import sqlite3 as sq

id_fb = 100000

storage = MemoryStorage()
proxy_url = "http://proxy.server:3128"
bot  = Bot(token="5824248980:AAFZYeSJ7rVfeaybrQ0N4TWqnxoR9jpwufY",proxy=proxy_url)                                      #Сюда нужно вставить токен бота
dp = Dispatcher(bot, storage=storage)

"""
class gl_station(StatesGroup):
    mesh = State()
    info = State()
@dp.message_handler(state=Tele.accept)
async def tele1(message: types.Message, state:FSMContext):
"""

b1 = KeyboardButton("Русский")
b2 = KeyboardButton("Қазақ")
kb_lang = ReplyKeyboardMarkup(resize_keyboard=True)
kb_lang.add(b1).insert(b2)
"""@dp.message_handler()
async def test(mes:types.Message):
    print(mes)"""
async def SEND (leng, id, textru, textkz, mark1=False, mark2=False):
    if mark1:
        if not mark2:
            mark2 = mark1
        if not leng:
            await bot.send_message(id, textru, reply_markup=mark1)
        elif leng:
            await bot.send_message(id, textkz, reply_markup=mark2)
    else:
        if not leng:
            await bot.send_message(id, textru)
        elif leng:
            await bot.send_message(id, textkz)

async def CEND (call, textru, textkz, mark1=False, mark2=False):
    print(call.from_user.id)
    leng = cur.execute("SELECT lang FROM register WHERE user_id == (?)", (call.from_user.id,)).fetchall()[0][0]
    if mark1:
        if not mark2:
            mark2 = mark1
        if not leng:
            await call.message.answer(textru, reply_markup=mark1)
        elif leng:
            await call.message.answer(textkz, reply_markup=mark2)
    else:
        if not leng:
            await call.message.answer(textru)
        elif leng:
            await call.message.answer(textkz)
    await call.answer()

async def DEND (call, textru, textkz):
    print(call.from_user.id)
    leng = cur.execute("SELECT lang FROM register WHERE user_id == (?)", (call.from_user.id,)).fetchall()[0][0]
    if not leng:
        await call.message.answer_document(open(textru,"rb"))
    elif leng:
        await call.message.answer_document(open(textkz,"rb"))
    await call.answer()



pre_reg = {}
class Lang_station(StatesGroup):
    lang = State()
    register_mail = State()
    register_phone = State()
    register_name = State()
    commit = State()

async def feedback(message,c):
    global id_fb
    id_fb += 1
    cur.execute("INSERT INTO fb VALUES (?,?)",(message.from_user.id, id_fb))
    con.commit()
    country = {"0":"-822291972","1":"","2":""}                                                          #сюда вставить id каналов
    await bot.send_message(int(country[str(c)]),f"Вопрос номер: {id_fb} \n\n {message.text}")

class Answer(StatesGroup):
    ans = State()

@dp.message_handler(state=Answer.ans)
async def feedback1(message:types.Message,state:FSMContext):
    mes = message.text
    id = mes[:len(str(id_fb))]
    mes = mes[len(str(id_fb))+1:]
    id_user = cur.execute("SELECT id_user FROM fb WHERE id_req == ?", (int(id), )).fetchall()[0][0]
    cur.execute("DELETE FROM fb WHERE id_req == (?)",(int(id),))
    print(id,mes,id_user,999)
    a = cur.execute("SELECT lang FROM register WHERE user_id == (?)", (id_user,)).fetchall()[0][0]
    print(1234213)
    con.commit()
    try:
        await SEND(a, id_user, f"Ваш ответ на вопрос номер {id}\n\n{mes}",f"Сұраққа сіздің жауап нөмірі {id}\n\n{mes}")
    except Exception as P:
        print(P)
    print(123)
    await General.general.set()


@dp.message_handler(commands=["start","hey","ans"],state="*")
async def starter(message:types.Message):
    if message.get_command() == "/ans":
        print("AAASNNNSNS")
        m = message.text.split()
        id = m[1]
        mes = m[2]
        id_user = cur.execute("SELECT id_user FROM fb WHERE id_req == ?", (int(id),)).fetchall()[0][0]
        cur.execute("DELETE FROM fb WHERE id_req == (?)", (int(id),))
        print(id, mes, id_user, 999)
        a = cur.execute("SELECT lang FROM register WHERE user_id == (?)", (id_user,)).fetchall()[0][0]
        print(1234213)
        con.commit()
        try:
            await SEND(a, id_user, f"Ваш ответ на вопрос номер {id}\n\n{mes}",
                       f"Сұраққа сіздің жауап нөмірі {id}\n\n{mes}")
        except Exception as P:
            print(P)
        print(123)
        await General.general.set()
    else:
        print(1)
        a = cur.execute("SELECT lang, mail FROM register WHERE user_id == (?)", (message.from_user.id,)).fetchall()
        c = True
        print(message.from_user.id)
        print(len(a))
        if len(a) == 0:
            c = False
            await bot.send_message(message.from_user.id, "Выберите язык / Тілді таңдаңыз", reply_markup=kb_lang)
            await Lang_station.lang.set()
        print(a)
        if c:
            if a[0][1] != "0" and c:
                await SEND(a[0][0],message.from_user.id, "Вы уже зарегестрированны","Сіз қазірдің өзінде тіркелдіңіз",mark1=kb_home_ru,mark2=kb_home_kz)
                await General.general.set()
            else:
                print(1.1)
                await SEND(a[0][0], message.from_user.id, "Введите свою почту", "Поштаны енгізіңіз", types.ReplyKeyboardRemove())
                await Lang_station.register_mail.set()

@dp.message_handler(state=Lang_station.lang)
async def starter_lang(message:types.Message, state: FSMContext):
    print(2)
    l = -1
    if message.text == "Русский":
        l = 0
    elif message.text == "Қазақ":
        l = 1
    else:
        await SEND(l,message.from_user.id, "Вы неправильно написали язык", "Сіз тілді қате жаздыңыз")

    cur.execute("INSERT INTO register VALUES (0, 0, 0, ?, ?)", (message.from_user.id, l))
    con.commit()
    if l==0:
        await bot.send_message(message.from_user.id, "Введите свою почту почту", reply_markup=types.ReplyKeyboardRemove())
        await Lang_station.next()
    elif l==1:
        await bot.send_message(message.from_user.id, "Поштаны енгізіңіз", reply_markup=types.ReplyKeyboardRemove())
        await Lang_station.next()

@dp.message_handler(state=Lang_station.register_mail)
async def starter_reg1(message:types.Message, state:FSMContext):
    print(3)
    a = cur.execute("SELECT lang FROM register WHERE user_id == (?)",(message.from_user.id,)).fetchall()[0][0]
    global pre_reg
    pre_reg[message.from_user.id] = []
    acc = True
    for i in message.text:
        if not i.isascii():
            acc = False
            break

    if "@" not in message.text and acc == True:
        acc = False
    if acc:
        pre_reg[message.from_user.id].append(message.text)
        await SEND(a,message.from_user.id, "Введите номер телефона","Телефон нөмірін енгізіңіз")
        await Lang_station.next()
    else:
        await SEND(a, message.from_user.id, "Вы неверно ввели почту", "Сіз поштаны қате енгіздіңіз")
@dp.message_handler(state=Lang_station.register_phone)
async def starter_reg2(message:types.Message, state:FSMContext):
    print(4)
    a = cur.execute("SELECT lang FROM register WHERE user_id == (?)", (message.from_user.id,)).fetchall()[0][0]
    global pre_reg
    message.text = message.text.replace(" ","").replace("(","").replace(")","").replace("-","")
    if "+" == message.text[0]:
        try:
            message.text = f"{int(message.text[1])+1}{message.text[2:]}"
        except:
            print("error number")
            await SEND(a, message.from_user.id, "Вы неверно ввели номер", "Сіз нөмірді қате енгіздіңіз")
    acc = True
    for i in message.text:
        if i != " ":
            try:
                int(i)
            except Exception as P:
                acc = False
                print(P)
                break
    if acc:
        pre_reg[message.from_user.id].append(int(message.text))
        await SEND(a, message.from_user.id, "Введите фамилию и имя", "Тегі мен атын енгізіңіз")
        await Lang_station.next()
    else:
        print("error number")
        await SEND(a, message.from_user.id, "Вы неверно ввели номер", "Сіз нөмірді қате енгіздіңіз")

wordss = "abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюяаеқпфъәёлрхыбжмсһівзнтцьгиңучэғйоұшюдкөүщя "

b1 = KeyboardButton("Подтвердить")
b2 = KeyboardButton("Изменить")
kb_acc_ru = ReplyKeyboardMarkup(resize_keyboard=True)
kb_acc_ru.add(b1).insert(b2)
b1 = KeyboardButton("Растау")
b2 = KeyboardButton("Өзгерту")
kb_acc_kz = ReplyKeyboardMarkup(resize_keyboard=True)
kb_acc_kz.add(b1).insert(b2)

@dp.message_handler(state=Lang_station.register_name)
async def starter_reg3(message:types.Message, state:FSMContext):
    a = cur.execute("SELECT lang FROM register WHERE user_id == (?)", (message.from_user.id,)).fetchall()[0][0]
    global pre_reg
    acc = True
    for i in message.text.lower():
        if i not in wordss:
            acc = False
            break
    if acc:
        pre_reg[message.from_user.id].append(message.text)
        await SEND(a, message.from_user.id, "Проверьте данные для регистрации, если что-то указано неверно - нажмите 'изменить' и пройдите регистрацию заново, если всё верно - нажмите 'подтвердить'",\
                   "Егер бірдеңе дұрыс көрсетілмесе, тіркеу үшін деректерді тексеріңіз - 'өзгерту' түймесін басып, қайта тіркеліңіз, егер бәрі дұрыс болса - 'растау' түймесін басыңыз")
        formkz = ["mail","Телефон нөмірі", "Аты-жөні"]
        texkz = "\n".join([f"{formkz[i]} - {pre_reg[message.from_user.id][i]}" for i in range(3)])
        formru = ["mail", "Номер телефона", "Имя и фамилия"]
        texru = "\n".join([f"{formru[i]} - {pre_reg[message.from_user.id][i]}" for i in range(3)])
        await SEND(a, message.from_user.id, texru, texkz, mark1=kb_acc_ru, mark2=kb_acc_kz)
        await Lang_station.next()
    else:
        await SEND(a, message.from_user.id, "Замечены недопустимые символы при вводе имени или фамилии\n Попробуйте заново", "Аты немесе ТЕГІН енгізу кезінде жол берілмейтін таңбалар байқалды\n Қайта көріңіз(кз)")


b1 = KeyboardButton("Обратная связь")

b2 = KeyboardButton("Сменить язык")
kb_home_ru = ReplyKeyboardMarkup(resize_keyboard=True)
kb_home_ru.add(b1).add(b2)

b1 = KeyboardButton("Кері байланыс")

b2 = KeyboardButton("Тілді ауыстыру")
kb_home_kz = ReplyKeyboardMarkup(resize_keyboard=True)
kb_home_kz.add(b1).add(b2)



@dp.message_handler(state=Lang_station.commit)
async def starter_reg(message:types.Message, state:FSMContext):
    a = cur.execute("SELECT lang FROM register WHERE user_id == (?)", (message.from_user.id,)).fetchall()
    if message.text == "Подтвердить" or message.text == "Растау":
        data = pre_reg[message.from_user.id]
        print(data)
        cur.execute("UPDATE register SET mail = (?), phone = (?), name = (?) WHERE user_id = (?)", (data[0], data[1], data[2], message.from_user.id))
        con.commit()
        await SEND(a[0][0], message.from_user.id, "Вы успешно зарегистрировались!", "сіз сәтті тіркелдіңіз!",mark1=kb_home_ru,mark2=kb_home_kz)
        await General.general.set()

    else:
        await SEND(a[0][0], message.from_user.id, "Введите свою почту почту", "Поштаны енгізіңіз",types.ReplyKeyboardRemove())
        await Lang_station.register_mail.set()

class General(StatesGroup):
    general = State()
    hub = State()
    step = State()
    vip = State()
    cont = State()


b1 = KeyboardButton("Bolashaq News")
b2 = KeyboardButton("Межправительственные гранты")
b3 = KeyboardButton("Обратная связь")
b4 = KeyboardButton("Контакты")
b5 = KeyboardButton("Претенденту")
b6 = KeyboardButton("Назад")
kb_hub_ru = ReplyKeyboardMarkup(resize_keyboard=True)
kb_hub_ru.add(b5).add(b1).insert(b2).add(b3).insert(b4).add(b6)

b1 = KeyboardButton("Написать куратору")
b2 = KeyboardButton("Образцы документов")
b3 = KeyboardButton("FAQ")
b4 = KeyboardButton("Все о финансировании")
b5 = KeyboardButton("Оформление визы")
b7 = KeyboardButton("Замена залога")
b8 = KeyboardButton("Заключение договора на обучение и стажировку")
b6 = KeyboardButton("Назад")
kb_step_ru = ReplyKeyboardMarkup(resize_keyboard=True)
kb_step_ru.add(b1).add(b3).insert(b4).add(b5).insert(b2).add(b7).add(b8).add(b6)


b1 = KeyboardButton("Кураторға жазу")
b2 = KeyboardButton("Құжат үлгілері")
b3 = KeyboardButton("FAQ")
b4 = KeyboardButton("Қаржыландыру туралы")
b5 = KeyboardButton("Визаны  рәсімдеу")
b7 = KeyboardButton("кепілді ауыстыру")
b8 = KeyboardButton("оқу және тағылымдамадан өту шартын жасау")
b6 = KeyboardButton("Қайтып оралу")
kb_step_kz = ReplyKeyboardMarkup(resize_keyboard=True)
kb_step_kz.add(b1).add(b3).insert(b4).add(b5).insert(b2).add(b7).add(b8).add(b6)

b1 = KeyboardButton("Трудовая отработка")
b2 = KeyboardButton("Расчет трудовой отработки")
b3 = KeyboardButton("Узнать куратора")
b4 = KeyboardButton("Формы заявлений")
b5 = KeyboardButton("Замена залога")
b6 = KeyboardButton("Трудоустройство")
b7 = KeyboardButton("Справка о статусе выпускника")
b9 = KeyboardButton("Снятие обременения с недвижимого имущества")
b8 = KeyboardButton("Назад")
kb_vip_ru = ReplyKeyboardMarkup(resize_keyboard=True)
kb_vip_ru.add(b1).insert(b2).add(b3).insert(b4).add(b5).insert(b6).add(b7).add(b9).add(b8)


class General(StatesGroup):
    general = State()
    hub = State()
    step = State()
    vip = State()
    cont = State()
    not_general = State()


async def to_home(message):
    if message.text == "Назад" or message.text == "Қайтып оралу":
        a = cur.execute("SELECT lang FROM register WHERE user_id == (?)", (message.from_user.id,)).fetchall()[0][0]
        await SEND(a, message.from_user.id, "Вы перемещены в главное меню","Сіз негізгі мәзірге ауысасыз",mark1=kb_home_ru,mark2=kb_home_kz)
        await General.general.set()

class ChangeL(StatesGroup):
    step1 = State()




@dp.message_handler(state=General.general)
async def home(message:types.Message, state:FSMContext):
    a = cur.execute("SELECT lang FROM register WHERE user_id == (?)", (message.from_user.id,)).fetchall()[0][0]
    if message.text == "Главная":
        await SEND(a, message.from_user.id, "Основная информация","Негізгі ақпарат",mark1=kb_hub_ru)
        await General.hub.set()
    if message.text == "Обратная связь" or message.text == "Кері байланыс":
        await SEND(a, message.from_user.id, "Написать обращение","Өтініш жазу")
        await message.answer("перетащите файл сюда...")
    if message.text == "Сменить язык" or message.text == "Тілді ауыстыру":
        await SEND(a, message.from_user.id, "Выберите язык","Тілді таңдаңыз", mark1=kb_lang)
        await ChangeL.step1.set()
@dp.message_handler(state=ChangeL.step1)
async def changeL(message:types.Message, state:FSMContext):
    if message.text == "Русский":
        cur.execute("UPDATE register SET lang = 0 WHERE user_id == (?)",(message.from_user.id,))
        await message.reply("Вы успешно сменили язык",reply_markup=kb_home_ru)
        await General.general.set()
    elif message.text == "Қазақ":
        await message.reply("Сіз тілді сәтті өзгерттіңіз", reply_markup=kb_home_kz)
        cur.execute("UPDATE register SET lang = 1 WHERE user_id == (?)",(message.from_user.id, ))
        await General.general.set()
    con.commit()


@dp.message_handler(state='*',content_types=["text", "photo"])
async def answer_question(message:types.Message,state:FSMContext):

    if message.photo is not None:
        await bot.send_photo(
            '-822291972',
            message.photo[-1].file_id,
            message.caption,
        )




@dp.message_handler(state=General.hub)
async def hubb(message:types.Message, state:FSMContext):
    a = cur.execute("SELECT lang FROM register WHERE user_id == (?)", (message.from_user.id,)).fetchall()[0][0]
    await to_home(message)


b1 = KeyboardButton("Отмена")
kb_c = ReplyKeyboardMarkup(resize_keyboard=True)
kb_c.add(b1)

b1 = KeyboardButton("болдырмау")
kb_c_kz = ReplyKeyboardMarkup(resize_keyboard=True)
kb_c_kz.add(b1)



con = sq.connect("mkdb.db")
cur = con.cursor()
executor.start_polling(dp, skip_updates=True)