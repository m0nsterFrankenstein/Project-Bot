from telegram.ext import Updater,CommandHandler,MessageHandler,Filters # import the required handlers from telegram.ext package
from Adafruit_IO import Client,Feed,Data   # import the libraries to create feeds and send data to it
import os   #operating system

ADAFRUIT_IO_USERNAME = os.getenv('ADAFRUIT_IO_USERNAME')   # adafruit username and password should be given as 'Config Vars' in the settings of your app on Heroku 
ADAFRUIT_IO_KEY = os.getenv('ADAFRUIT_IO_KEY')
aio = Client('ADAFRUIT_IO_USERNAME','ADAFRUIT_IO_KEY') # create instance of REST client
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')  # similar to the adafruit username and password

# for displaying the /start command message so that the user knows what the bot does 
def start(bot, update):
    print(str( update.effective_chat.id ))
    bot.send_message(chat_id = update.effective_chat.id, text="Welcome! Type 'Turn on the Light' or /lighton to switch on the light bulb. Type 'Turn off the Light' or /lightoff to switch off the light bulb.")
# if the user types some unknown command
def unknown(bot, update):
    bot.send_message(chat_id=update.effective_chat.id, text="Oops, I didn't understand that. Try again!")

# function to send values to adafruit.io
def value_send(value):
  to_feed = aio.feeds('lightbotctrl') # put your own feed name here
  aio.send_data(to_feed.key,value)  # append a new value to a feed

# function to switch on light and send value '1' to adafruit
def lighton(bot, update):
  chat_id = update.message.chat_id
  bot.send_message(chat_id, text="Light has been turned ON")
  bot.send_photo(chat_id, photo='https://www.securityroundtable.org/wp-content/uploads/2019/03/AdobeStock_261504199-scaled.jpeg')
  value_send(1)
#function to switch off the light and send value '0' to adafruit
def lightoff(bot, update):
  chat_id = update.message.chat_id
  bot.send_message(chat_id, text="Light has been turned OFF")
  bot.send_photo(chat_id=update.effective_chat.id,photo='https://ak.picdn.net/shutterstock/videos/1027638404/thumb/1.jpg?ip=x480')
  value_send(0)
# function to control the bot without giving commands
def given_message(bot, update):
  text = update.message.text.upper()
  text = update.message.text
  if text == 'Turn on the Light':
    lighton(bot,update)
  
  elif text == 'Turn off the Light':
    lightoff(bot,update)

u = Updater('TELEGRAM_TOKEN',use_context = True) 
dp = u.dispatcher
dp.add_handler(CommandHandler('lighton',lighton))  # register a handler
dp.add_handler(CommandHandler('lightoff',lightoff))
dp.add_handler(CommandHandler('start', start))
dp.add_handler(MessageHandler(Filters.command, unknown)) # Filters.command allows messages starting with a bot command
dp.add_handler(MessageHandler(Filters.text, given_message)) # Filters.text allows text messages

u.start_polling()  # starts polling updates from Telegram
u.idle() # blocks until one of the signals are received and stops the updater
