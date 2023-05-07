import asyncio

from aiogram.types import InlineKeyboardButton, Message
from cryptography.fernet import Fernet

from settings_env import CIPHER_KEY

cipher = Fernet(CIPHER_KEY)


def create_inline_button(text: str, callback: str):
    return InlineKeyboardButton(text=text, callback_data=callback)


def encrypt_text(text: str):
    return cipher.encrypt(bytes(text, encoding='utf8')).decode('utf-8')


def decrypt_text(encrypted_text):
    return cipher.decrypt(bytes(encrypted_text, encoding='utf8')).decode('utf-8')


async def delete_message(message: Message, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    try:
        await message.delete()
    except Exception as e:
        pass
