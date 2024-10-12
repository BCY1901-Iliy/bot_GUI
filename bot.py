from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import filters, ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, \
    CallbackQueryHandler, ConversationHandler

TOKEN = '6350996888:AAGJONPVfVBjoklFhtxB004u8zxX0i_ctM8'

list_of_pref = ['Программирование', 'Коммуникации']
users_choice = []
START_ROUTES, END_ROUTES, DEL_ROUTE, ADD_ROUTE, PROCESS_ADD = range(5)
# Callback data
ONE, TWO, THREE, FOUR = range(4)


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f'Привет {update.effective_user.first_name}\n'
                                        'Я могу присылать вам новости\n\n'
                                        'Для обновления рассылки новостей по тэгам используйте команду /news\n'
                                        'Для настройки тэгов испоьзуйте команду /show_tags\n'
                                        'Для поиска поиска по ключевым словам используйте команду /search с '
                                        'пользовательскими '
                                        'параметрами\n'
                                        'Чтобы узнать подробнее введите /help')


async def bad_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=update.message.text + ' - не является командой')


async def get_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pref = ' '.join(users_choice)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f'Бот обновляет и присылает новости в соотвествии с выбранными тегами {pref}...')


async def get_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text='Бот осуществляет новостну рассылку  в соотвествии с выбранными тегами\n'
                                        'Для вызова меню управления тегами исполлзуется команда /show_tags\n'
                                        'Для прямого добавления тегов используется команда /add_tags\n'
                                        'Для прямого удаления тиспользуется команда /delete_tags\n'
                                        f'Для поиска по ключевым словам используйте команду /search\n'
                                        f'Пример:\n/search it в науке в наши дни\n\n'
                                        'Сообщения об ошибках и пожелания присылать на адрес developers_email@gmail.com'
                                    )


async def search_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    x = " ".join(context.args)

    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f'Бот ищет новость по ключевым словам \"{x}\"')


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    keyboard = [[InlineKeyboardButton(text, callback_data=text)]
                for text in list_of_pref
                if text != query.data
                if text not in users_choice]

    keyboard.append([InlineKeyboardButton('Сохранить', callback_data='0')])

    if query.data == '/get_pref':
        keyboard = [[InlineKeyboardButton(text, callback_data=text)]
                    for text in list_of_pref
                    if text not in users_choice]
        keyboard.append([InlineKeyboardButton('Сохранить', callback_data='0')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Пожалуйста выберите интересующие теги:", reply_markup=reply_markup)

    elif query.data == '/delete_tags':
        keyboard = [[InlineKeyboardButton(text, callback_data='del' + text)]
                    for text in list_of_pref
                    if text in users_choice]
        keyboard.append([InlineKeyboardButton('Сохранить', callback_data='0')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Выберите теги которые хотите удалить:", reply_markup=reply_markup)

    elif query.data == '0':
        pref = ' '.join(users_choice)
        await query.edit_message_text(f'Ваши выбранные теги: {pref}')
    else:
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.answer()
        if 'del' not in query.data:
            users_choice.append(query.data)
            await query.edit_message_text(text=f"Вы добавили: {query.data}", reply_markup=reply_markup)
        else:
            keyboard = [[InlineKeyboardButton(text, callback_data='del' + text)]
                        for text in list_of_pref
                        if text in users_choice
                        if text != query.data[3:]]
            keyboard.append([InlineKeyboardButton('Сохранить', callback_data='0')])
            reply_markup = InlineKeyboardMarkup(keyboard)
            users_choice.remove(query.data[3:])
            await query.edit_message_text(text=f"Вы удалили: {query.data[3:]}", reply_markup=reply_markup)


async def get_pref(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(text, callback_data=text)]
                for text in list_of_pref
                if text not in users_choice]
    keyboard.append([InlineKeyboardButton('Сохранить', callback_data='0')])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(text="Пожалуйста выберите интересующие теги:", reply_markup=reply_markup)


async def procc_get(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    users_choice.append(query.data)
    keyboard = [[InlineKeyboardButton(text, callback_data=text)]
                for text in list_of_pref
                if text not in users_choice]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=f"Вы добавили: {query.data}", reply_markup=reply_markup)
    return PROCESS_ADD


async def show_pref(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pref = ' '.join(users_choice)
    keyboard = [[InlineKeyboardButton('Добавить теги', callback_data='/get_pref'),
                 InlineKeyboardButton('Удалить теги', callback_data='/delete_tags')],
                [InlineKeyboardButton('Оставить без изменений', callback_data='0')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(f'Ваши выбранные теги: {pref}', reply_markup=reply_markup)


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    pref = ' '.join(users_choice)
    await query.answer()
    await query.edit_message_text(text=f'Ваши теги: {pref}')
    return ConversationHandler.END


async def delete_tags(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(text, callback_data='del' + text)]
                for text in list_of_pref
                if text in users_choice]
    keyboard.append([InlineKeyboardButton('Сохранить', callback_data='0')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите теги которые хотите удалить:", reply_markup=reply_markup)
    return DEL_ROUTE


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    # conv_handler = ConversationHandler(
    #     entry_points=[CommandHandler("show_tags", show_pref)],
    #     states={
    #         ADD_ROUTE: [
    #             CallbackQueryHandler(get_pref, pattern="/get_pref"),
    #         ],
    #         PROCESS_ADD: [
    #
    #         ],
    #         DEL_ROUTE: [
    #             CallbackQueryHandler(delete_tags, pattern="/delete_tags"),
    #         ],
    #         END_ROUTES: [
    #             CallbackQueryHandler(end, pattern="0"),
    #         ],
    #     },
    #     fallbacks=[CommandHandler("start", start)],
    # )
    # application.add_handler(conv_handler)
    echo_handler = MessageHandler(filters.TEXT, bad_input)
    favor_command = CommandHandler('add_tags', get_pref)
    start_handler = CommandHandler('start', start)
    del_tags = CommandHandler('delete_tags', delete_tags)
    application.add_handler(CommandHandler('show_tags', show_pref))
    application.add_handler(del_tags)
    application.add_handler(favor_command)
    application.add_handler(CommandHandler('news', get_news))
    application.add_handler(start_handler)
    application.add_handler(CommandHandler('help', get_help))
    application.add_handler(CommandHandler('search', search_data))
    application.add_handler(echo_handler)
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()
