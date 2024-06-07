from aiogram import Bot, Dispatcher
import asyncio
from dotenv import load_dotenv
import os
from handlers import user_commands
import sys

sys.path.append(f'{os.environ.get("PWD")}/..')

load_dotenv()

async def main():
    bot = Bot(token=os.getenv("API_KEY"))
    dp = Dispatcher()

    dp.include_routers(
        user_commands.router
    )
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

