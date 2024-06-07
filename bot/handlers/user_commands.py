from aiogram.filters import CommandStart, Command
from aiogram.filters.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram import types, Router, Bot
from aiogram.types.input_media_photo import InputMediaPhoto
from aiogram.utils.media_group import MediaGroupBuilder
from replics.get_replic import get_text
from inline_buttons.buttons import greeteng_actions_list, main_menu_actions_list, return_actions_list, get_answers_list
import sys
import os

sys.path.append(f'{os.environ.get("PWD")}/..')

from data2.train.get import get_data_predict
from data2.train.send import send_data_predict


router = Router()

regions_list = ["МСК", "Центр", "СЗ", "НН", "Юг", "Урал", "Сиб", "ДВ"]
region = ''
get_list = []
send_list = []

class Dialog(StatesGroup):
    main = State()
    region = State()
    get_data = State()
    send_data = State()
    answer = State()
    prediction_error = State()
    prediction_success = State()

@router.message(CommandStart())
async def start_message(message: types.Message, state: FSMContext):
    await state.set_state(Dialog.main)
    await message.answer(get_text(text_name="greeting"), reply_markup=greeteng_actions_list)

@router.message(Command("help", prefix="!/"))
async def help_message(message: types.Message):
    await message.answer(get_text(text_name="help"))

@router.message(Dialog.main)
async def main_menu(message: types.Message, state: FSMContext):
    await state.set_state(Dialog.region)
    await message.answer(get_text(text_name="main"), reply_markup=main_menu_actions_list)

@router.message(Dialog.region)
async def get_region(message: types.Message, state: FSMContext):
    global region
    if message.text == "Главное меню":
        await state.set_state(Dialog.main)
        await main_menu(message=message, state=state)
        # await message.answer(get_text(text_name="return"))
    elif message.text not in regions_list :
        await state.set_state(Dialog.main)
        await message.answer(get_text(text_name="region_error"))
    else:
        region = message.text
        await state.set_state(Dialog.get_data)
        await message.answer(get_text(text_name="get_data"), reply_markup=return_actions_list)

@router.message(Dialog.get_data)
async def get_data(message: types.Message, state: FSMContext):
    global get_list
    if message.text == "Главное меню":
        await state.set_state(Dialog.main)
        await main_menu(message=message, state=state)
    else:
        try:
            get_list = [int(x) for x in message.text.split(" ")]
        except Exception:
            await message.answer(get_text(text_name="get_data_error"))
        await state.set_state(Dialog.send_data)
        await message.answer(get_text(text_name="send_data"), reply_markup=return_actions_list)

@router.message(Dialog.send_data)
async def send_data(message: types.Message, state: FSMContext):
    global send_list
    if message.text == "Главное меню":
        await state.set_state(Dialog.main)
        await main_menu(message=message, state=state)
    else:
        try:
            send_list = [int(x) for x in message.text.split(" ")]
        except Exception:
            await message.answer(get_text(text_name="send_data_error1"))
        if len(get_list) != len(send_list):
            await message.answer(get_text(text_name="send_data_error2"))
        await state.set_state(Dialog.answer)
        await answer(message=message, state=state)
        
@router.message(Dialog.answer)
async def answer(message: types.Message, state: FSMContext):
    await get_data_predict(region, get_list)
    await send_data_predict(region, send_list)
    await state.set_state(Dialog.prediction_success)
    await message.answer(get_text(text_name="success_prediction"), reply_markup=get_answers_list)



@router.message(Dialog.prediction_success)
async def answer_check(message: types.Message, state: FSMContext):
    if message.text == "Главное меню":
        await state.set_state(Dialog.main)
        await main_menu(message=message, state=state)
    elif message.text == "Получить число для получения":
        await message.answer("Число для получения")
    elif message.text == "Получить число для отправки":
        await message.answer("Число для отправки")
    elif message.text == "Получить график для получения":
        await message.answer_photo(photo=types.FSInputFile(path="get2.png"))
    elif message.text == "Получить график для отправки":
        await message.answer_photo(photo=types.FSInputFile(path="send2.png"))
    else:
        await message.answer(get_text(text_name="answer_check_error"))
