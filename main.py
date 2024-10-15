from aiogram import executor


if __name__ == '__main__':
    from handlers import callbackHandlers
    from create import dp

    callbackHandlers.registerHandlers(dp)
    executor.start_polling(dp, skip_updates=True, timeout=1_000_000)
