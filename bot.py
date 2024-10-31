from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, \
    CallbackQueryHandler, CommandHandler, ContextTypes

from credentials import ChatGPT_TOKEN, TG_TOKEN
from gpt import ChatGptService
from util import load_message, load_prompt, send_text_buttons, send_text, \
    send_image, show_main_menu, Dialog, default_callback_handler


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = 'main'
    text = load_message('main')
    await send_image(update, context, 'main')
    await send_text(update, context, text)
    await show_main_menu(update, context, {
        'start': 'Главное меню',
        'random': 'Узнать случайный интересный факт 🧠',
        'gpt': 'Задать вопрос чату GPT 🤖',
        'talk': 'Поговорить с известной личностью 👤',
        'quiz': 'Поучаствовать в квизе ❓',
        'recipes': 'Подбор рецептов 🍝',
        'trainer': 'Словарный тренажёр 📖'
        # Добавить команду в меню можно так:
        # 'command': 'button text'

    })


dialog = Dialog()
dialog.mode = None
dialog.count = 0


# Переменные можно определить, как атрибуты dialog

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Отправляет сообщение обратно пользователю (task 1)
    """
    if dialog.mode == "gpt":
        await gpt_dialog(update, context)
    elif dialog.mode == "talk":
        await talk_dialog(update, context)
    elif dialog.mode == "quiz":
        await quiz_dialog(update, context)
    elif dialog.mode == "recipes":
        await recipes_dialog(update, context)
    else:
        text = update.message.text
        await send_text(update, context, text)


async def random_fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Task 2
    """
    promt = load_prompt("random")
    message = load_message("random")
    await send_image(update, context, "random")
    message = await send_text(update, context, message)
    answer = await chat_gpt.send_question(promt, "")
    await message.edit_text(answer)


async def gpt_dialog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Task 3
    """
    text = update.message.text
    message = await send_text(update, context, "Думаю над ответом...")
    answer = await chat_gpt.add_message(text)
    await message.edit_text(answer)


async def gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Task 3
    """
    dialog.mode = 'gpt'
    promt = load_prompt("gpt")
    message = load_message("gpt")
    chat_gpt.set_prompt(promt)
    await send_image(update, context, "gpt")
    await send_text(update, context, message)



async def talk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Task 4
    """
    dialog.mode = 'talk'
    message = load_message("talk")
    await send_image(update, context, "talk")
    await send_text_buttons(update, context, message, {
        "talk_cobain": "Курт Кобейн",
        "talk_queen": "Елизавета II",
        "talk_tolkien": "Джон Толкиен",
        "talk_nietzsche": "Фридрих Ницше",
        "talk_hawking": "Стивен Хокинг"
    })


async def talk_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Task 4
    """
    query = update.callback_query.data
    await update.callback_query.answer()
    promt = load_prompt(query)
    message = load_message("talk2")
    chat_gpt.set_prompt(promt)
    await send_image(update, context, query)
    await send_text(update, context, message)

async def talk_dialog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Task 4
    """
    text = update.message.text
    message = await send_text(update, context, "Думаю...")
    answer = await chat_gpt.add_message(text)
    await message.edit_text(answer)

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Task 5
    """
    dialog.mode = 'quiz'
    message = load_message("quiz")
    await send_image(update, context, "quiz")
    await send_text_buttons(update, context, message, {
        "quiz_prog": "Вопросы о Python",
        "quiz_math": "Математические теории",
        "quiz_biology": "Биология",
        "quiz_more": "Вопрос на ту же тему",
    })

async def quiz_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Task 5
    """
    query = update.callback_query.data
    await update.callback_query.answer()
    promt = load_prompt("quiz")
    chat_gpt.set_prompt(promt)
    message = await send_text(update, context,"Готовлю вопрос")
    answer = await chat_gpt.add_message(query)
    await message.edit_text(answer)

async def quiz_dialog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Task 5
    """
    text = update.message.text
    message = await send_text(update, context, "Думаю...")
    answer = await chat_gpt.add_message(text)
    if answer == "Правильно!":
        dialog.count += 1
    await message.edit_text(f"{answer}\nПравильных ответов: {dialog.count}")

async def recipes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Task 6.1
    """
    dialog.mode = 'recipes'
    message = load_message("recipes")
    await send_image(update, context, "recipes")
    await send_text(update, context, message)
async def recipes_dialog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Task 6.1
    """
    text = update.message.text
    promt = load_prompt("recipes")
    message = await send_text(update, context, "Думаю над ответом...")
    answer = await chat_gpt.send_question(promt, text)
    await message.edit_text(answer)

async def trainer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Task 6.2
    """
    dialog.mode = 'trainer'
    message = load_message("trainer")
    await send_image(update, context, "trainer")
    await send_text_buttons(update, context, message, {
        "trainer_new": "Хочу слово",
    })

async def trainer_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Task 6.2
    """
    query = update.callback_query.data
    await update.callback_query.answer()
    promt = load_prompt(query)
    message = await send_text(update, context, "Думаю над словом...")
    answer = await chat_gpt.send_question(promt, "")
    await message.edit_text(answer)


chat_gpt = ChatGptService(ChatGPT_TOKEN)
app = ApplicationBuilder().token(TG_TOKEN).build()
app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('random', random_fact))
app.add_handler(CommandHandler('talk', talk))
app.add_handler(CommandHandler('gpt', gpt))
app.add_handler(CommandHandler('quiz', quiz))
app.add_handler(CommandHandler('recipes', recipes))
app.add_handler(CommandHandler('trainer', trainer))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
# Зарегистрировать обработчик команды можно так:
# app.add_handler(CommandHandler('command', handler_func))

# Зарегистрировать обработчик кнопки можно так:
# app.add_handler(CallbackQueryHandler(app_button, pattern='^app_.*'))
app.add_handler(CallbackQueryHandler(talk_button, pattern='^talk_.*'))
app.add_handler(CallbackQueryHandler(quiz_button, pattern='^quiz_.*'))
app.add_handler(CallbackQueryHandler(trainer_button, pattern='^trainer_.*'))
app.add_handler(CallbackQueryHandler(default_callback_handler))
app.run_polling()
