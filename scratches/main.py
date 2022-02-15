import threading
from queue import Queue
import bot_overlay
import bot

q = Queue()
bot_thread = threading.Thread(target=bot.bot, args=(q, ))
bot_overlay_thread = threading.Thread(target=bot_overlay.createOverlay, args=(q, ))

bot_thread.start()
bot_overlay_thread.start()

