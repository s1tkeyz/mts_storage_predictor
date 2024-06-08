from aiogram.filters import CommandStart, Command
from aiogram.filters.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram import types, Router
from replics.get_replic import get_text
from inline_buttons.buttons import greeteng_actions_list, main_menu_actions_list, return_actions_list, get_answers_list
import sys
from dotenv import load_dotenv
import os

# sys.path.append(f'{os.environ.get("PWD")}/..')

from data.train.get import get_data_predict
from data.train.send import send_data_predict

load_dotenv()

router = Router()

regions_list = ["МСК", "Центр", "СЗ", "НН", "Юг", "Урал", "Сиб", "ДВ"]
region = ''
get_list = []
send_list = []
initial_volume = 0
get_prediction_list = []
send_prediction_list = []

class Dialog(StatesGroup):
    main = State()
    region = State()
    get_data = State()
    send_data = State()
    volume_data = State()
    check_code = State()
    answer = State()
    prediction_success = State()

@router.message(CommandStart())
async def start_message(message: types.Message, state: FSMContext):
    await state.set_state(Dialog.check_code)
    await message.answer(get_text(text_name="check_code"))

@router.message(Dialog.check_code)
async def check_code(message: types.Message, state: FSMContext):
    if (message.text != os.getenv("SECRET_CODE")):
        await message.answer(get_text(text_name="check_code_fail"))
    else:
        await state.set_state(Dialog.main)
        await message.answer(get_text(text_name="greeting"), reply_markup=greeteng_actions_list)

@router.message(Dialog.main)
async def main_menu(message: types.Message, state: FSMContext):
    try:
        os.remove(f'send{str(message.chat.id)}.png')
        os.remove(f'get{str(message.chat.id)}.png')
    except Exception:
        print()
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
            await state.set_state(Dialog.send_data)
            await message.answer(get_text(text_name="send_data"), reply_markup=return_actions_list)
        except Exception:
            await message.answer(get_text(text_name="get_data_error"))


@router.message(Dialog.send_data)
async def send_data(message: types.Message, state: FSMContext):
    global send_list
    if message.text == "Главное меню":
        await state.set_state(Dialog.main)
        await main_menu(message=message, state=state)
    else:
        try:
            send_list = [int(x) for x in message.text.split(" ")]
            if len(get_list) != len(send_list):
                await message.answer(get_text(text_name="send_data_error2"))
            else:        
                await state.set_state(Dialog.volume_data)
                await message.answer(get_text(text_name="initial_volume"), reply_markup=return_actions_list)
        except Exception as e:
            await message.answer(get_text(text_name="get_data_error"))

@router.message(Dialog.volume_data)
async def volume_data(message: types.Message, state: FSMContext):
    global initial_volume
    if message.text == "Главное меню":
        await state.set_state(Dialog.main)
        await main_menu(message=message, state=state)
    else:
        try:
            initial_volume = int(message.text)
            await state.set_state(Dialog.answer)
            await answer(message=message, state=state)
        except Exception:
            await message.answer(get_text(text_name="get_data_error"))

        
@router.message(Dialog.answer)
async def answer(message: types.Message, state: FSMContext):
    global get_prediction_list, send_prediction_list
    get_prediction_list = await get_data_predict(region, get_list, message.chat.id)
    send_prediction_list = await send_data_predict(region, send_list, message.chat.id)
    await state.set_state(Dialog.prediction_success)
    await message.answer(get_text(text_name="success_prediction"), reply_markup=get_answers_list)



@router.message(Dialog.prediction_success)
async def answer_check(message: types.Message, state: FSMContext):
    if message.text == "Главное меню":
        await state.set_state(Dialog.main)
        await main_menu(message=message, state=state)
    elif message.text == "Объем, который необходимо зарезервировать для каждого месяца":
        current_volume = initial_volume
        result = ''
        for i in range(len(get_prediction_list)):
            result += f"Через {i + 1} мес: {round(current_volume + get_prediction_list[i] - send_prediction_list[i], 2)} м^3\n"
            current_volume = current_volume + get_prediction_list[i] - send_prediction_list[i]
        await message.answer(text=result)
    elif message.text == "График для получения":
        await message.answer_photo(photo=types.FSInputFile(path=f"get{str(message.chat.id)}.png"))
    elif message.text == "График для отправки":
        await message.answer_photo(photo=types.FSInputFile(path=f"send{str(message.chat.id)}.png"))
    else:
        await message.answer(get_text(text_name="answer_check_error"))
