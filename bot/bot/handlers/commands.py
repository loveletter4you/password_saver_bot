from aiogram import Router
from aiogram.filters import CommandStart, Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.service import Service
from bot.utils.handler_utils import delete_message, create_inline_button, encrypt_text, decrypt_text

router = Router(name="commands-router")


class OrderService(StatesGroup):
    choosing_service_name = State()
    choosing_login = State()
    choosing_password = State()
    choosing_get_service = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        text="Этот бот поможет вам не забывать пароли от любых сервисов.\n"
        "Добавляйте сервисы при помощи комманды /set, "
        "а затем получите любой из добавленных логинов и паролей при помощи комманды /get. "
        "Также вы можете удалить любой добавленный сервис коммандой /del"
    )


@router.message(Command(commands=["cancel"]))
@router.message(Text(text="отмена", ignore_case=True))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
    )
    await delete_message(message)


@router.message(Command("set"))
async def cmd_add_service(message: Message, state: FSMContext):
    await message.answer(
        text="Введите название сервиса",
    )
    await state.set_state(OrderService.choosing_service_name)
    await delete_message(message)


@router.message(OrderService.choosing_service_name, Text)
async def service_name_chosen(message: Message, state: FSMContext):
    await state.update_data(service=message.text)
    await delete_message(message)
    await message.answer(text="Введите логин.")
    await state.set_state(OrderService.choosing_login)


@router.message(OrderService.choosing_login, Text)
async def service_name_chosen(message: Message, state: FSMContext):
    await state.update_data(login=message.text)
    await delete_message(message)
    await message.answer(text="Введите пароль.")
    await state.set_state(OrderService.choosing_password)


@router.message(OrderService.choosing_password, Text)
async def service_name_chosen(message: Message, state: FSMContext, session: AsyncSession):
    user_data = await state.get_data()
    service = Service(
        telegram_id=message.from_user.id,
        service_name=user_data['service'],
        login=encrypt_text(user_data['login']),
        password=encrypt_text(message.text)
    )
    await session.merge(service)
    await session.commit()
    await message.answer(
        text=f"Сервис {service.service_name} успешно сохранен!",
    )
    await delete_message(message)
    await state.clear()


@router.message(Command("get"))
@router.message(Command("del"))
async def get_services(message: Message, session: AsyncSession):
    services_request = await session.execute(select(Service).filter_by(telegram_id=message.from_user.id))
    services = services_request.scalars().all()
    if len(services) == 0:
        await message.answer(
            text=f"У вас нет ни одного сервиса!",
        )
        await delete_message(message)
        return
    if message.text.startswith('/get'):
        services_buttons = [create_inline_button(f'{service.service_name}', f'get_service{service.id}') for service
                            in services]
        keyboard_builder = InlineKeyboardBuilder(markup=[services_buttons])
        keyboard_builder.adjust(1)
        await message.answer(
            text=f"Выберите сервис!",
            reply_markup=keyboard_builder.as_markup()
        )
    elif message.text.startswith('/del'):
        services_buttons = [create_inline_button(f'{service.service_name}', f'del_service{service.id}') for service in
                            services]
        keyboard_builder = InlineKeyboardBuilder(markup=[services_buttons])
        keyboard_builder.adjust(1)
        await message.answer(
            text=f"Выберите сервис для удаления!",
            reply_markup=keyboard_builder.as_markup()
        )
    await delete_message(message)


@router.callback_query(lambda callback: callback.data and callback.data.startswith('get_service'))
async def get_service(callback: CallbackQuery, session: AsyncSession):
    service_request = await session.execute(select(Service).filter_by(id=int(callback.data.replace('get_service', ''))))
    service = service_request.scalar()
    if service is None:
        await callback.message.answer(
            text="Сервиса не существует!"

        )
        await delete_message(callback.message)
        return
    message = await callback.message.answer(
        text=f'Сервис: {service.service_name}\n'
             f'Логин: {decrypt_text(service.login)}\n'
             f'Пароль {decrypt_text(service.password)}',
    )
    await delete_message(callback.message)
    await delete_message(message, 10)


@router.callback_query(lambda callback: callback.data and callback.data.startswith('del_service'))
async def get_service(callback: CallbackQuery, session: AsyncSession):
    service_request = await session.execute(select(Service).filter_by(id=int(callback.data.replace('del_service', ''))))
    service = service_request.scalar()
    if service is None:
        await callback.message.answer(
            text=f'Сервиса не существует!',
        )
        await delete_message(callback.message)
        return
    await session.delete(service)
    await session.commit()
    await callback.message.answer(
            text=f'Сервис {service.service_name} удален!',
    )
    await delete_message(callback.message)

