import telebot
from telebot import types

from pyzbar.pyzbar import decode
from PIL import Image
import io
import pandas as pd

bot = telebot.TeleBot("API")


@bot.message_handler(commands=["start"])
def hello_handle(message):
    """
    Greets the user when the bot is started and displays available options.
    It sends an appropriate greeting depending on whether the user has a last name or not.
    Calls the choise_comands() function to display the command menu.

    Arguments:
    - message (telebot.types.Message): The message object that contains the user's data and the message.
    """

    if message.from_user.last_name:
        bot.send_message(
            message.chat.id, f"Привіт, {message.from_user.first_name} {message.from_user.last_name}")
        choise_comands(message)
    else:
        bot.send_message(
            message.chat.id, f"Привіт, {message.from_user.first_name}")
        choise_comands(message)


def choise_comands(message):
    """
    Creates a keyboard with buttons for selecting actions:
    1. Upload a photo
    2. Enter manually
    3. Help

    Arguments:
    - message (telebot.types.Message): The message object to send the keyboard.
    """

    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton(
        "Завантажити фото", callback_data="Take_a_photo")
    btn2 = types.InlineKeyboardButton(
        "Ввести вручну", callback_data="manual_input")
    btn3 = types.InlineKeyboardButton("Допомога", callback_data="help_handle")
    markup.add(btn1, btn2, btn3)
    bot.send_message(
        message.chat.id, "Оберіть будь ласка команду", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    """
    Handles button presses on the inline keyboard:
    - "Take_a_photo": requests a photo to analyze the barcode.
    - "manual_input": prompts the user to enter a barcode manually.
    - "help_handle": provides help to the user.

    Arguments:
    - call (telebot.types.CallbackQuery): The object containing data about the user's button press.
    """
    if call.data == "Take_a_photo":
        bot.send_message(call.message.chat.id, "Будь ласка, надішліть фото.")
        bot.register_next_step_handler(call.message, image)

    elif call.data == "manual_input":
        bot.send_message(call.message.chat.id, "Введіть дані вручну.")
        bot.register_next_step_handler(call.message, manual)

    elif call.data == "help_handle":
        help_text = (
            "Цей бот дозволяє вам виконувати наступні дії:\n\n"
            "1. **Завантажити фото**:\n"
            "   - Натисніть кнопку 'Завантажити фото', щоб надіслати зображення з штрих-кодом.\n"
            "   - Бот розпізнає код і надасть інформацію про товар, якщо його знайдено в базі даних 'Зроблено в Україні'.\n\n"
            "2. **Ввести штрих-код вручну**:\n"
            "   - Натисніть кнопку 'Ввести вручну', щоб ввести штрих-код самостійно.\n"
            "   - Бот надасть інформацію про товар, якщо його знайдено в базі даних 'Зроблено в Україні'.\n\n"
            "3. **Отримати допомогу**:\n"
            "   - Натисніть кнопку 'Допомога', щоб переглянути цю інструкцію.\n\n"
            "Більш детальну інформацію про умови можна знайти за посиланням:\n"
            "https://madeinukraine.gov.ua/"
        )

        bot.send_message(call.message.chat.id, help_text)
        choise_comands(call.message)


def image(message):
    """
    Processes the received photo, looks for barcodes and calls the search function.
    If a barcode is found, it calls search_csv to search in the database.
    If the photo does not contain a barcode or is invalid, it sends an error message.

    Arguments:
    - message (telebot.types.Message): The message object containing the user's photo to process.
    """
    if message.content_type == 'photo':
        file_id = message.photo[-1].file_id

        file_info = bot.get_file(file_id)

        downloaded_file = bot.download_file(file_info.file_path)

        image_stream = io.BytesIO(downloaded_file)
        try:
            img = Image.open(image_stream)

            decoded_objects = decode(img)

            if decoded_objects:
                first_obj = next((obj for obj in decoded_objects if obj.type in [
                                 'EAN13', 'EAN8', 'UPC']), None)

                if first_obj:  
                    decoded_data = first_obj.data.decode("utf-8")
                    search_csv(decoded_data, message)
                else:
                    bot.send_message(
                        message.chat.id, "На фото не знайдено штрих-код відповідного типу.")
                    choise_comands(message)
            else:
                bot.send_message(
                    message.chat.id, "На фото не знайдено жодного штрих-коду.")
                choise_comands(message)

        except IOError:
            bot.send_message(
                message.chat.id, "Файл не є дійсним зображенням. Будь ласка, надішліть фото.")
            choise_comands(message)
    else:
        bot.send_message(
            message.chat.id, "Файл не є дійсним зображенням. Будь ласка, надішліть фото.")
        choise_comands(message)


def search_csv(id_code, message):
    """
    Searches for the product in the CSV file using the provided barcode.
    If the product is found, it sends the product name; otherwise, it notifies that the product was not found.

    Arguments:
    - id_code (int): The barcode of the product to search for in the database.
    - message (telebot.types.Message): The message object to send the search results to the user.
    """
    id_code = int(id_code)
    df = pd.read_csv('file.csv', delimiter=';')
    result = df[df['Штрих-код'] == id_code]

    if not result.empty:
        product_name = result['Назва товару'].values[0]
        response_text = f"Товар є у списку: {product_name}"
    else:
        response_text = "Товар не знайдено."

    bot.send_message(
        message.chat.id, response_text)

    choise_comands(message)





def manual(message):
    """
    Processes the manually entered barcode, checking its validity.
    If an invalid value is entered, it sends an error message.

    Arguments:
    - message (telebot.types.Message): The message object containing the manually entered barcode by the user.
    """

    try:
        id_code = message.text.strip()
        id_code_int = int(id_code)
        search_csv(id_code_int, message)
    except ValueError:
        bot.send_message(
            message.chat.id, "Будь ласка, введіть коректний цілий номер.")
        choise_comands(message)


if __name__ == "__main__":
    bot.polling(non_stop=True)
