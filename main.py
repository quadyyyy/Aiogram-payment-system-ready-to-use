import config
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType

# логирование / logging
logging.basicConfig(level=logging.INFO)

# инициализация / init
bot = Bot(token=config.Token)
dp = Dispatcher(bot)

# цены / prices
Price = types.LabeledPrice(label='Подписка на 1 месяц', amount=179*100) 

# покупка / buy command
@dp.message_handler(commands=['buy'])
async def buy(message: types.Message):
    if config.Payments_Token.split(':')[1] == 'TEST':
        await bot.send_message(message.chat.id, 'Тестовый платеж')

    await bot.send_invoice(message.chat.id,
    title='Подписка на канал',
    description='Активация подписки на канал на 1 месяц',
    provider_token=config.Payments_Token,
    currency='rub',
    is_flexible=False,
    prices=[Price],
    start_parameter='one-month-subscription',
    payload='test-invoice-payload')

# пре-чекаут (ответ серверу должен быть отправлен в течение 10 секунд, иначе платеж не пройдет) / pre-checkout
@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)

# успешная оплата / succesful payment
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    print("SUCCESSFUL PAYMENT:")
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")
 
    await bot.send_message(message.chat.id,
                           f"Платёж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно!!!")


# запуск лонгпула
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)