import logging
from telegram import Update, Document
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import subprocess
import os

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Define the invert function
def invert(input_file, output_file):
    if input_file == output_file:
        directory = os.path.dirname(input_file)
        fullname = os.path.basename(input_file)
        extension = fullname.split('.')[-1]
        filename = fullname.split('.')[0]

        output_file = f"{directory}/{filename}_inv.{extension}"

    logging.info(f"Inverting '{input_file}' to '{output_file}' ---------------------------------------------")

    subprocess.run(['gs', '-o', output_file, '-sDEVICE=pdfwrite', '-c', '{1 exch sub}{1 exch sub}{1 exch sub}{1 exch sub} setcolortransfer', '-f', input_file])

# Define the start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your PDF inverter bot. Send me a PDF file, and I will invert its colors.')

# Define the invert command
def invert_command(update: Update, context: CallbackContext) -> None:
    if not update.message.document:
        update.message.reply_text('Please send a PDF file for inversion.')
        return

    document: Document = update.message.document
    file_id = document.file_id
    new_file = f"{file_id}_inv.pdf"

    # Download the file
    file_path = context.bot.get_file(file_id).download()

    # Perform the inversion
    invert(file_path, new_file)

    # Send the inverted file
    update.message.reply_document(document=open(new_file, 'rb'), caption='Inverted PDF')

    # Clean up the temporary files
    os.remove(file_path)
    os.remove(new_file)

# Set up the bot token and start the bot
def main():
    updater = Updater("YOUR_BOT_TOKEN")
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.document, invert_command))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
