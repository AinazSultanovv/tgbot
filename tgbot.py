import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler



# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Определение состояний для ConversationHandler
CHOOSING, TARGET_CHOICE = range(2)

# Тексты валентинок
valentines_texts = {
    '14 февраля': "Любимый/Любимая, ты самое прекрасное, что случилось в моей жизни! С Днем всех влюбленных!",
    'маме': "Дорогая мама, спасибо за твою любовь и заботу! С 8 Марта!",
    'сестре': "Дорогая сестра, ты самая лучшая! С 8 Марта!",
    'девушке': "Моя любимая, ты самая прекрасная! С 8 Марта!",
    'подруге': "Дорогая подруга, спасибо за твою дружбу! С 8 Марта!",
}

# Команда /start
async def start(update: Update, context):
    reply_keyboard = [['14 февраля', '8 марта']]
    await update.message.reply_text(
        "Привет! Я бот для создания валентинок. Выбери праздник:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return CHOOSING

# Обработка выбора праздника
async def choose_holiday(update: Update, context):
    holiday = update.message.text
    if holiday == '14 февраля':
        await update.message.reply_text(valentines_texts['14 февраля'])
        return ConversationHandler.END
    elif holiday == '8 марта':
        reply_keyboard = [['маме', 'сестре', 'девушке', 'подруге']]
        await update.message.reply_text(
            "Кому вы хотите отправить валентинку?",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )
        return TARGET_CHOICE

# Обработка выбора получателя для 8 марта
async def choose_target(update: Update, context):
    target = update.message.text
    await update.message.reply_text(valentines_texts[target])
    return ConversationHandler.END

# Команда /cancel для отмены
async def cancel(update: Update, context):
    await update.message.reply_text("Создание валентинки отменено.")
    return ConversationHandler.END

def main():
    application = ApplicationBuilder().token('8102899596:AAE17jz7TNpTRJN55m74EzkAQrDEbUcD7Bw').build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_holiday)],
            TARGET_CHOICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_target)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    application.add_handler(conv_handler)

    application.run_polling()

if __name__ == '__main__':
    main()