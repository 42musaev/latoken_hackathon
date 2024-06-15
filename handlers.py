from aiogram import Router, F
from aiogram.types import Message
from query_data import generate_local_response

router = Router()


@router.message(F.text)
async def echo(message: Message):
    print(message.text)
    if res := generate_local_response(message.text):
        await message.answer(res)
    await message.answer("Many requests. 10 second timeout")
