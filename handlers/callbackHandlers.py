import os
from symtable import Class

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, InputFile

from create import bot
from data import *

# from dotenv import load_dotenv, find_dotenv

menuMessage: dict[int, types.Message] = {}

async def start(message: types.Message) -> None:
    """Функция старта бота"""
    await message.delete()
    await resendMenuMessage(userID=message.from_user.id, text=mainMenuText, replyMarkup=Keyboards.mainMenu.value)


async def headBackToMainMenu(callback: types.CallbackQuery) -> None:
    """Head back to main menu"""
    await callback.answer()
    await editMenuMessageText(userID=callback.from_user.id, text=mainMenuText, replyMarkup=Keyboards.mainMenu.value)












class RegisterHours(StatesGroup):
    enterDate: State = State()
    enterHours: State = State()

async def registerHours(callback: types.CallbackQuery) -> None:
    await callback.answer()
    await editMenuMessageText(text="Введите дату мероприятия:", userID=callback.from_user.id)
    await RegisterHours.enterDate.set()

async def registerHours_enterDate(message: types.Message, state: FSMContext):
    if message.text == "/cancel":
        await state.finish()
        await editMenuMessageText(userID=message.from_user.id, text=mainMenuText, replyMarkup=Keyboards.mainMenu.value)
        await message.delete()

    else:
        await bot.send_message(chat_id=message.from_user.id, text=f"{message.text} - сам хавай")
        await state.finish()
        await resendMenuMessage(userID=message.from_user.id, text=mainMenuText, replyMarkup=Keyboards.mainMenu.value)








async def editMenuMessageText(
        *, userID: int, text: str, replyMarkup=InlineKeyboardMarkup()
) -> None:
    """
    Edit menu message text, picture and inline keyboard

    :param userID: Chat ID where menu message should be edited
    :param text: The new text of the menu message
    :param replyMarkup: A new reply markup that will be attached to the message
    """
    try:
        menuMessage.update(
            {
                userID: await menuMessage.get(userID).edit_text(
                    reply_markup=replyMarkup,
                    text=text
                )
            }
        )
    except (KeyError, AttributeError) as ex:
        pass
        # Log.warning('[%s] Menu message can not be edited. (%s)', userID, ex)
        # await sendErrorMessage(userID=userID, text=editMenuMessageCaptionErrorText, delay=7.0)
    # except MessageNotModified as ex:
    #     Log.warning('[%s] Menu message was not edited. (%s)', userID, ex)


async def resendMenuMessage(
        userID: int, text: str, replyMarkup=InlineKeyboardMarkup()
) -> None:
    """
    Resend main menu message

    :param userID: Chat ID where menu message should be resent
    :param text: The new text of the menu message
    :param replyMarkup: A new reply markup that will be attached to the new message
    # :param newPhotoPath: A path to the new photo for the new message
    """
    try:
        await menuMessage.get(userID).delete()

    except Exception:
        pass
    # except MessageCantBeDeleted as ex:
    #     Log.warning('[%s] Menu message was not deleted. Deletion period expired. (%s)', userID, ex)
    #
    # except (AttributeError, MessageToDeleteNotFound) as ex:
    #     Log.warning('[%s] Menu message was not deleted, sending brand new instead. (%s)', userID, ex)
    # menuMessage.update(
    #     {
    #         userID: await bot.send_photo(
    #             chat_id=userID, photo=open(newPhotoPath, 'rb'),
    #             caption=text, reply_markup=replyMarkup)
    #     }
    # )

    menuMessage.update(
        {
            userID: await bot.send_message(chat_id=userID, text=text, reply_markup=replyMarkup)
        }
    )




def registerHandlers(dp: Dispatcher) -> None:
    dp.register_message_handler(start, commands=["start"])
    dp.register_callback_query_handler(headBackToMainMenu, text="headBackToMainMenu")
    dp.register_callback_query_handler(registerHours, text="registerHours")
    dp.register_message_handler(registerHours_enterDate, state=RegisterHours.enterDate, content_types=["text"])