# import modules
import telegram.ext
import os
import wikipedia
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode

# constants
PORT = int(os.environ.get("PORT", 443))
TOKEN = "[YourTelegramToken]"

# mutliple results display buttons
def create_disambiguation_keyboard(disambiguation_options):
    keyboard = []

    for option in disambiguation_options:
        new_option = [
            InlineKeyboardButton(option, callback_data="ERROR;DISAMBIGUATION;" + option)
        ]
        keyboard.append(new_option)

    return InlineKeyboardMarkup(keyboard)


# function to fetch wikipedia articles
def wikipedia_page():
    query = updater.message.text
    try:
        result = wikipedia.summary(query, sentences=2, auto_suggest=False)
    except wikipedia.exceptions.DisambiguationError as e:
        # na = e.options
        na = create_disambiguation_keyboard(e.options)

        return f"""
                    Please specify your query for {query}:
                    \n Example: If you want {na[1]}, Copy and paste (or just type) {na[1]}
                    \n\n{na}
        
        """

    return f"{query}\n\n{result}"


# Bot start function
def start(update, context):
    update.message.reply_text(
        """

Wikipedia Summarizer is a bot that summarises Wikipedia articles for you.

<b>USAGE:</b>
To search for articles, type and send your keyword.
    """,
        parse_mode=ParseMode.HTML,
    )


def handle_message(update, context):
    update.message.reply_text(wikipedia_page(update.message.text))
    update.message.reply_text(wikipedia.page(update.message.text).images[0])


updater = telegram.ext.Updater(TOKEN, use_context=True)
disp = updater.dispatcher


disp.add_handler(telegram.ext.CommandHandler("start", start))
disp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))

# for deployment
# updater.start_webhook(
#     listen="0.0.0.0",
#     port=int(PORT),
#     url_path=TOKEN,
#     webhook_url="[YourHerokuSite]/" + TOKEN,
# )

# for local deployment
updater.start_polling()
updater.idle()
