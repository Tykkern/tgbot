from enum import Enum
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from data.menuText import backButtonText, backToMainMenuButton

def buildKeyboardEnum(buttons: dict, *adds: InlineKeyboardButton) -> InlineKeyboardMarkup:
    """Создать клавиатуру"""
    keyboard = InlineKeyboardMarkup()
    for text, callbackData in buttons.items():
        if type(callbackData) is dict:
            rowList = []
            for rowText, rowCallbackData in callbackData.items():
                rowList.append(InlineKeyboardButton(text=rowText, callback_data=rowCallbackData))
            keyboard.row(*rowList)
        else:
            keyboard.add(
                InlineKeyboardButton(text=text, callback_data=callbackData)
            )
    for button in adds:
        keyboard.add(button)
    return keyboard


class Buttons(Enum):
    backToMainMenu: InlineKeyboardButton = InlineKeyboardButton(
        text=backToMainMenuButton,
        callback_data="headBackToMainMenu"
    )

class Keyboards(Enum):
    mainMenu: InlineKeyboardMarkup = buildKeyboardEnum(
        {
            '📝\000Зарегестрировать часы': 'registerHours'
        }
    )

    backToMainMenu: InlineKeyboardMarkup = buildKeyboardEnum(
        {}, Buttons.backToMainMenu.value
    )
