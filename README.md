# Telegram Barcode Bot

This is a Telegram bot that allows users to scan barcodes from images or enter them manually to get information about a product. The bot is integrated with a database (CSV file) that contains product details.

## Features

- **Upload a photo**: Send an image containing a barcode, and the bot will decode the barcode and provide product information.
- **Manual input**: Enter a barcode manually, and the bot will search for product information in the database.
- **Help**: Get detailed instructions on how to use the bot.

## Requirements

Before running the bot, make sure you have the following dependencies installed:

- **Python 3.6+**
- **pyzbar**: A library for reading barcodes from images.
- **Pillow**: A Python Imaging Library to handle image processing.
- **pandas**: A library to work with data structures like DataFrames, used for managing the product database.
- **python-telegram-bot**: A Python wrapper for the Telegram Bot API.

To install the required libraries, run:

```bash
pip install pyzbar pillow pandas python-telegram-bot

```



## Setup
1. Get the Telegram Bot API key
Create a bot on Telegram by following these steps:

Open Telegram and search for the BotFather.
Use the /newbot command to create a new bot and get an API key.
Store this API key securely.

2. Configure the bot
Replace the API in the bot = telebot.TeleBot("API") line with your actual API key.

3. Prepare the database
Create a products.csv file with product information.


## Commands and Actions

#### `/start`
When the bot is started, it greets the user and shows the available options:

- **Upload a photo**: Send a photo that contains a barcode.
- **Enter manually**: Enter a barcode manually.
- **Help**: Get instructions on how to use the bot.

---

#### **Upload a photo**
Send a photo with a barcode, and the bot will try to detect the barcode and search for the product in the database.

---

#### **Enter manually**
Type in a barcode, and the bot will search for the product in the database.

---

#### **Help**
Get detailed instructions on how to use the bot.
## Example Usage

1. **User starts the bot**  
   The bot greets the user and provides options to either upload a photo, enter a barcode manually, or request help.

2. **User uploads a photo**  
   The bot will decode any valid barcode (EAN13, EAN8, UPC) from the image and look for the product in the database. If found, it returns the product name.

3. **User enters a barcode manually**  
   The bot searches the product database for the entered barcode and responds with the product information.

4. **User requests help**  
   The bot provides instructions on how to use the available commands.

